# Lambda Curator
Lambda curator is a lambda function deletes old AWS ElasticSearch indices using [curator][curator].

All you need to do is tagging existing ES cluster.

## Getting Started

### Usage
By adding one or more tags to existing ES cluster, you enabled lambda curator to manage it.

A tag should follow one pattern, which is prefix=retention_period.

Example:

| Key | Value | Comment |
|-----|-------|---------|
| logstash- | 7d | indices starting with logstash- and older than 7 dayts will be deleted |
| curator.default | 1m | indices not matched by other prefixes and older than 1 month be deleted |

A manageable index name takes the following form:

> ^prefix-(\d{4}([-/.]w?\d{2}){,3})$

Example:

| Index | Comment |
|-----|-------|
| logstash-2018-02-01-01 | OneHour Rotation |
| logstash-2018-02-01 | OneDay Rotation |
| logstash-2018-02 | OneMonth Rotation |
| logstash-2018-w02 | OneWeek Rotation |
| logstash-2018 | OneYear Rotation |
| logstash-2018.05.10 | . as delimiter |
| logstash-2018/05/10 | / as delimiter |

A retention period takes the following form:

> `\d+[y|m|w|d|h]`

Example:

| Retention | Comment |
|-----|-------|
| 12h | retain 12 hours |
| 7d | retain 7 days |
| 1w | retain 1 week |
| 1m | retain 1 month |
| 1y | retain 1 year |

### Installation
It's as easy as launching a CloudFormation (or
[Terraform][Terraform])
stack and setting the `prefix=retention_period` tag on existing ES cluster.
All the required infrastructure and configuration will be created automatically,
so you can get started as fast as possible.

[![Launch](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=LambdaCurator&templateURL=https://s3.amazonaws.com/harmy.github.com/lambda-curator/template.yaml)

A single installation can handle all enabled clusters across all available AWS regions, but can be restricted to fewer regions if desired.

## License
This software is distributed under the terms of the Apache-2.0 [license][license].

[curator]: https://github.com/elastic/curator
[license]: https://github.com/harmy/lambda-curator/blob/master/LICENSE
[Terraform]: https://github.com/harmy/lambda-curator/tree/master/terraform


## Usage

```
provider "aws" {
  region = "us-east-1"
}

module "lambda_curator" {
  source       = "github.com/harmy/lambda-curator//terraform"

  schedule_expression = "rate(1 day)"
  regions = "us-east-1 us-east-2"
}

```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| enabled | If true, schedule_expression will be applied | string | `true` | no |
| regions | Regions in which lambda-curator is enabled, split by comma or space,leave it blank as all regions enabled | string | `` | no |
| schedule_expression | Optional rate() or cron() expression to schedule the Lambda function at regular intervals | string | `rate(1 hour)` | no |
| stage | Stage, e.g. 'prod', 'staging', 'dev', or 'test' | string | `prod` | no |

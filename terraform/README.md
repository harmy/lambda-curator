
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| enabled | If true, schedule_expression will be applied | string | `true` | no |
| regions | Regions in which lambda-curator is enabled, split by comma or space,leave it blank as all regions enabled | string | `` | no |
| schedule_expression | Optional rate() or cron() expression to schedule the Lambda function at regular intervals | string | `rate(1 hour)` | no |
| stage | Stage, e.g. 'prod', 'staging', 'dev', or 'test' | string | `prod` | no |


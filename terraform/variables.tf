variable "stage" {
  default = "prod"
  description = "Stage, e.g. 'prod', 'staging', 'dev', or 'test'"
}

variable "enabled" {
  default = true
  description = "If true, schedule_expression will be applied"
}

variable "schedule_expression" {
  default     = "rate(1 hour)"
  description = "Optional rate() or cron() expression to schedule the Lambda function at regular intervals"
}

variable "regions" {
  default = ""
  description = "Regions in which lambda-curator is enabled, split by comma or space,leave it blank as all regions enabled"
}
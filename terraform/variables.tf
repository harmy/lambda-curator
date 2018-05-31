variable "stage" {
  default = ""
}

variable "enabled" {
  default = true
}

variable "schedule_expression" {
  default     = "rate(1 minute)"
  description = "Optional rate() or cron() expression to schedule the Lambda function at regular intervals"
}
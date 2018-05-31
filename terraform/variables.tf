variable "stage" {
  default = "prod"
}

variable "enabled" {
  default = true
}

variable "schedule_expression" {
  default     = "rate(1 hour)"
  description = "Optional rate() or cron() expression to schedule the Lambda function at regular intervals"
}
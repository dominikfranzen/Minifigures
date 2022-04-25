variable "daily_minifigures_trigger" {
  default     = "cron(45 18 * * ? *)"
  description = "the aws cloudwatch event rule schedule expression that specifies when the scheduler runs. Default is 5 minuts past the hour. for debugging use 'rate(5 minutes)'. See https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html"
}

variable "daily_minifigure_parts_trigger" {
  default     = "cron(0 19 * * ? *)"
  description = "the aws cloudwatch event rule schedule expression that specifies when the scheduler runs. Default is 5 minuts past the hour. for debugging use 'rate(5 minutes)'. See https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html"
}

variable "daily_part_prices_trigger" {
  default     = "cron(15 19 * * ? *)"
  description = "the aws cloudwatch event rule schedule expression that specifies when the scheduler runs. Default is 5 minuts past the hour. for debugging use 'rate(5 minutes)'. See https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html"
}

resource "aws_cloudwatch_event_rule" "daily_exec_minifigure_prices" {
    name = "daily"
    description = "Fires daily"
    schedule_expression = var.daily_minifigures_trigger
}

resource "aws_cloudwatch_event_rule" "daily_exec_minifigure_parts" {
    name = "daily"
    description = "Fires daily"
    schedule_expression = var.daily_minifigure_parts_trigger
}

resource "aws_cloudwatch_event_rule" "daily_exec_part_prices" {
    name = "daily"
    description = "Fires daily"
    schedule_expression = var.daily_part_prices_trigger
}

resource "aws_cloudwatch_event_target" "save_minifigure_prices_daily" {
    rule = "${aws_cloudwatch_event_rule.daily_exec_minifigure_prices.name}"
    target_id = "save_minifigure_prices"
    arn = "${aws_lambda_function.save_minifigure_prices.arn}"
}

resource "aws_cloudwatch_event_target" "save_minifigure_parts_daily" {
    rule = "${aws_cloudwatch_event_rule.daily_exec_minifigure_parts.name}"
    target_id = "save_minifigure_parts"
    arn = "${aws_lambda_function.save_minifigure_parts.arn}"
}

resource "aws_cloudwatch_event_target" "save_part_prices_daily" {
    rule = "${aws_cloudwatch_event_rule.daily_exec_part_prices.name}"
    target_id = "save_minifigure_prices"
    arn = "${aws_lambda_function.save_part_prices.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_save_minifigure_prices" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.save_minifigure_prices.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.daily_exec_minifigure_prices.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_save_minifigure_parts" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.save_minifigure_parts.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.daily_exec_minifigure_parts.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_save_part_pricess" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.save_part_prices.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.daily_exec_part_prices.arn}"
}
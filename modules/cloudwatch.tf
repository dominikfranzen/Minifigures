resource "aws_cloudwatch_event_rule" "daily_exec_minifigure_prices" {
    name = "daily_exec_minifigure_prices"
    description = "Fires daily"
    schedule_expression = "cron(30 11 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "daily_exec_minifigure_parts" {
    name = "daily_exec_minifigure_parts"
    description = "Fires daily"
    schedule_expression = "cron(45 11 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "daily_exec_part_prices" {
    name = "daily_exec_part_prices"
    description = "Fires daily"
    schedule_expression = "cron(0 12 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "daily_exec_profit_calc" {
    name = "daily_exec_profit_calc"
    description = "Fires daily"
    schedule_expression = "cron(15 12 * * ? *)"
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

resource "aws_cloudwatch_event_target" "profit_calc_daily" {
    rule = "${aws_cloudwatch_event_rule.daily_exec_profit_calc.name}"
    target_id = "save_minifigure_prices"
    arn = "${aws_lambda_function.profit_calc.arn}"
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

resource "aws_lambda_permission" "allow_cloudwatch_to_call_profit_calc" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.profit_calc.function_name}"
    principal = "events.amazonaws.com"
    source_arn = "${aws_cloudwatch_event_rule.daily_exec_profit_calc.arn}"
}
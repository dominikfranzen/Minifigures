resource "aws_iam_role" "lambda-iam-role" {
    name = "lambda-iam-role"
    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com"
                ]
            }
        }
    ]
}
EOF
}

resource "aws_iam_role_policy" "lambda-iam-role-policy" {
  name = "lambda-iam-role-policy"
  role = "${aws_iam_role.lambda-iam-role.id}"
  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_lambda_function" "save_minifigure_prices" {
  filename      = "lambda-package-minifigures.zip"
  function_name = "save_minifigure_prices"
  role          = aws_iam_role.lambda-iam-role.arn
  handler       = "lambda_save_minifigure_prices.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("lambda-package-minifigures.zip")

  runtime = "python3.9"
}

resource "aws_lambda_function" "save_minifigure_parts" {
  filename      = "lambda-package-minifigure-parts.zip"
  function_name = "save_minifigure_parts"
  role          = aws_iam_role.lambda-iam-role.arn
  handler       = "lambda_save_parts.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("lambda-package-minifigure-parts.zip")

  runtime = "python3.9"
}

resource "aws_lambda_function" "save_part_prices" {
  filename      = "lambda-package-part-prices.zip"
  function_name = "save_part_prices"
  role          = aws_iam_role.lambda-iam-role.arn
  handler       = "lambda_save_part_prices.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("lambda-package-part-prices.zip")

  runtime = "python3.9"
}

resource "aws_lambda_function" "profit_calc" {
  filename      = "lambda-package-profit-calculation.zip"
  function_name = "profit_calc"
  role          = aws_iam_role.lambda-iam-role.arn
  handler       = "lambda_profit_calculation.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("lambda-package-profit-calculation.zip")

  runtime = "python3.9"
}
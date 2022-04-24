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

resource "aws_lambda_function" "save_minifigure_prices" {
  filename      = "lambda-package-minifigures.zip"
  function_name = "save_minifigure_prices"
  role          = aws_iam_role.lambda-iam-role.arn
  handler       = "lambda_save_minifigure_prices.lambda_handler"
  memory_size = 512
  timeout = 900
  source_code_hash = filebase64sha256("lambda-package-minifigures.zip")

  runtime = "python3.9"
  
#  environment {
#    variables = {
#      WEATHER_TABLE_NAME = var.weather_table_name
#    }
#  }
}


#output "write_to_dynamodb_lambda" {
#  value = aws_lambda_function.write_to_dynamo
#}
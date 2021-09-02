terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.56.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.2.0"
    }
  }

  required_version = "~> 1.0"
}

provider "aws" {
  region = var.aws_region
}

locals {
  project_root = "${path.module}/.."
  out_dir = "${local.project_root}/out"
}

# Define a Lambda, using the S3 object setup in code_assets.tf, and the IAM role setup in execution_role.tf
resource "aws_lambda_function" "lambda_function" {
  function_name = "DCA_CoinbasePro"

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = aws_s3_bucket_object.lambda_code_bucket.key
  source_code_hash = filesha256("${local.out_dir}/package.zip")

  runtime = "python3.9"
  handler = "src.main.handler"

  role = aws_iam_role.lambda_execution_role.arn

  timeout = 120
  memory_size = 128

  environment {
    variables = {
      CREDENTIALS_SECRET_NAME = aws_secretsmanager_secret.credentials.arn
      CONFIG_SECRET_NAME = aws_secretsmanager_secret.config.arn
      PRODUCTION = "YES_PLEASE"
    }
  }
}

# Define a log group
resource "aws_cloudwatch_log_group" "lambda_function_log_group" {
  name = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
  retention_in_days = 60
}

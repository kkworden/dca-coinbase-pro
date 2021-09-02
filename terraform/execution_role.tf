# This file defines IAM role resources to be used for the Lambda execution role

# Trust document so Lambda can use the execution role
data "aws_iam_policy_document" "trust_policy" {
  statement {
    actions    = ["sts:AssumeRole"]
    effect     = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# The Lambda execution role
resource "aws_iam_role" "lambda_execution_role" {
  name               = "DCA_CoinbasePro_Execution_role"
  assume_role_policy = "${data.aws_iam_policy_document.trust_policy.json}"
}

# Attaches a basic Lambda policy needed for the execution role
resource "aws_iam_role_policy_attachment" "basic_execution_role_policy" {
  role       = "${aws_iam_role.lambda_execution_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# A policy that allows access to Secrets manager
resource "aws_iam_role_policy" "secrets_manager_policy" {
  role   = "${aws_iam_role.lambda_execution_role.name}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action   = ["secretsmanager:GetSecretValue"]
      Effect   = "Allow"
      Resource = [
        aws_secretsmanager_secret.credentials.arn,
        aws_secretsmanager_secret.config.arn
      ]
    }]
  })
}
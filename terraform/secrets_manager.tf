# This file copies configuration into AWS Secrets Manager for use by the Lambda function

# Used for bucket naming
resource "random_string" "secret_suffix" {
  length  = 14
  special = false
  upper   = false
}

resource "aws_secretsmanager_secret" "credentials" {
  name = "credentials-${random_string.secret_suffix.id}"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "credentials_secret" {
  secret_id     = aws_secretsmanager_secret.credentials.id
  secret_string = file("${path.module}/../config/prod_creds.json")
}

resource "aws_secretsmanager_secret" "config" {
  name = "config-${random_string.secret_suffix.id}"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "config_secret" {
  secret_id     = aws_secretsmanager_secret.config.id
  secret_string = file("${path.module}/../config/prod.json")
}
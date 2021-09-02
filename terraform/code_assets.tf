# Used for bucket naming
resource "random_string" "lambda_bucket_name" {
  length  = 14
  special = false
  upper   = false
}

# Bucket to hold the Lambda code
resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "dca-cbpro-${random_string.lambda_bucket_name.id}"

  acl           = "private"
  force_destroy = true
}

# Package code using shell script
resource "null_resource" "package_lambda" {

  # We should always package the code
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command     = "./bin/packageforlambda.sh"
    working_dir = local.project_root
  }
}

# Upload our ZIP archive into the S3 bucket
resource "aws_s3_bucket_object" "lambda_code_bucket" {
  bucket = aws_s3_bucket.lambda_bucket.id

  key    = "package.zip"
  source = "${local.out_dir}/package.zip"

  depends_on = [null_resource.package_lambda]

  etag = filemd5("${local.out_dir}/package.zip")
}
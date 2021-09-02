output "bucketname" {
  value = "dca-cbpro-${random_string.lambda_bucket_name.id}"
}
resource "aws_s3_bucket" "lawson" {
  bucket = "arimo-panasonic-ap-cn-lawson"

  tags = {
    Project     = "CN-Lawson"
    Name        = "CN-Lawson-S3"
    Cluster     = "CN-Lawson-S3-STG"
    Environment = "STG"
  }
}
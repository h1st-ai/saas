terraform {
  backend "s3" {
    bucket  = "arimo-infrastructure"
    key     = "terraform/h1st/terraform.tfstate"
    region  = "us-east-1"
  }
}

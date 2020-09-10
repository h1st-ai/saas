terraform {
  backend "s3" {
    bucket  = "arimo-infrastructure"
    key     = "terraform/h1st/terraform.tfstate"
    region  = "us-east-1"
  }
}

provider "aws" {
  version = "~> 3.0"
  region  = "us-west-1"
}

provider "template" {
  
}

# allow access to PROD RDS
data "aws_security_group" "infra_rds" {
  id = "sg-0c79b76a99b9bc595"
}

terraform {
  backend "s3" {
    bucket  = "aitomatic-infrastructure"
    key     = "terraform/h1st/staging.tfstate"
    region  = "us-east-1"
  }
}

provider "aws" {
  region  = "us-west-1"
}

provider "template" {}

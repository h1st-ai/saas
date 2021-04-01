terraform {
  backend "s3" {
    bucket  = "infrastructure"
    key     = "terraform/h1st/staging.tfstate"
    region  = "cn-northwest-1"
  }
}

provider "aws" {
  region  = "cn-northwest-1"
}

provider "template" {}

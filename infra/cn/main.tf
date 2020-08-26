terraform {
  backend "s3" {
    bucket  = "arimo-infrastructure"
    key     = "terraform/h1st/staging.tfstate"
    region  = "cn-northwest-1"
  }
}

provider "aws" {
  region  = "cn-northwest-1"
}

provider "template" {}

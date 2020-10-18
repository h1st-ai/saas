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

variable "environment_tag" {
  default = "PROD"
}

variable "project_tag" {
  default = "H1st"
}

terraform {
  backend "s3" {
    bucket  = "arimo-infrastructure"
    key     = "terraform/h1st/staging.tfstate"
    region  = "us-east-1"
  }
}

provider "aws" {
  version = "~> 3.0"
  region  = "us-west-1"
}

provider "template" {
  
}

variable "ecs_cluster" {
  default = "H1st-staging"
}

variable "environment_tag" {
  default = "STAGING"
}

variable "project_tag" {
  default = "H1st"
}

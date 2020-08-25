provider "aws" {
  version = "~> 3.0"
  region  = "us-west-1"
}

data "aws_vpc" "vpc" {
  id = "vpc-008a670427932b3b7"
}

data "aws_subnet" "public_1a" {
  id = "subnet-011f013cad6710f69"
}

data "aws_subnet" "public_1b" {
  id = "subnet-02582523dabdce1f3"
}

data "aws_security_group" "infra_efs" {
  id = "sg-0158cfd1e78fb4eb0"
}

data "aws_efs_file_system" "main" {
  file_system_id = "fs-bfdaf7a6"
}

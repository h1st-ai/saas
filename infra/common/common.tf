# common infrastructure setup

data "aws_vpc" "vpc" {
  id = "vpc-008a670427932b3b7"
}

data "aws_subnet" "public_1a" {
  id = "subnet-011f013cad6710f69"
}

data "aws_subnet" "public_1b" {
  id = "subnet-02582523dabdce1f3"
}

data "aws_efs_file_system" "main" {
  file_system_id = "fs-bfdaf7a6"
}

# allow to connect to efs
data "aws_security_group" "infra_efs" {
  id = "sg-0158cfd1e78fb4eb0"
}

# allow web access
data "aws_security_group" "infra_web" {
  id = "sg-01f3b408dd73fd7de"
}

data "aws_security_group" "infra_gateway" {
  id = "sg-0dfdbe4bf39efaa86"
}

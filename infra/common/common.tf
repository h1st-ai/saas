# common infrastructure setup

data "aws_vpc" "vpc" {
  id = "vpc-008a670427932b3b7"
}

data "aws_subnet" "public_1a" {
  id = "subnet-011f013cad6710f69"
}

data "aws_subnet" "nat_1a" {
  id = "subnet-05328d842dd3de7b9"
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

# allow access to RDS
data "aws_security_group" "infra_rds" {
  id = "sg-0c79b76a99b9bc595"
}

data "aws_security_group" "infra_gateway" {
  id = "sg-0dfdbe4bf39efaa86"
}

variable "lb_https_listener" {
  default = "arn:aws:elasticloadbalancing:us-west-1:394497726199:listener/app/h1st-lb/08becaddc92dc8c6/3d6c032b3f32f2b7"
}

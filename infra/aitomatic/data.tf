# common infrastructure setup
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_vpc" "vpc" {
  id = "vpc-1aec397c"
}

data "aws_subnet_ids" "subnets" {
  vpc_id = data.aws_vpc.vpc.id
}

data "aws_subnet" "public_1a" {
  id = "subnet-317ffb57"
}

//data "aws_subnet" "public_1b" {
//  id = "subnet-022eb964"
//}

data "aws_subnet" "public_1c" {
  id = "subnet-afee3ef5"
}

data "aws_efs_file_system" "main" {
  file_system_id = aws_efs_file_system.h1st.id
}

# allow to connect to efs
data "aws_security_group" "infra_efs" {
  id = aws_security_group.infra_efs.id
}

# allow web access
data "aws_security_group" "infra_web" {
  id = aws_security_group.infra_web.id
}

# allow access to RDS
data "aws_security_group" "infra_rds" {
  id = aws_security_group.infra_rds.id
}

data "aws_security_group" "infra_gateway" {
  id = aws_security_group.infra_gateway.id
}

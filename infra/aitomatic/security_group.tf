resource "aws_security_group" "infra_efs" {
  name        = "infra_efs"
  description = "Infra EFS"
  vpc_id      = data.aws_vpc.vpc.id

  tags = {
    Project = "INFRA"
  }
}

resource "aws_security_group" "infra_web" {
  name        = "infra_web"
  description = "Infra Web"
  vpc_id      = data.aws_vpc.vpc.id

  tags = {
    Project = "INFRA"
  }
}

resource "aws_security_group" "infra_rds" {
  name        = "infra_rds"
  description = "Infra RDS"
  vpc_id      = data.aws_vpc.vpc.id

  tags = {
    Project = "INFRA"
  }
}

resource "aws_security_group" "infra_gateway" {
  name        = "infra_gateway"
  description = "Infra Gateway"
  vpc_id      = data.aws_vpc.vpc.id

  tags = {
    Project = "INFRA"
  }
}

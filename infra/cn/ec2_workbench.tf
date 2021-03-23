resource "aws_security_group" "workbench" {
  name        = "workbench"
  description = "Workbench"
  vpc_id      = data.aws_vpc.vpc.id

  tags = {
    Environment   = var.environment_tag
    Project       = var.project_tag
    Name          = "Workbench"
  }
}

resource "aws_network_interface" "workbench" {
  subnet_id = data.aws_subnet.public_1a.id
  security_groups = [
    data.aws_security_group.infra_gateway.id,
    data.aws_security_group.infra_web.id,
    data.aws_security_group.infra_rds.id,
    aws_security_group.workbench.id,
  ]

  tags = {
    Environment   = var.environment_tag
    Project       = var.project_tag
    Name          = "Workbench ENI"
  }
}

resource "aws_instance" "workbench-dashboard" {
  ami           = "ami-0a22b8776bb32836b"
  instance_type = "t3.large"

  key_name  = "an"

  network_interface {
    network_interface_id = aws_network_interface.workbench.id
    device_index = 0
  }

  tags = {
    Environment   = var.environment_tag
    Project       = var.project_tag
    Name          = "Workbench Dashboard"
  }
}

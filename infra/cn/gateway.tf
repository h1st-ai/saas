resource "aws_security_group" "gateway" {
  name        = "gateway-staging"
  description = "Gateway Staging"
  vpc_id      = data.aws_vpc.vpc.id

  tags = {
    Name = "Gateway Staging"
  }
}

resource "aws_security_group" "gateway_access" {
  name        = "gateway-staging-access"
  description = "Gateway Staging Access"
  vpc_id      = data.aws_vpc.vpc.id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    security_groups = [aws_security_group.gateway.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Allow access from Gateway Staging"
  }
}

resource "aws_network_interface" "gateway" {
  subnet_id = data.aws_subnet.public_1a.id
  security_groups = [
    data.aws_security_group.infra_gateway.id,
    data.aws_security_group.infra_web.id,
    data.aws_security_group.infra_rds.id,
    aws_security_group.gateway.id,
  ]

  # source_dest_check      = false

  tags = {
    Environment   = var.environment_tag
    Project       = var.project_tag
    Name          = "Gateway ENI"
  }
}

resource "aws_instance" "gateway" {
  ami           = "ami-0a22b8776bb32836b"
  instance_type = "t3.large"

  key_name  = "an"

  network_interface {
    network_interface_id = aws_network_interface.gateway.id
    device_index = 0
  }

  root_block_device {
    volume_size = "128"
    volume_type = "gp2"
  }

  tags = {
    Environment   = var.environment_tag
    Project       = var.project_tag
    Name          = "Gateway - ${var.environment_tag}"

    # always-on     = "true"
  }
}

resource "aws_lb_target_group" "gateway" {
  name     = "h1st-gateway-${var.environment_tag}"
  port     = 80
  protocol = "HTTP"
  vpc_id   = data.aws_vpc.vpc.id
}

resource "aws_lb_target_group_attachment" "gateway" {
  target_group_arn = aws_lb_target_group.gateway.arn
  target_id        = aws_instance.gateway.id
}

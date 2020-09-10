resource "aws_network_interface" "gateway" {
  subnet_id = data.aws_subnet.public_1a.id
  security_groups = [
    data.aws_security_group.infra_gateway.id,
    data.aws_security_group.infra_web.id,
  ]

  # source_dest_check      = false

  tags = {
    Environment   = "${var.environment_tag}"
    Project       = "${var.project_tag}"
    Name          = "Gateway ENI"
  }
}

resource "aws_instance" "gateway" {
  ami           = "ami-0dd005d3eb03f66e8"
  instance_type = "t3.large"

  key_name  = "bao"

  network_interface {
    network_interface_id = "${aws_network_interface.gateway.id}"
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

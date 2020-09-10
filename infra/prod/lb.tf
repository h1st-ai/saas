resource "aws_lb" "lb" {
  name         = "h1st-lb"
  internal     = false
  idle_timeout = 3600

  security_groups = [
    data.aws_security_group.infra_web.id,
  ]

  # This has to be in public subnets
  subnets = [
    data.aws_subnet.public_1a.id,
    data.aws_subnet.public_1b.id,
  ]

  tags = {
    Name        = "H1st LB"
    Environment = "PROD"
    Project     = "H1st"
  }
}

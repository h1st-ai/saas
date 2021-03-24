resource "aws_elb" "h1st" {
  name               = "h1st"
  availability_zones = [
    "us-west-1a",
    "us-west-1c",
  ]

  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }

//  listener {
//    instance_port     = 443
//    instance_protocol = "https"
//    lb_port           = 443
//    lb_protocol       = "https"
//  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    target              = "HTTP:80/"
    interval            = 30
  }

  instances = [aws_instance.gateway.id]
  cross_zone_load_balancing   = true
  idle_timeout                = 400
  connection_draining         = true
  connection_draining_timeout = 400

  tags = {
    Project = "H1st"
  }
}
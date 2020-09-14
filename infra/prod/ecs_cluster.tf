data "aws_ami" "ecs_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn-ami-*-amazon-ecs-optimized"]
  }
}

data "template_file" "worker_init" {
  template = "${file("${path.module}/ecs_userdata.txt")}"

  vars = {
    cluster = "H1st"
  }
}

data "aws_iam_policy_document" "ecs_instance_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_instance_role" {
  name               = "ecs-instance-role-h1st"
  assume_role_policy = data.aws_iam_policy_document.ecs_instance_assume_role_policy.json
}

resource "aws_iam_role_policy_attachment" "ecs_instance_role_policy" {
  role       = aws_iam_role.ecs_instance_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecsInstanceRole-h1st"
  path = "/"
  role = aws_iam_role.ecs_instance_role.name
}

resource "aws_launch_configuration" "ecs_as_conf" {
  name_prefix = "ecs_as_"

  image_id      = data.aws_ami.ecs_ami.id
  instance_type = "c5.2xlarge"

  iam_instance_profile = aws_iam_instance_profile.ecs_instance_profile.name
  associate_public_ip_address = false

  security_groups = [
    data.aws_security_group.infra_efs.id,
    data.aws_security_group.infra_gateway.id,
    data.aws_security_group.infra_web.id,
    data.aws_security_group.infra_rds.id,
  ]

  key_name  = "bao"
  user_data = data.template_file.worker_init.rendered

  root_block_device {
    volume_size = 64
    volume_type = "gp2"
  }

  ebs_block_device {
    device_name = "/dev/xvdcz"
    volume_type = "gp2"
    volume_size = 128
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "ecs" {
  name = "ecs-h1st"

  launch_configuration = aws_launch_configuration.ecs_as_conf.id
  termination_policies = ["OldestLaunchConfiguration", "Default"]
  vpc_zone_identifier  = [
    "subnet-05328d842dd3de7b9",  # nat 1a
    "subnet-0d0ea9d85743f0ef6",  # nat 1b
  ]

  protect_from_scale_in = true

  desired_capacity = 1
  max_size         = 10
  min_size         = 3

  lifecycle {
    create_before_destroy = true
    ignore_changes = [
      desired_capacity
    ]
  }

  tag {
    key                 = "Name"
    value               = "ecs-h1st"
    propagate_at_launch = true
  }

  tag {
    key                 = "Project"
    value               = "H1st"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = "PROD"
    propagate_at_launch = true
  }

  tag {
    key                 = "Automation"
    value               = "Terraform"
    propagate_at_launch = true
  }
}

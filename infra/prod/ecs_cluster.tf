locals {
  instance_role = "ecsInstanceRole-h1st" # TODO: do we need different role for staging?
}


data "aws_ami" "ecs_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-2.0.*-x86_64-ebs"]
  }
}

data "template_file" "worker_init" {
  template = "${file("${path.module}/ecs_userdata.txt")}"

  vars = {
    cluster = "H1st"
  }
}

resource "aws_launch_template" "ecs_as_lt" {
  name_prefix = "h1st_"

  update_default_version = true

  block_device_mappings {
    device_name = "/dev/xvda"

    ebs {
      volume_size = 256
    }
  }

  # ebs_optimized = true
  iam_instance_profile { name = local.instance_role }
  image_id = data.aws_ami.ecs_ami.id
  instance_type = "c5.2xlarge"
  key_name = "bao"

  monitoring {
    enabled = true
  }

  vpc_security_group_ids = [
    data.aws_security_group.infra_efs.id,
    data.aws_security_group.infra_gateway.id,
    data.aws_security_group.infra_web.id,
    # data.aws_security_group.infra_rds.id,
  ]

  tag_specifications {
    resource_type = "instance"

    tags = {
      Project = var.project_tag
      Name = "ecs-h1st"
      Environment = var.environment_tag
    }
  }

  user_data = base64encode(data.template_file.worker_init.rendered)
}

resource "aws_autoscaling_group" "ecs" {
  name = "ecs-h1st"

  launch_template {
    id      = aws_launch_template.ecs_as_lt.id
    version = "$Latest"
  }
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

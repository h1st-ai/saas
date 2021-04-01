resource "aws_iam_instance_profile" "h1st_profile" {
  name = "ecsInstanceRole-h1st_profile"
  role = "ecs-instance-role-h1st"
}

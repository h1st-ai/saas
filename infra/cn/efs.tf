resource "aws_efs_file_system" "h1st" {
  creation_token = "h1st"

  tags = {
    Name = "H1st"
  }
}
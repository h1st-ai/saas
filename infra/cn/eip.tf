resource "aws_eip" "workbench" {
  instance = aws_instance.workbench-dashboard.id
  vpc      = true
}

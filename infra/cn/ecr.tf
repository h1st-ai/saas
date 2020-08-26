resource "aws_ecr_repository" "workbench" {
  name = "workbench"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags  = var.tags
}

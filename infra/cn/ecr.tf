resource "aws_ecr_repository" "workbench" {
  name = "workbench"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags  = var.tags
}

resource "aws_ecr_repository" "workbench-dashboard" {
  name = "workbench-dashboard"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags  = var.tags
}

resource "aws_ecr_repository" "workbench-controller" {
  name = "workbench-controller"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags  = var.tags
}

resource "aws_ecr_repository" "keycloak" {
  name = "keycloak"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags  = var.tags
}

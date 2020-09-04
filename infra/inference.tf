resource "aws_ecs_task_definition" "inference" {
  family                = "inference"
  container_definitions = file("./inference.json")

  volume {
    name = "efs"

    efs_volume_configuration {
      file_system_id = "fs-bfdaf7a6"
      root_directory = "/"
    }
  }
}

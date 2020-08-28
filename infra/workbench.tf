resource "aws_ecs_task_definition" "workbench" {
  family                = "workbench"
  container_definitions = file("./workbench.json")

  volume {
    name = "efs"

    efs_volume_configuration {
      file_system_id = "fs-bfdaf7a6"
      root_directory = "/"
    }
  }
}

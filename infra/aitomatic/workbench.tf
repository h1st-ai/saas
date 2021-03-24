resource "aws_ecs_task_definition" "workbench" {
  family                = "workbench-staging"
  container_definitions = file("./workbench.json")

  volume {
    name = "efs"

    efs_volume_configuration {
      file_system_id = aws_efs_file_system.h1st.id
      root_directory = "/"
    }
  }
}

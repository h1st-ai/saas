resource "aws_ecs_task_definition" "keycloak" {
  family                = "keycloak"
  container_definitions = file("./keycloak.json")

#   volume {
#     name = "service-storage"

#     docker_volume_configuration {
#       scope         = "shared"
#       autoprovision = true
#       driver        = "local"

#       driver_opts = {
#         "type"   = "nfs"
#         "device" = "${aws_efs_file_system.fs.dns_name}:/"
#         "o"      = "addr=${aws_efs_file_system.fs.dns_name},rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport"
#       }
#     }
#   }
}

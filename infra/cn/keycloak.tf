resource "aws_ecs_task_definition" "keycloak" {
  family                = "keycloak"
  container_definitions = file("./keycloak.json")
}

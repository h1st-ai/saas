resource "aws_db_instance" "h1st" {
  identifier           = "h1st"
  allocated_storage    = 32
  storage_type         = "gp2"
  engine               = "postgres"
  instance_class       = "db.t3.large"
  name                 = "keycloak"
  username             = "keycloak"
  password             = "keycloakrds"
}

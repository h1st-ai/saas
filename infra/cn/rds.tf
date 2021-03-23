resource "aws_db_instance" "h1st" {
  identifier           = "h1st"
  allocated_storage    = 32
  storage_type         = "gp2"
  engine               = "postgres"
  instance_class       = "db.t3.large"
  name                 = "postgres"
  username             = "postgres"
  password             = "arimoiscool"

  vpc_security_group_ids = [
    aws_security_group.infra_rds.id
  ]
}

resource "aws_dynamodb_table" "h1st_saas_workbench_staging" {
  name           = "H1st_saas_workbench_staging"
  billing_mode   = "PROVISIONED"
  read_capacity  = 3
  write_capacity = 3
  hash_key       = "user_id"
  range_key      = "workbench_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "workbench_id"
    type = "S"
  }

  attribute {
    name = "task_arn"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  global_secondary_index {
    name               = "workbench-index"
    hash_key           = "workbench_id"
    write_capacity     = 3
    read_capacity      = 3
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "status-task_arn-index"
    hash_key           = "status"
    range_key          = "task_arn"
    write_capacity     = 3
    read_capacity      = 3
    projection_type    = "KEYS_ONLY"
  }

  tags = {
    Project     = "H1st"
    Name        = "H1st-DynamoDB"
    Cluster     = "H1st-DynamoDB-STG"
    Environment = "STG"
  }
}

resource "aws_dynamodb_table" "h1st_saas_workbench_sharing_staging" {
  name           = "h1st_saas_workbench_sharing_staging"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "user_id"
  range_key      = "workbench_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "workbench_id"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  global_secondary_index {
    name               = "workbench-index"
    hash_key           = "workbench_id"
    write_capacity     = 1
    read_capacity      = 1
    projection_type    = "ALL"
  }

  tags = {
    Project     = "H1st"
    Name        = "H1st-DynamoDB"
    Cluster     = "H1st-DynamoDB-STG"
    Environment = "STG"
  }
}

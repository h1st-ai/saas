variable "tags" {
  type = object({
    Project     = string
    Name        = string
    Cluster     = string
    Environment = string
  })
  default = {
    Project     = "H1st"
    Name        = "Workbench"
    Cluster     = "Workbench-STG"
    Environment = "STG"
  }
}

variable "ecs_cluster" {
  default = "H1st-staging"
}

variable "environment_tag" {
  default = "STG"
}

variable "project_tag" {
  default = "H1st"
}

resource "aws_ecr_repository" "auth_api" {
  name                 = "auth_api_${var.env}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = local.tags
}

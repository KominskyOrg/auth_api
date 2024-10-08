terraform {
  required_version = ">= 1.5.0"
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.11.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.0.0"
    }
  }

  backend "s3" {}
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = local.tags
  }
}

data "aws_eks_cluster" "cluster" {
  name = data.terraform_remote_state.infrastructure.outputs.eks_cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = data.terraform_remote_state.infrastructure.outputs.eks_cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

data "terraform_remote_state" "infrastructure" {
  backend = "s3"
  config = {
    bucket         = "tf-statelock"
    key            = "kom_aws_tf.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-table"
  }
}

module "eks" {
  source           = "git::https://github.com/KominskyOrg/kom_tf_modules.git//eks?ref=v1.6"
  eks_service_name = "${local.stack_name}-${local.microservice_type}"
  env              = local.env
  ecr_url          = aws_ecr_repository.app_ecr.repository_url
  image_tag        = var.image_tag
  node_selector = {
    role = local.node_selector
  }
  service_port        = 8080
  service_target_port = 5000
  env_vars = {
    AUTH_SERVICE_URL = "https://${local.stack_name}-service.${var.env}.svc.cluster.local:8080"
    FLASK_ENV        = local.env
  }
  readiness_probe_path = "/health"
  liveness_probe_path  = "/health"
}

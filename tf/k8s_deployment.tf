resource "kubernetes_deployment" "auth_api" {
  metadata {
    name      = "auth_api"
    namespace = var.env
    labels = {
      app = "auth_api"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "auth_api"
      }
    }

    template {
      metadata {
        labels = {
          app = "auth_api"
        }
      }

      spec {
        container {
          name  = "auth_api"
          image = "your-account-id.dkr.ecr.your-region.amazonaws.com/auth_api:latest"

          port {
            container_port = 5000
          }

          env_from {
            secret_ref {
              name = kubernetes_secret.db_credentials.metadata[0].name
            }
          }
        }
      }
    }
  }
}
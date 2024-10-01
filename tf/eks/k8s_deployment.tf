resource "kubernetes_deployment" "auth_api" {
  metadata {
    name      = "auth-api"
    namespace = var.env
    labels = {
      app = "auth-api"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "auth-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "auth-api"
        }
      }

      spec {
        node_selector = {
          role = "backend"
        }

        container {
          name  = "auth-api"
          image = "${var.auth_api_ecr_url}:${var.image_tag}"

          port {
            container_port = 5000
          }

          env {
            name = "FLASK_ENV"
            value = var.env
          }

          env {
            name = "AUTH_SERVICE_URL"
            value = "https://${var.env}.jaredkominsky.com/service/auth"
          }

          liveness_probe {
            http_get {
              path = "/api/auth/health"
              port = 5000
            }
            initial_delay_seconds = 30
            period_seconds        = 10
            timeout_seconds       = 5
            failure_threshold     = 3
          }

          readiness_probe {
            http_get {
              path = "/api/auth/health"
              port = 5000
            }
            initial_delay_seconds = 5
            period_seconds        = 10
            timeout_seconds       = 5
            failure_threshold     = 3
          }
        }
      }
    }
  }
}

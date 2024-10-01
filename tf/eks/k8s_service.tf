resource "kubernetes_service" "auth_api" {
  metadata {
    name      = "auth-api"
    namespace = var.env
  }

  spec {
    selector = {
      app = "auth-api"
    }

    port {
      port        = 8080
      target_port = 5000
    }

    type = "ClusterIP"
  }
}
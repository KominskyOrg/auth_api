resource "kubernetes_service" "auth_api" {
  metadata {
    name      = "auth_api"
    namespace = kubernetes_namespace.auth.metadata[0].name
  }

  spec {
    selector = {
      app = "auth_api"
    }

    port {
      port        = 443
      target_port = 5000
    }

    type = "ClusterIP"
  }
}
# Configuration for Prometheus URL, Grafana URL, Applications and directories for outputs and templates under the Config Class
class Config:
    # Prometheus URL and Grafana URL Cluster Routes, and the Prometheus Authentication Token to extract the data 
    PROMETHEUS_URL = "https://prometheus-k8s-openshift-monitoring.apps.infomed.foma.p1.openshiftapps.com/api"
    GRAFANA_URL = "https://grafana-info-mediator-route-info-mediator-monitoring.apps.infomed.foma.p1.openshiftapps.com/d/bad7784b-3776-46b2-a518-7980e2973335/jvm-quarkus-micrometer-metrics?orgId=1&refresh=10s"
    PROMETHEUS_TOKEN = "sha256~3TFSILl1BFqPsyMv8zmYIk8XhUN3O29-mcHoMxK_3SA"

    # Applications to monitor and their respective dashboards
    APPLICATIONS = ["birth-api","driving-license-api"]

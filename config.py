# Configuration for Prometheus URL, Grafana URL, Applications and directories for outputs and templates under the Config Class
class Config:
    # Prometheus URL and Grafana URL Cluster Routes
    PROMETHEUS_URL = "https://prometheus-k8s-openshift-monitoring.apps.infomed.foma.p1.openshiftapps.com/api"
    GRAFANA_URL = "https://grafana-info-mediator-route-info-mediator-monitoring.apps.infomed.foma.p1.openshiftapps.com"

    # Applications to monitor and their respective dashboards
    APPLICATIONS = ["birth-api","driving-license-api"]

    # Output Directories
    OUTPUT_DIR = 'outputs/'
    TEMPLATE_DIR = 'templates/'

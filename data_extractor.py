# Import the necessary libraries for interacting with Prometheus and handling data
from datetime import datetime, timedelta
# Import the requestd library to communicate with apis in the cluster
import requests
# Import the Config class from the config.py file
from config import Config


# Define a class to retrieve data from Prometheus
class DataExtractor:
  # Initialise the class with the Prometheus URL and the output directory
  def __init__(self):
    # Initialiase the Prometheus URL, Grafana URL and Token from config
    self.prometheusUrl = Config.PROMETHEUS_URL
    self.grafanaUrl = Config.GRAFANA_URL
    self.token = Config.PROMETHEUS_TOKEN

  # function to fetch the prometheus data
  def fetchPrometheusData(self, query):
    headers = {
      "Authorization": f"Bearer {self.token}"
    }
    response = requests.get(f"{self.prometheusUrl}/v1/query", params={"query":query}, headers=headers)
    response.raise_for_status()
    return response.json()["data"]["result"]
  
  # function to get metrics from Grafana
  def getMetrics(self, startDate, endDate, application):
    # Initalisining metrics collection
    metrics = {}

    # Fetching Uptime of api application (in Hours/Days/Month/Years)
    uptimeQuery = (
            'process_uptime_seconds{container="driving-license-api", endpoint="8080", instance="10.128.2.92:8080", '
            'job="driving-license-api", namespace="info-mediator-uat", pod="driving-license-api-87bf69c7-mwwr6", '
            'prometheus="openshift-user-workload-monitoring/user-workload", service="driving-license-api"}'
        )
    # Fetching Uptime result
    uptimeResult = self.fetchPrometheusData(uptimeQuery)
    # Checking if uptime data is available and extracting it if available
    if uptimeResult:
      # Fetching how long application has been running
      uptimeSeconds = float(uptimeResult[0]["value"][1])
      # Extracting Uptime in hours
      metrics["uptime_hours"] = uptimeSeconds / 3600 # converts seconds to hours
    else:
      metrics["uptime_hours"] = "N/A"

    # Start time
    if uptimeResult:
      # Reseting uptimeSeconds
      uptimeSeconds = float(uptimeResult[0]["value"][1])
      startTime = datetime.now() - timedelta(seconds=uptimeSeconds)
      metrics["start_time"] = startTime.strptime('%Y-%m-%d %H:%M:%S')
    else:
      metrics["start_time"] = "N/A"

    # Fetching Heap Used Percentage
    heapUsedQuery = {
      'sum(jvm_memory_used_bytes{container="driving-license-api", instance="10.128.2.92:8080", area="heap"}) * 100 '
      '/ sum(jvm_memory_max_bytes{container="driving-license-api", instance="10.128.2.92:8080", area="heap"})'
    }
    # Fetching Heap Used Percentage result
    heapUsedResult = self.fetchPrometheusData(heapUsedQuery)
    # Checking if heap used data is available and extracting it if available
    if heapUsedResult:
     # Extracting Heap Used Percentage
     heapUsedPercentage = float(heapUsedResult[0]["value"][1])
     metrics["heap_used_percentage"] = heapUsedPercentage
    else:
      metrics["heap_used_percentage"] = "N/A"

    # Fetching Non Heap Used (Bytes)
    nonHeapUsedQuery = {
      'sum(jvm_memory_used_bytes{container="driving-license-api", instance="10.128.2.92:8080", area="nonheap"}) * 100 '
      '/ sum(jvm_memory_max_bytes{container="driving-license-api", instance="10.128.2.92:8080", area="nonheap"})'
    }
    # Fetching Non Heap Used Result
    nonHeapUsedResult = self.fetchPrometheusData(nonHeapUsedQuery)
    # Checking if non heap used data is available and extracting it if available
    if nonHeapUsedResult:
      nonheapUsedPercentage = float(nonHeapUsedResult[0]["value"][1])
      # Extracting Non Heap Used (Bytes)
      metrics["non_heap_used_percentage"] = nonheapUsedPercentage
    else:
      metrics["non_heap_used_percentage"] = "N/A"

    return metrics
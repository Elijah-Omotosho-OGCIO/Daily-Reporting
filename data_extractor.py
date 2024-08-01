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
    # Initialiase the Prometheus URL from config
    self.prometheusUrl = Config.PROMETHEUS_URL
    self.grafanaUrl = Config.GRAFANA_URL

  # function to fetch the prometheus data
  def fetchPrometheusData(self, query):
    response = requests.get(f"{self.prometheusUrl}/v1/query", params={"query":query})
    response.raise_for_status()
    return response.json()["data"]["result"]
  
  # function to get metrics from Grafana
  def getMetrics(self, startDate, endDate, application):
    # Initalisining metrics collection
    metrics = {}

    # Fetching Uptime of api application (in Hours/Days/Month/Years)
    uptimeQuery = f'avg_over_time({application}_uptime[1h])'

    # Fetching Uptime result
    uptimeResult = self.fetchPrometheusData(uptimeQuery)

    # Extracting Uptime in hours
    metrics["uptime_hours"] = uptimeResult[0]["value"][1]

    # Fetching Start Time of Application
    startTimeQuery = f'{application}_start_time'

    # Fetching Start Time result
    startTimeResult = self.fetchPrometheusData(startTimeQuery)

    # Extracting Start Time
    metrics["start_time"] = datetime.fromtimestamp(float(startTimeResult[0]["value"][1])).strftime('%d-%m-%Y %H:%M:%S')

    # Fetching Heap Used Percentage
    heapUsedQuery = f'{application}_jvm_memory_used{{area="heap"}}'

    # Fetching Heap Used Percentage result
    heapUsedResult = self.fetchPrometheusData(heapUsedQuery)

    # Extracting Heap Used Percentage
    metrics["heap_used"] = heapUsedResult[0]["value"][1]

    # Fetching Non Heap Used (Percentage)
    nonHeapUsedQuery = f'{application}_jvm_memory_used{{area="nonheap"}}'

    # Fetching Non Heap Used Result
    nonHeapUsedQueryResult = self.fetchPrometheusData(nonHeapUsedQuery)

    # Extracting Non Heap Used Percentage
    metrics["non_heap_used"] = nonHeapUsedQueryResult[0]["value"][1]

    return metrics
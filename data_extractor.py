# Import the necessary libraries for interacting with Prometheus and handling data
from datetime import datetime, timedelta

# Import the pandas library for data manipulation and analysis
import pandas as pd
import requests

# Import the configuration settings from the config.py file
import config


# Define a class to retrieve data from Prometheus
class DataExtractor:
  # Initialize the class with the Prometheus URL and the output directory
  def __init__(self):
    # Initialiase the Prometheus URL from config
    self.prometheus_url = config.PROMETHEUS_URL

  # Creating a func to get the data from Prometheus
  def fetchData(self, startTime, endTime, query):
    """
    Fetch data from Prometheus betweem specified start and end time using a query.
    """
    
    # Convert dates to timeStamps for Prometheus sockets
    startTimestamp = int(startTime.timestamp())
    endTimestamp = int(endTime.timestamp())

    # Requesting data from Prometheus Operator
    # Send a GET request to the Prometheus API endpoint for querying data over a range
    response = requests.get(
        f"{self.prometheus_url}/api/v1/query_range",
        params={

            # Specify the Prometheus query to be executed
            "query": query,

            # Set the start time of the query range in Unix timestamp format
            "start": startTimestamp,

            # Set the end time of the query range in Unix timestamp format
            "end": endTimestamp,

            # Define the sampling interval for the data retrieval (1 second in this case)
            "step": "1s"
        })

    """
    Process response and change it into a DataFrame = 'df' using pandas = 'pd'
    """
    # Check if the response status code is OK (200)
    if response.status_code != 200:
      raise Exception(f"Error fetching data from Prometheus: {response.status_code} - {response.text}")

    # Attempt to parse the response as JSON
    try:
      # Extracting the result array from the JSON response
      result = response.json()['data']['result']
    except ValueError as e:
      raise Exception(f"Error decoding JSON response: {e}")

    # Initializing an empty list to store the processed data
    data = []

    # Iterating through each metric in the result array
    for metric in result:

      # Iterating through each data point for the current metric
      for value in metric['values']:
        # Creating a dictionary with timestamp, value, and metric labels, appending to the data list
        data.append({
            'timestamp': value[0],
            'value': float(value[1]),
            **metric['metric']
        })

    # Creating a Pandas DataFrame from the data list
    return pd.DataFrame(data)


if __name__ == "__main__":
  # Example usage of Data Extractor
  extractor = DataExtractor()

  # Get yesterday's date
  startDate = datetime.now() - timedelta(days=1)

  # Get today's date
  endDate = datetime.now()

  # A Prometheus query to sum the rate of HTTP requests over the last minute, grouped by job
  query = 'sum(rate(http_requests_total[1m])) by (job)'

  # Call the fetchData method to get the data
  df = extractor.fetchData(startDate, endDate, query)

  # Print the first 5 rows of the DataFrame
  print(df.head())
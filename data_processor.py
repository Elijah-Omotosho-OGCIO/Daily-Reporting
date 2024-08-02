# Import the datetime package
import datetime

# Function to process data
class DataProcessor:
  def processData(self, rawData):
    processedData = {}
    
    processedData["uptime_hours"] = rawData["uptime_hours"]
    processedData["start_time"] = rawData["start_time"]
    processedData["heap_used"] = rawData["heap_used_percentage"]
    processedData["non_heap_used"] = rawData["non_heap_used_percentage"]

    return processedData
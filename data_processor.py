# Import the datetime package
import datetime

# Function to process data
class DataProcessor:
  def processData(self, rawData):
    processedData = {}
    
    processedData["uptime_hours"] = float(rawData["uptime_hours"])
    processedData["start_time"] = datetime.strptime(rawData["start_time"], '%d-%m-%Y %H:%M:%S')
    processedData["heap_used"] = float(rawData["heap_used"])
    processedData["non_heap_used"] = float(rawData["non_heap_used"])

    return processedData
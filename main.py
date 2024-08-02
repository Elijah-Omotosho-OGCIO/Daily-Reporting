# Import the DataExtractor class for data extraction
from data_extractor import DataExtractor
# Import the DataProcessor class for data processing
from data_processor import DataProcessor
# Import the ReportGenerator class for report generation
from report_generator import ReportGenerator
# Import datetime and timedelta classes for handling dates and times
from datetime import datetime, timedelta

# Define the main function to run the entire data extraction, processing, and report generation workflow
def main():
    # Setting Appliacation api
    application  = "driving-license-api"
    # Define the start date as one day before the current date
    startDate = datetime.now() - timedelta(days=1)
    # Define the end date as the current date and time
    endDate = datetime.now()
    
    # Step 1: Data Extraction
    # Create an instance of DataExtractor to fetch data
    extractor = DataExtractor()
    # Fetch the data for the defined date range and query
    rawData = extractor.getMetrics(startDate,endDate,application)

    # Step 2: Data Processing
    # Create an instance of DataProcessor with the fetched data
    processor = DataProcessor()
    # Processing the data to generate metrics
    processedData = processor.processData(rawData)

    # Step 3: Report Generation
    # Create an instance of ReportGenerator with the processed metrics and configuration settings
    generator = ReportGenerator()
    # Generate the PDF report
    generator.generateReport(processedData,"outputs/daily_stats_report.pdf")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

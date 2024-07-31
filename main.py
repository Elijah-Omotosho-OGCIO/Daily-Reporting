# main.py

# Import the DataExtractor class for data extraction
from data_extractor import DataExtractor
# Import the DataProcessor class for data processing
from data_processor import DataProcessor
# Import the ReportGenerator class for report generation
from report_generator import ReportGenerator
# Import the config module which contains configuration settings
import config
# Import datetime and timedelta classes for handling dates and times
from datetime import datetime, timedelta

# Define the main function to run the entire data extraction, processing, and report generation workflow
def main():
    # Step 1: Data Extraction
    # Create an instance of DataExtractor to fetch data
    extractor = DataExtractor()
    # Define the start date as one day before the current date
    start_date = datetime.now() - timedelta(days=1)
    # Define the end date as the current date and time
    end_date = datetime.now()
    # Define the query to fetch data (modify based on specific requirements)
    query = 'sum(rate(http_requests_total[1m])) by (job)'  
    # Fetch the data for the defined date range and query
    data = extractor.fetchData(start_date, end_date, query)

    # Step 2: Data Processing
    # Create an instance of DataProcessor with the fetched data
    processor = DataProcessor(data)
    # Process the data to generate metrics
    metrics = processor.processData()
    # Add the end date formatted as a string to the metrics
    metrics['date'] = end_date.strftime('%Y-%m-%d')

    # Step 3: Report Generation
    # Create an instance of ReportGenerator with the processed metrics and configuration settings
    generator = ReportGenerator(metrics, config.OUTPUT_DIR, config.TEMPLATE_DIR)
    # Generate the HTML content for the report using the metrics
    html_content = generator.generateHTML()
    # Generate the PDF report from the HTML content
    generator.generatePDF(html_content)

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()

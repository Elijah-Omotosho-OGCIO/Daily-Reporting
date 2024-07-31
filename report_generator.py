# Import necessary modules from the jinja2 package for HTML templating
from datetime import date
from jinja2 import Environment, FileSystemLoader

# Import the HTML class from weasyprint to convert the HTML to PDF
from weasyprint import HTML

# Import the necessary os module for interacting with the operating system
import os

# Import the config module which contains configuration settings
import config

# Define a class to generate reports
class ReportGenerator:

  def __init__(self, metrics, outputDir, templateDir):
    # Initialise the metrics, output directory, and template directory
    self.metrics = metrics
    self.outputDir = outputDir
    self.templateDir = templateDir

  def generateHTML(self):
    """
    Generate HTML report from the metrics using the template.
    """
    # Create a Jinja2 environment with the template directory
    env = Environment(loader=FileSystemLoader(self.templateDir))

    # Load the template from the template directory named 'report.html'
    template = env.get_template('report.html')

    # Render the template with the metrics data to create HTML content
    htmlContent = template.render(
        # Insert the date from metrics
        date=self.metrics['date'],

        # Insert the number of daily active users
        dailyActiveUsers=self.metrics['dailyActiveUsers'],

        # Insert the average session length
        averageSessionLength=self.metrics['averageSessionLength'],

        # Insert the session frequency
        sessionFrequency=self.metrics['sessionFrequency'],

        # Insert the retention rate
        retention_rate=self.metrics['retention_rate'])
    # Return the generated HTML content
    return htmlContent  # Return the generated HTML content

  def generatePDF(self, htmlContent):
    """
    Generate a PDF report from the HTML content.
    """
    # Defining the output file path
    outputFilePath = os.path.join(self.outputDir, 'dailyStatsReport.pdf')

    # Convert the HTML content to PDF and write an Output path
    HTML(string=htmlContent).write_pdf(outputFilePath)

    # Print a message indicating the PDF generation is complete
    print(f'PDF report generated at {outputFilePath}')

if __name__ == "__main__":
  # Define sample metrics for generating a report with examples of each section
  metrics = {
      "date": "2023-08-01",
      "dailyActiveUsers": 1000,
      "averageSessionLength": 30,
      "sessionFrequency": 5,
      "retention_rate": 0.8
  }

  # Create an instance of the ReportGenerator class with the sample metrics
  reportGenerator = ReportGenerator(metrics, config.OUTPUT_DIR,
                                    config.TEMPLATE_DIR)

  # Create the HTML content using the provided metrics
  htmlContent = reportGenerator.generateHTML()

  # Generate the PDF report from the HTML content
  reportGenerator.generatePDF(htmlContent)

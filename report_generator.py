# Import necessary modules from the jinja2 package for HTML templating
from jinja2 import Environment, FileSystemLoader

# Import the HTML class from weasyprint to convert the HTML to PDF
from weasyprint import HTML

# Define a class to generate reports
class ReportGenerator:

  def __init__(self):
    # Initialize the Jinja2 environment with the template directory
    self.env = Environment(loader=FileSystemLoader('templates'))
    self.template = self.env.get_template('report_template.html')

  def generateReport(self, data, outputFile):
    htmlContent = self.template.render(data)
    HTML(string=htmlContent).write_pdf(outputFile)

# Import the timedelta class for time calculations
from datetime import timedelta

# Import the pandas library for data manipulation
import pandas as pd

class DataProcessor:
  def __init__(self, data):
    # Initialise the extracted DataFrame with the provided data
    self.df = data

  # This function calculates daily active users, average session length, session frequency, and retention rate.
  def processData(self):
    """
    Process the extracted data to calculate required metrics.
    """
    metrics = {"dailyActiveUsers": self.df['user_id'].nunique() if 'user_id' in self.df.columns else 'N/A', 
               "averageSessionLength": self.calculateAverageSessionLength(),
               "sessionFrequency": self.calculateSessionFrequency(),
               "retentionRate": self.calculateRetentionRate()
              }
    # It returns a dictionary containing these metrics.
    return metrics

  # This function checks if the 'session_length' column exists in the DataFrame.
  def calculateAverageSessionLength(self):
    """
    Calculate average session length.
    """
    # If it exists, it calculates the mean of the 'session_length' column and returns it.
    if 'session_length' in self.df.columns:
      return self.df['session_length'].mean()
    # Otherwise, it returns 'N/A'.
    return 'N/A'

  # This function checks if the 'user_id' column exists in the DataFrame.
  def calculateSessionFrequency(self):
    """
    Calculate session frequency per user
    """
    # If it exists, it groups the DataFrame by 'user_id' and calculates the size of each group.
    if 'user_id' in self.df.columns:
      # It then returns the mean of the group sizes, representing the average session frequency per user.
      sessionCounts = self.df.groupby('user_id').size()
      return sessionCounts.mean()
    # Otherwise, it returns 'N/A'.
    return 'N/A'

  # This function checks if the 'user_id' column exists in the DataFrame.
  def calculateRetentionRate(self):
    """
    Calculate retention rate
    """
    # If it exists, it calculates the retention rate based on the assumption that 'timestamp' represents the login timestamp.
    if 'user_id' in self.df.columns:
      # It identifies users who logged in on consecutive days and calculates the ratio of retained users to the total number of unique users.
      # Assuming 'timestamp' is the login timestamp and users logging in consecutive days are retained
      firstLogin = self.df.groupby('user_id')['timestamp'].min()
      retainedUser = firstLogin[firstLogin < (self.df['timestamp'].max() - timedelta(days=-1))]
      retentionRate = len(retainedUser) / self.df['user_id'].nunique()
      return retentionRate
    # Otherwise, it returns 'N/A'.
    return 'N/A'

if __name__ == "__main__":
  # Example usage of DataFrame
  df = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 1],
    'session_length': [10, 20, 30, 40, 15],
    'timestamp': ['1627884000', '1627887600', '1627891200', '1627894800', '1627898400']
  })
  processor = DataProcessor(df)
  metrics = processor.processData()
  print(metrics)
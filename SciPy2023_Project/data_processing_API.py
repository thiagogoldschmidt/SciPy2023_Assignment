import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# This class handles data retrieval and processing of survey data from Google Sheets
class SurveyDataProcessor:
    
    # Define the scope of permissions for the Google Sheets API
    SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # Path to the Google service account credentials JSON file

    CREDS_PATH = '/Users/thiagogoldschmidt/Desktop/Thesis_Python_script/bachelor-thesis-survey-5cfd13208281.json'
    TASKS = [1, 2, 3]
    # Define the tasks and dimensions for the survey analysis
    # Tasks represent different sections or parts of the survey.
    # Dimensions represent different metrics or categories within each task.
    DIMENSIONS = ['E', 'Q', 'S', 'P', 'Si']  # E for Efficiency, Q for Quality, S for Satisfaction, P for Prevalence, Si for Significance
    
    def __init__(self, survey_name):
        """
        Initializes the SurveyDataProcessor with a specified survey name.
    
        Args:
        - survey_name (str): The name of the Google Sheet containing the survey data.
    
        Attributes:
        - survey_name (str): Stores the name of the survey.
        - client (Client): Google Sheets API client authorized using provided credentials.
        - df (DataFrame): Data retrieved from the Google Sheet and stored as a Pandas DataFrame.
        """
        self.survey_name = survey_name
        self.client = self._get_gspread_client()
        self.df = self._fetch_data_from_sheet()

        
    def _get_gspread_client(self):
        """
        Authorizes and returns a Google Sheets API client using service account credentials.
    
        Returns:
        - Client: Google Sheets API client.
        """
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.CREDS_PATH, self.SCOPE)
        return gspread.authorize(creds)
    
    def _fetch_data_from_sheet(self):
        """
        Fetches the survey data from the Google Sheet specified by the survey_name attribute.
    
        Returns:
        - DataFrame: Pandas DataFrame containing the fetched survey data.
         """
        # Find the workbook by name and open the first sheet
        sheet = self.client.open(self.survey_name)
        sheet_instance = sheet.get_worksheet(0)

        # Get all records of the data and convert to DataFrame
        records_data = sheet_instance.get_all_records()
        return pd.DataFrame(records_data)

    def calculate_averages(self):
        """
        Calculates the average score for each combination of tasks and dimensions from the survey data.
    
        Returns:
        - DataFrame: A Pandas DataFrame containing the average scores for each task and dimension combination.
                 The DataFrame has columns: 'Task', 'Dimension', and 'Average'.
        """
        averages = pd.DataFrame(columns=['Task', 'Dimension', 'Average'])
        
        # Iterate over each task and dimension combination
        for task in self.TASKS:
            for dimension in self.DIMENSIONS:
                # Filter the data for the current task and dimension
                task_dimension_df = self.df.filter(regex=f'.*{dimension}{task}.*')
                # Calculate the average score for the current task and dimension
                average = task_dimension_df.mean().mean()
                new_row = pd.DataFrame([{'Task': task, 'Dimension': dimension, 'Average': average}])
                averages = pd.concat([averages, new_row], ignore_index=True)


        return averages

    def calculate_general_averages(self):
        """
        Calculates the average scores for general survey questions (questions without specific task and dimension identifiers).
    
        Returns:
        - Series: A Pandas Series containing average scores for the general survey questions.
        """
        # Drop the 'Timestamp' column if it exists
        df = self.df.drop(columns=['Timestamp'], errors='ignore')

        # Identify the columns corresponding to general questions (without task and dimension identifiers)
        general_columns = [col for col in df.columns if not any(f"{dim}{task}" in col for task in self.TASKS for dim in self.DIMENSIONS)]

        # Filter the dataframe to include only general question columns
        df_general = df[general_columns]

        # Calculate and return the average scores for the general questions
        return df_general.mean()
    
    def compute_prioritization_scores(self, averages, weights):
        """
        Computes the prioritization scores for each task based on given average scores and dimension weights.
    
        Parameters:
        - averages (DataFrame): The average scores for each task and dimension.
        - weights (dict): A dictionary with dimensions as keys and their respective weights as values.
        
        Returns:
        - DataFrame: A Pandas DataFrame containing the prioritization scores for each task. 
                    The DataFrame has columns: 'Task' and 'Prioritization Score'.
        """
        prioritization_scores = pd.DataFrame(columns=['Task', 'Prioritization Score'])
        
        for task in self.TASKS:
            task_df = averages[averages['Task'] == task]
            
            # Compute the weighted score for each dimension of the task
            score = sum(
                task_df[task_df['Dimension'] == dimension]['Average'].values[0] * weights.get(dimension, 0)
                for dimension in weights
            )
            
            # For specific dimensions (E, Q, S), adjust the score by considering (1 - average)
            for dimension in ['E', 'Q', 'S']:
                if dimension in task_df['Dimension'].values:
                    score -= 2 * task_df[task_df['Dimension'] == dimension]['Average'].values[0] * weights.get(dimension, 0)
            
            score = score / 5  # Adjust score by dividing by 5
            new_row = pd.DataFrame({'Task': [task], 'Prioritization Score': [score]})
            prioritization_scores = pd.concat([prioritization_scores, new_row], ignore_index=True)
        
        return prioritization_scores
    
    def prepare_data_for_violinplot(self):
        """
        Prepares and reshapes the survey data into a long form suitable for generating violin plots.
        
        Returns:
        - DataFrame: A Pandas DataFrame containing the data in a long format for violin plots. 
                    The DataFrame has columns: 'Survey', 'Task-Dimension', and 'Score'.
        """
        long_data = []

        for task in self.TASKS:
            for dimension in self.DIMENSIONS:
                # Extract data relevant to the current task and dimension
                task_dimension_df = self.df.filter(regex=f'.*{dimension}{task}.*')

                # Convert wide data to long form
                for _, row in task_dimension_df.iterrows():
                    for col in task_dimension_df.columns:
                        score = row[col]
                        if pd.notna(score):  # Exclude missing values
                            long_data.append({
                                "Survey": self.survey_name,
                                "Task-Dimension": f"{task}-{dimension}",
                                "Score": score
                            })

        return pd.DataFrame(long_data)
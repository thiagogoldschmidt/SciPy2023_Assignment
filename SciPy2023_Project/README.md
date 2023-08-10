# VisioLab Operations Enhancement Analysis with ChatGPT

## Introduction
This project is an intrinsic part of a Bachelor thesis aimed at evaluating the impact of ChatGPT on the efficiency and efficacy of tasks performed by VisioLab's growth and operations team. The scripts encompass data processing, analysis, and visualization tools to provide a comprehensive understanding of the data collected from surveys conducted before and after ChatGPT's implementation.

## Objective
To quantitatively assess the influence of ChatGPT on:

- Team productivity and efficiency.
- Quality of output and deliverables.
- Overall job satisfaction and engagement.

## Repository Structure
1. **data_processing_API.py**
   - **Purpose**: Central to data manipulation, this script fetches survey data via an API, preprocesses, and structures it, making it ready for analysis and visualization.
   - **Key Features**:
     - API Data Retrieval
     - Data Cleaning
     - Averages Calculation
     - Prioritization Score
     - Data Structuring for Visualizations

2. **visualizations.py**
   - **Purpose**: Dedicated to rendering insightful visualizations based on the processed data. It translates raw numbers into understandable and actionable insights.
   - **Key Features**:
     - Bar Charts
     - Heatmaps
     - Line Graphs
     - Comparative Plots
     - Distribution Plots (Violin Plots)

3. **main.py**
   - **Purpose**: Acts as the conductor, seamlessly integrating data processing with visualization. It ensures a smooth flow of data from raw input to insightful output.
   - **Key Features**:
     - Data Processors Initialization
     - Data Analysis
     - Visualization Generation
     - Results Compilation

## API Access and Usage

### Preparing for API Access:
1. **API Endpoint and Credentials**: The necessary API endpoint and credentials are provided in the `bachelor-thesis-survey-5cfd13208281.json` file included in this repository. Ensure you've loaded and parsed this JSON file to retrieve the required details.
2. **Authentication**: Use the credentials from the JSON file for authentication while making API requests.
3. **Data Retrieval**: The `data_processing_API.py` script is designed to fetch survey data directly from the API using the provided credentials. Ensure that you have an active internet connection for seamless data retrieval.

## Access to the Google Sheets
Access to Survey Data: [Link to Google Sheet](https://drive.google.com/drive/folders/1N9qC-4LPg_ZCxZSAZTetjcau-rKYFxUp?usp=sharing)

## Execution Instructions

## Prerequisites

### Environment and Dependencies:
- **Python**: Ensure you have Python (version 3.x recommended) installed on your system.
- **Libraries**: The following Python libraries are essential for the successful execution of the scripts:
    - `pandas`: Install via `pip install pandas`
    - `matplotlib`: Install via `pip install matplotlib`
    - `seaborn`: Install via `pip install seaborn`
    - `numpy`: Install via `pip install numpy`
    - `oauth2client`: Install via `pip install oauth2client`


### Execution:

1. **Running the Script**: Navigate to the directory containing the scripts and execute the `main.py` script:

2. **Settings and Configuration**:
    - **Survey Names**: At the beginning of the `main.py` script, there's a section where you can define the names of the surveys you wish to analyze. Adjust the `SURVEY_NAMES` list to include the titles of the Google Sheets that contain your survey data. Make sure these titles match exactly with the names of the sheets as they appear in Google Drive.
    - **Weights Configuration**: If you wish to adjust the weights for the prioritization score calculation, modify the `weights` dictionary in the `main.py` script.
    - **Visualization Styles**: You can customize the appearance and style of all the visualizations using the global variable named `color_palette` found in the `visualizations.py` script. Adjust the colors to fit your preference or to match the theme of your presentation.


### Interpreting Outputs:

1. **Grouped Bar Charts**: These charts display average scores for different dimensions across tasks. Higher bars indicate better performance in that particular dimension for a task.
2. **Heatmaps**: A visual representation of average scores. Darker colors represent higher scores, allowing for a quick understanding of high and low-performing areas.
3. **Line Graphs**: Tracks average scores across tasks. Any noticeable upward or downward trend indicates an improvement or decline in performance, respectively.
4. **Comparative Plots**: Side-by-side bars showing differences in scores between initial and later surveys. It provides a direct comparison of performance before and after the implementation of ChatGPT.
5. **Violin Plots**: Depicts the distribution of scores. The width of the plot at different score levels shows the density of responses, giving insights into the most common scores for a task or dimension.

By following the steps above and interpreting the visualizations, you'll gain a comprehensive understanding of the tasks' performance and the overall impact of ChatGPT integration.

## Results

Upon executing the scripts, you'll obtain a series of plots and visualizations offering insights into areas of improvement, task performance, and the overall impact of ChatGPT on the growth and operations team's workflow.

## Conclusion and Implications

Post-analysis, this toolkit provides actionable insights into areas that have seen significant improvement with ChatGPT and those that might require further optimization. It's a stepping stone for organizations aiming to leverage AI for operational enhancement, offering a blueprint to replicate and adapt the process in different contexts.

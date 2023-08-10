from data_processing_API import SurveyDataProcessor
import visualizations as viz

# Define the surveys you want to analyze
SURVEY_NAMES = ['Thiago Bachelor Thesis v.2 (Responses)', 'Results Thiago Bachelor Thesis v.2 (Responses)']

# Create `SurveyDataProcessor` instances for each survey. This class fetches data from the Google Sheet
# and provides methods to compute averages and other metrics from the fetched data.
processors = [SurveyDataProcessor(survey_name) for survey_name in SURVEY_NAMES]

# Calculate the average scores for each dimension and task for the surveys
averages = [processor.calculate_averages() for processor in processors]

# Define weights for each dimension. This can be adjusted based on the importance of each dimension.
weights = {
    "E": 0.1,
    "Q": 0.2,
    "S": 0.1,
    "P": 0.3,
    "Si": 0.3
}

# Visualizations:

# Plot grouped bar charts for each survey's average scores. 
# This provides a side-by-side comparison for each dimension within the tasks.
for avg in averages:
    viz.create_grouped_bar_charts(avg, processors[0].DIMENSIONS, processors[0].TASKS)

# Plot a heatmap for the first survey's average scores. 
# This provides a visual representation of how scores are distributed across tasks and dimensions.
viz.create_heatmap(averages[0])

# Plot line graphs to visualize the trend of scores across dimensions for each task in the first survey.
viz.create_line_graphs(averages[0], processors[0].TASKS)

# Calculate and visualize the prioritization scores for the first survey.
# This score is based on the average scores and predefined weights for each dimension.
prioritization_scores = processors[0].compute_prioritization_scores(averages[0], weights)
viz.plot_prioritization_scores(prioritization_scores)

# Plot a comparison of average scores between the initial and later survey for each task and dimension.
viz.plot_task_specific_scores(averages[0], averages[1], processors[0].TASKS, processors[0].DIMENSIONS)

# Plot a comparison of average scores for general questions between the initial and later survey.
viz.plot_general_comparison(processors[0], processors[1])

# Prepare the data in a format suitable for violin plots. This will allow us to visualize the distribution of scores.
data_violins = [processor.prepare_data_for_violinplot() for processor in processors]

# Plot violin graphs to visualize the distribution of scores for each dimension and task.
# The graphs are created in pairs, comparing the distributions between the initial and later surveys.
for i in range(0, len(data_violins), 2):  # Assuming you always have even number of surveys
    viz.plot_violin_graph(data_violins[i], data_violins[i+1])

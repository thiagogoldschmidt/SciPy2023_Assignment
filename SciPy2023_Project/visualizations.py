import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import textwrap
import seaborn as sns
from data_processing_API import SurveyDataProcessor

# Set global style for all plots
sns.set_style("whitegrid")

# Define a color palette
color_palette = sns.color_palette("muted") # Colour palette 


def create_grouped_bar_charts(averages, dimensions, tasks):
    """
    Creates grouped bar charts to visualize average scores for each dimension across different tasks.
    
    Parameters:
    - averages (DataFrame): The average scores for each task and dimension.
    - dimensions (list): A list of dimension identifiers.
    - tasks (list): A list of task identifiers.
    
    Returns:
    None
    """
    # Define the width of each bar in the bar chart
    width = 0.8 / len(dimensions) 
    fig, ax = plt.subplots()

    # Iterate over dimensions to create grouped bars    
    for i, dimension in enumerate(dimensions):
        dimension_df = averages[averages['Dimension'] == dimension]
        ax.bar(dimension_df['Task'] + i * width - width*(len(dimensions)-1)/2, dimension_df['Average'], width, label=dimension, color=color_palette[i % len(color_palette)])

    # Set x-axis ticks and labels
    ax.set_xticks(np.arange(1, len(tasks) + 1))
    ax.set_xticklabels([f'Task {i}' for i in tasks])
    ax.set_ylim(0, 7)
    ax.set_title('Average Scores')
    ax.set_xlabel('Task')
    ax.set_ylabel('Average Score')
    ax.legend()
    plt.show()

def create_heatmap(averages):
    """
    Creates a heatmap to visualize average scores across dimensions and tasks.
    
    Parameters:
    - averages (DataFrame): The average scores for each task and dimension.
    
    Returns:
    None
    """
    heatmap_data = averages.pivot(index='Dimension', columns='Task', values='Average')
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
    plt.title('Heatmap of Average Scores')
    plt.show()


def create_line_graphs(averages, tasks):
    """
    Creates line graphs to visualize average scores for each dimension across different tasks.
    
    Parameters:
    - averages (DataFrame): The average scores for each task and dimension.
    - tasks (list): A list of task identifiers.
    
    Returns:
    None
    """

    # Define the y-axis range for the graph
    y_range = [0, 7]
    
    # Define the desired order for dimensions for a consistent look across graphs
    ordered_dimensions = ['E', 'Q', 'S', 'P', 'Si']  # Define the desired order
    
    for idx, task in enumerate(tasks):
        task_df = averages[averages['Task'] == task]
        
        # Reorder the dataframe according to the desired order of dimensions
        task_df = task_df.set_index('Dimension').loc[ordered_dimensions].reset_index()
        
        # Plot a line for each task with a distinct color and marker
        plt.plot(task_df['Dimension'], task_df['Average'], marker='o', label=f'Task {task}', color=color_palette[idx])

    # Set titles, labels, and other graph properties
    plt.title('Line Graph of Average Scores for Each Dimension')
    plt.xlabel('Dimension')
    plt.ylabel('Average Score')
    plt.ylim(y_range)  
    plt.legend()
    plt.grid(True)
    plt.show()



def plot_prioritization_scores(prioritization_scores):
    """
    Plots a bar graph to visualize the prioritization scores for each task.
    
    Parameters:
    - prioritization_scores (DataFrame): The prioritization scores for each task.
    
    Returns:
    None
    """
    
    # Sort the DataFrame by prioritization score in descending order for better visualization
    sorted_prioritization_scores = prioritization_scores.sort_values(by='Prioritization Score', ascending=False)
    
    # Create the bar graph using the sorted data and colors from the global color palette
    plt.bar(
        sorted_prioritization_scores['Task'],
        sorted_prioritization_scores['Prioritization Score'],
        color=color_palette[:len(sorted_prioritization_scores)]  # use as many colors as the tasks
    )
    
    # Set graph titles, labels, and other properties
    plt.title('Prioritization Scores for Each Task')
    plt.xlabel('Task')
    plt.ylabel('Prioritization Score')
    plt.ylim(0, 1)  # Set y-axis limits to 0-1

    # Assign x-ticks based on the tasks
    plt.xticks(ticks=[1, 2, 3], labels=sorted_prioritization_scores['Task'])

    plt.show()


def plot_task_specific_scores(averages1, averages2, tasks, dimensions, width_adjusted=0.35):
    """
    Plots a grouped bar chart comparing average scores from two different surveys for specific tasks and dimensions.

    Parameters:
    - averages1 (DataFrame): The average scores for each task and dimension from the first survey.
    - averages2 (DataFrame): The average scores for each task and dimension from the second survey.
    - tasks (list): A list of task identifiers.
    - dimensions (list): A list of dimension identifiers.
    - width_adjusted (float, optional): Adjusted width for the bars in the bar chart. Default is 0.35.

    Returns:
    None
    """

    # Initialize the plot and set its size
    fig, ax = plt.subplots(figsize=(15, 7))

    # Set up the x-axis values based on the number of dimensions and tasks
    x = np.arange(len(dimensions))
    bar_positions = []

    # Colors for Initial and Later Surveys from the global color palette
    color_initial = color_palette[0]
    color_later = color_palette[1]

    # Loop through each task to plot its bars
    for idx, task in enumerate(tasks):

        # Filter data for the current task
        task_df1 = averages1[averages1['Task'] == task]
        task_df2 = averages2[averages2['Task'] == task]

        # Extract the average scores in the order of the provided dimensions list
        bars1 = task_df1.set_index('Dimension')['Average'].reindex(dimensions).tolist()
        bars2 = task_df2.set_index('Dimension')['Average'].reindex(dimensions).tolist()
        
        # Calculate x-axis positions for the bars based on the current task index
        positions = x + idx * (len(dimensions) + 1)
        bar_positions.extend(positions)

        # Plot bars for both surveys side-by-side for easy comparison
        ax.bar(positions - width_adjusted/2, bars1, width_adjusted, color=color_initial, alpha=0.6, label=f'Initial Survey' if idx == 0 else "")
        ax.bar(positions + width_adjusted/2, bars2, width_adjusted, color=color_later, alpha=0.6, label=f'Later Survey' if idx == 0 else "")

    # Setting properties for x-axis ticks, labels, and graph title
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([f'{dim}{idx+1}' for idx in range(len(tasks)) for dim in dimensions])
    ax.set_ylim(0, 7)
    ax.set_title(f'Average Scores for Tasks')
    ax.set_xlabel('Dimension')
    ax.set_ylabel('Average Score')

    # Add a legend to the plot to differentiate between the two surveys
    ax.legend(title="Survey", loc="upper right")

    # Adjust the layout for better display
    plt.tight_layout()
    plt.show()


def plot_general_comparison(processor1, processor2):
    """
    Plots a horizontal bar chart comparing average scores for general questions from two different surveys.
    
    Parameters:
    - processor1: An instance of the data processor class for the first survey.
    - processor2: An instance of the data processor class for the second survey.

    Returns:
    None
    """

    # Calculate average scores for general questions from both surveys using the data processors
    averages_general1 = processor1.calculate_general_averages()
    averages_general2 = processor2.calculate_general_averages()

    # Construct a DataFrame containing average scores from both surveys, as well as their differences
    df_general_averages = pd.DataFrame({
        'Initial': averages_general1, 
        'Later': averages_general2,
        'Difference': averages_general2 - averages_general1
    })

    # Determine y-values (position) for the bars based on the number of questions
    y_values = df_general_averages.index
    width = 0.4  # width of the bars

    # Wrap long question text to make y-tick labels more readable
    wrapped_labels = [textwrap.fill(label, width=45) for label in y_values]

    # Adjusting the y-values for grouped bars
    y_initial = [y + width/2 for y in range(len(y_values))]
    y_later = [y - width/2 for y in range(len(y_values))]

    # Create a new figure and axis for the plot
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot horizontal bars for average scores from the initial and later surveys
    ax.barh(y_initial, df_general_averages['Initial'], width, color=color_palette[0], label='Initial Survey', alpha=0.6)
    ax.barh(y_later, df_general_averages['Later'], width, color=color_palette[1], label='Later Survey', alpha=0.6)

    # Setting the y-ticks and labels for the plot
    ax.set_yticks(range(len(y_values)))
    ax.set_yticklabels(wrapped_labels)

    # Add a legend and title to the plot
    ax.legend()
    ax.set_title('Comparison of Average Scores for General Questions')

    # Display the plot
    plt.show()


def plot_violin_graph(data1, data2):
    """
    Plots a side-by-side violin graph comparing the distributions of scores for each task and dimension 
    across two surveys. The graphs show the distribution of responses for each combination of task and dimension.
    
    Parameters:
    - data1 (DataFrame): Data from the first survey. Should have columns 'Task-Dimension', 'Score', and 'Survey'.
    - data2 (DataFrame): Data from the second survey. Should have columns 'Task-Dimension', 'Score', and 'Survey'.
    
    Returns:
    None
    """
    
    # Update the Survey columns to differentiate the source of data
    data1['Survey'] = 'Initial Survey'
    data2['Survey'] = 'Later Survey'
    
    # Combine the data from both dataframes into a single dataframe
    combined_data = pd.concat([data1, data2])
    
    # Define the tasks present in the data
    tasks = [1, 2, 3]
    
    # Initialize a figure with 3 subplots (one for each task), sharing the y-axis
    fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
    
    # Define a color palette to distinguish between the two surveys
    hue_palette = {
        'Initial Survey': color_palette[0],
        'Later Survey': color_palette[1]
    }
    
    # Plot the violin graphs for each task
    for i, task in enumerate(tasks):
        # Filter data for the current task
        task_data = combined_data[combined_data['Task-Dimension'].str.startswith(str(task))]
        
        # Plot the violin graph for the current task, splitting by the 'Survey' hue
        sns.violinplot(
            x="Task-Dimension", y="Score", hue="Survey", data=task_data, 
            ax=axs[i], split=True, inner="quartile", palette=hue_palette
        )
        
        # Set title and x-label for the subplot
        axs[i].set_title(f'Task {task} Distribution')
        axs[i].set_xlabel('Dimension')
        
        # Set y-label only for the first subplot to avoid repetition
        if i == 0:
            axs[i].set_ylabel('Score')
        else:
            axs[i].set_ylabel('')

    # Adjust the layout for better presentation
    plt.tight_layout()
    
    # Render the plots
    plt.show()

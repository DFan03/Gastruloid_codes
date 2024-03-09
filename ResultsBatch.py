#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 20:14:52 2024

@author: donglifan
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Path to the master directory
master_directory = os.getcwd()+"/Converted"
output_directory=  os.getcwd()+"/FiguresOutput"

directory_path = output_directory

# Create the directory, including any intermediate directories
try:
    os.makedirs(directory_path, exist_ok=True)
    print(f"Directory '{directory_path}' created successfully")
except OSError as error:
    print(f"Error creating directory '{directory_path}': {error}")
# Placeholder for dataframes
dataframes = []

# Iterate over all entries in the master directory
for subdir, dirs, files in os.walk(master_directory):
    for file in files:
        # Check if the file ends with .csv
        if file.endswith('.csv'):
            # Construct full file path
            file_path = os.path.join(subdir, file)
            # Read the CSV file into a dataframe
            df = pd.read_csv(file_path)
            # Add a new column to the dataframe with the sub-directory name
            df['condition'] = os.path.basename(subdir)
            # Append the dataframe to the list of dataframes
            dataframes.append(df)

# Concatenate all dataframes into one
rawdata = pd.concat(dataframes, ignore_index=True)
rawdata.drop(rawdata.columns[0], axis=1, inplace=True)

excl_mat = rawdata[~rawdata['condition'].str.contains("Matrigel", case=False, na=False)]

# =============================================================================
# Functions
# =============================================================================

def CreateCellLine(data, list_of_cell_lines):
    """
    This function processes the 'Condition' column to assign clean 'cell_line' and 'treatment' values.
    Only strings from the list_of_cell_lines are included in the 'cell_line' column.

    Parameters:
    - data: A pandas DataFrame that contains a 'Condition' column.
    - list_of_cell_lines: A list of strings, each one a valid cell line name.

    Returns:
    - The modified DataFrame with 'cell_line' and 'treatment' columns.
    """
    # Initialize new columns
    data['cell_line'] = ''
    data['treatment'] = 'NT'  # Default treatment is 'NT'

    # Iterate through the DataFrame
    for index, row in data.iterrows():
        condition_parts = row['condition'].split('+', 1)  # Split at the first '+'
        cell_line_part = condition_parts[0]  # Before the '+'
        treatment_part = condition_parts[1] if len(condition_parts) > 1 else 'NT'  # After the '+', or 'NT' if absent

        # Check if the cell_line_part matches any of the known cell lines
        for cell_line in list_of_cell_lines:
            if cell_line in cell_line_part:
                data.at[index, 'cell_line'] = cell_line
                break  # Stop checking after the first match

        # Assign treatment
        data.at[index, 'treatment'] = treatment_part

    return data




def BoxPlot(x,data,colors):
    """
    This function plot the column X and assign different color base on the 
    colors column as a box plot.

    Parameters:
    - data: A pandas DataFrame that contains a 'Condition' column.
    - x: A string of the column name of interest
    - colors: A string of the column name to assign color.

    Returns:
    - Save the figure as 300dpi png in FigureOutput folder.
    """
    X=x
    figure_size = (10, 6) 
    plt.figure(figsize=figure_size)
    sns.set(style="whitegrid")
    box_plot = sns.boxplot(x=X, y=colors, data=data, palette='tab10', dodge=False)
    plt.xlabel(X)
    plt.ylabel('') 
    plt.title(f'Visualization of {X} marked by {colors}')
    
    # Adjust the figure to make space for the legend
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    filename = f"BoxPlot_{X}_vs_{colors}.png"
    full_path = os.path.join(directory_path, filename)
    plt.savefig(full_path,dpi=300)
    

def plot_scatter_with_highlight(x, y, data, cell, treat,name):
    """
    Plots a scatter plot of columns x and y from the DataFrame data.
    Points that match one of the cell lines AND one of the treatments are plotted in color.
    All other points are plotted in gray.

    Parameters:
    - x: The column name to be used for the x-axis.
    - y: The column name to be used for the y-axis.
    - data: The DataFrame containing the data.
    - cell: A list of strings specifying the cell lines to highlight.
    - treat: A list of strings specifying the treatments to highlight.
    - name: the name of output file, use this for iteration.
    """
    
    # Create a mask for rows with specified cell lines AND treatments
    figure_size = (10, 10) 
    plt.figure(figsize=figure_size)
    mask = data['cell_line'].isin(cell) & data['treatment'].isin(treat)

    # Plot points that do not match the mask in gray
    plt.scatter(data.loc[~mask, x], data.loc[~mask, y], color='gray', alpha=0.2, label='Other')

    # Plot points that match the mask in color
    for c in cell:
        for t in treat:
            specific_mask = (data['cell_line'] == c) & (data['treatment'] == t)
            plt.scatter(data.loc[specific_mask, x], data.loc[specific_mask, y], label=f'{c}/{t}')

    # Labeling the axes and setting the title
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(f'Highlight Scatter Plot of {y} vs {x} ')
    plt.legend(title='Condition')
    filename = f"Hightlight_ScatterPlot_{x}_{y}_{name}.png"
    full_path = os.path.join(directory_path, filename)
    plt.savefig(full_path,dpi=300)




def ScatterPlot(x,y,data,colors)    :
    """
    This function plot the column X and y with different color base on the 
    colors column as a scatter plot. Different Markers are used for distinct
    cell_line.

    Parameters:
    - data: A pandas DataFrame that contains a 'Condition' column.
    - x: A string of the column name of interest
    - y: A string of the column name of interest
    - colors: A string of the column name to assign color.

    Returns:
    - Save the figure as 300dpi png in FigureOutput folder.
    """
    # Choose the columns for the X and Y axes
    x_column = x
    y_column = y
    
    # Set the seaborn style
    sns.set(style="whitegrid")
    figure_size = (10, 10) 
    plt.figure(figsize=figure_size)
    # Create a scatter plot
    scatter_plot = sns.scatterplot(x=x_column, y=y_column, hue=colors, style="cell_line",data=data,legend="brief", palette='tab10')
    
    # Enhance the visualization with labels and title
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Scatter Plot of {y_column} vs {x_column} marked by {colors}')
    
    # Move the legend to the right side of the plot    
    # Adjust layout for better readability
    filename = f"ScatterPlot_{x}_{y}_vs_{colors}.png"
    full_path = os.path.join(directory_path, filename)
    plt.savefig(full_path,dpi=300)



# =============================================================================
# Example of Use
# =============================================================================
def Example():
    Cell_lined_data=CreateCellLine( excl_mat,['CTCF','PT'])
    #the excl_mat is the initial dataframe, ctcf and pt are the two example cell lines
    
    #use the box plot function to plot one varaible, colored by different columns.
    BoxPlot("Circ.",Cell_lined_data,"cell_line")
    BoxPlot("Area",Cell_lined_data,"cell_line")
    BoxPlot("Circ.",Cell_lined_data,"treatment")
    BoxPlot("Area",Cell_lined_data,"treatment")
    BoxPlot("Circ.",Cell_lined_data,"condition")
    BoxPlot("Area",Cell_lined_data,"condition")
    
    
    #Example of iteration that highlight intra-inter cell line treatment difference
    
    #grab all cell lines and treatments from the datafram.
    unique_treatments = Cell_lined_data['treatment'].unique().tolist()
    unique_cell_line = Cell_lined_data['cell_line'].unique().tolist()
    
    #Compare same treatment between cell line
    ScatterPlot("Circ.", "Area", Cell_lined_data, "treatment")
    
    #Iterate among treatment
    counter=0
    for i in unique_treatments:
        counter+=1
        plot_scatter_with_highlight("Circ.", "Area", Cell_lined_data, 
                                    ['CTCF','PT'], [i],f"treatment_by_cell {counter}")
    
    #Iterate among cell_line
    counter=0
    for i in unique_cell_line:
        counter+=1
        plot_scatter_with_highlight("Circ.", "Area", Cell_lined_data,
                                    [i],unique_treatments, f"cell_by_treatment {counter}")
        
Example() #remove this line so the example does not run.
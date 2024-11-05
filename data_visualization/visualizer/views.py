# visualizer/views.py
from django.shortcuts import render
import seaborn as sns
import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np

def visualization(request):
    # Load the dataset
    data = sns.load_dataset("tips")
    print(data.head(150))
    
    # Pass the entire days of the week to the template
    days_of_week = ['Thur', 'Fri', 'Sat', 'Sun']

    # Get the selected day from GET request, default to 'Thur'
    selected_day = request.GET.get('day', 'Thur')

    # Filter the dataset based on the selected day
    # This assumes your dataset has entries for each day, if it doesn't, it will just return what it has.
    filtered_data = data[data['day'] == selected_day]

    # Initialize plot URLs
    bar_url = scatter_url = None

    # Check if there's data for the selected day
    if not filtered_data.empty:
        # Plot 1: Bar Plot for the selected day
        plt.figure(figsize=(10, 6))
        sns.barplot(x='day', y='total_bill', data=filtered_data)
        plt.title(f"Average Total Bill on {selected_day}")
        bar_plot = io.BytesIO()
        plt.savefig(bar_plot, format='png')
        bar_plot.seek(0)
        bar_url = urllib.parse.quote(base64.b64encode(bar_plot.read()).decode())

        # Plot 2: Scatter Plot for the filtered dataset
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='total_bill', y='tip', data=filtered_data)
        plt.title(f"Scatter Plot of Total Bill vs Tip on {selected_day}")
        scatter_plot = io.BytesIO()
        plt.savefig(scatter_plot, format='png')
        scatter_plot.seek(0)
        scatter_url = urllib.parse.quote(base64.b64encode(scatter_plot.read()).decode())
    else:
        # If no data for the selected day, set a message
        bar_url = scatter_url = None

    return render(request, 'visualizer/visualization.html', {
        'bar_plot': bar_url,
        'scatter_plot': scatter_url,
        'selected_day': selected_day,
        'days_of_week': days_of_week,  # Pass the days of the week
        'data_available': not filtered_data.empty  # Flag for data availability
    })

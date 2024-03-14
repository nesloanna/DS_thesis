import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import pandas as pd
import os
import xarray as xr
import numpy as np
import geopandas as gpd

import pprint
pp = pprint.PrettyPrinter(indent=4)

# Define the directory where you want to save the data
data_dir = "/Users/annaolsen/Desktop/Speciale/DS_thesis/data"

os.chdir(data_dir)
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_SST.csv")


# Create a function to plot the original points and their closest matches

def plot_original_and_closest_matches(df):

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    fig, ax = plt.subplots(figsize=(15, 15))

    # Plot world map
    world.plot(ax=ax, color='lightgray', edgecolor='black')

    # Plot original points
    ax.scatter(df['Longitude'], df['Latitude'],
               color='mediumblue', label='Original points', s=12)

    # Plot closest match points
    ax.scatter(df['closest_lon'], df['closest_lat'],
               color='darkorange', label='Closest matches', s=10)

    # Set title
    ax.set_title('Original Points and Closest Matches')
    # Add legend
    ax.legend()

    plt.show()


# Call the function to plot
plot_original_and_closest_matches(df)


# Plot comparison
plt.figure(figsize=(10, 6))
plt.plot(df['Sea Surface Temp'], label='SST from TARA', color='mediumblue')
plt.plot(df['closest_sst'], label='SST from NOAA', color='darkorange')
plt.xlabel('Index')
plt.ylabel('Temperature')
plt.title('SST - TARA vs. NOAA')
plt.legend()
plt.grid(True)
plt.show()


# Group DataFrame by 'OS region'
grouped_df = df.groupby('OS region')

# Iterate over each group and create a separate plot for each region
for region, region_df in grouped_df:

    # Plot comparison for the current region
    plt.figure(figsize=(10, 6))
    plt.plot(region_df['Date'], region_df['Sea Surface Temp'],
             label='SST from TARA', color='mediumblue')
    plt.plot(region_df['Date'], region_df['closest_sst'],
             label='SST from NOAA', color='darkorange')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.title(f'Temperature for {region}')
    plt.legend()
    plt.grid(True)
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, fontsize=10)
    # plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
    # Customize x-axis tick labels to display every other label
    # Adjust the number of bins as needed
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=10))

    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    plt.show()

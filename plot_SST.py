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

df_2009 = pd.read_csv("Tara_SST_09.csv")
df_2010 = pd.read_csv("Tara_SST_10.csv")
df_2011 = pd.read_csv("Tara_SST_11.csv")
df_2012 = pd.read_csv("Tara_SST_12.csv")
df_2013 = pd.read_csv("Tara_SST_13.csv")


# List of DataFrames
dfs = [df_2009, df_2010, df_2011, df_2012, df_2013]

# Concatenate DataFrames along rows (vertically)
df_SST = pd.concat(dfs, ignore_index=True)

df_SST.to_csv("Tara_SST_Plot.csv", index=False)

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
plt.plot(df['Sea Surface Temp'], label='Tara', color='mediumblue')
plt.plot(df['closest_sst'], label='NOAA (weekly)', color='darkorange')
plt.xlabel('Index')
plt.ylabel('Temperature')
plt.title('SST (weekly) - Tara vs. NOAA')
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
             label='Tara', color='mediumblue')
    plt.plot(region_df['Date'], region_df['closest_sst'],
             label='NOAA (weekly)', color='darkorange')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.title(f'SST for {region}')
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


# Plot comparison 2013
plt.figure(figsize=(10, 6))
plt.plot(df_SST['Sea Surface Temp'], label='Tara', color='mediumblue')
plt.plot(df_SST['sst_daily'], label='NOAA (daily)', color='darkorange')
plt.xlabel('Index')
plt.ylabel('Temperature')
plt.title('SST (daily) - Tara vs. NOAA')
plt.legend()
plt.grid(True)
plt.show()


# Group DataFrame by 'OS region'
grouped_df = df_SST.groupby('OS region')

# Iterate over each group and create a separate plot for each region
for region, region_df in grouped_df:

    # Plot comparison for the current region
    plt.figure(figsize=(10, 6))
    plt.plot(region_df['Date'], region_df['Sea Surface Temp'],
             label='Tara', color='mediumblue')
    plt.plot(region_df['Date'], region_df['sst_daily'],
             label='NOAA (daily)', color='darkorange')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.title(f'SST (daily) for {region}')
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

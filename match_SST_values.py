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
df = pd.read_csv("Tara_BMN_Cleaned.csv")

# df = df1[df1['Year'] == 2009]
df = df.sort_values(by='Date')
df = df[["Sample ID", "Latitude", "Longitude", "Sea Surface Temp",
         "Date/Time", "Date", "OS region"]]
df = df.dropna(subset=['Longitude', 'Latitude'])

dates = df['Date'].unique()

# Load external SST data
sst_data = xr.open_dataset("SST/sst.wkmean.1990-present.nc")

# Convert the datetime format to date format
# sst_date = sst_data['time'].dt.date

# Convert latitude and longitude to match the format of the SST dataset
# Round latitude to match resolution of SST data
df['Latitude'] = df['Latitude'].round(2)
# Round longitude to match resolution of SST data
df['Longitude'] = df['Longitude'].round(2)

# Sort longitude values
sst_data = sst_data.sortby('lon')

# Convert longitude values from 0 to 360 to -180 to 180
sst_data['lon'] = xr.where(sst_data['lon'] > 180,
                           sst_data['lon'] - 360, sst_data['lon'])

# Sort longitude values
sst_data = sst_data.sortby('lon')

# Access the 'time' variable and extract its values
# time_values = sst_data['time'].values

# Find unique values
# unique_time_values = set(time_values)

# Convert each datetime object to date
# unique_date_values = [np.datetime64(date, 'D') for date in unique_time_values]

# unique_date_values = sorted(unique_date_values)


# unique_date_values = [str(date).replace(
#     "numpy.datetime64('", "").replace("')", "") for date in unique_date_values]


# Print the unique date values
# print(unique_date_values)
# pp.pprint(unique_date_values)


# Convert the 'time' coordinate to pandas datetime index in sst_data
sst_data['time'] = pd.to_datetime(sst_data['time'].values)

# Convert the 'time' column to datetime type in DataFrame df
df['Date'] = pd.to_datetime(df['Date'])


# # Create a function to find the closest match for a given date
# def find_closest_date(date, sst_data):
#     return pd.to_datetime(sst_data.sel(time=date, method='nearest')['time'].values)


# # Apply the function to each date in 'df'
# df['closest_match'] = df['Date'].apply(
#     lambda x: find_closest_date(x, sst_data))


# Create a function to find the closest match for a given date, latitude, and longitude
def find_closest_match(date, lat, lon, sst_data):
    # Find the nearest time point
    nearest_time = pd.to_datetime(sst_data.sel(
        time=date, method='nearest')['time'].values)

    # Find the nearest latitude and longitude
    nearest_lat = sst_data.sel(time=nearest_time)['lat'].sel(
        lat=lat, method='nearest').values
    nearest_lon = sst_data.sel(time=nearest_time)['lon'].sel(
        lon=lon, method='nearest').values

    # Find the 'sst' value corresponding to the closest date, latitude, and longitude
    sst_value = sst_data.sel(time=nearest_time, lat=nearest_lat, lon=nearest_lon)[
        'sst'].values.item()

    return nearest_time, nearest_lat, nearest_lon, sst_value


# Apply the function to each row in 'df'
df[['closest_date', 'closest_lat', 'closest_lon', 'closest_sst']] = \
    df.apply(lambda row: pd.Series(find_closest_match(
        row['Date'], row['Latitude'], row['Longitude'], sst_data)), axis=1)

# Display the DataFrame with closest matches
print(df)

df.to_csv("Tara_SST.csv", index=False)

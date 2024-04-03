import pandas as pd
import os
import xarray as xr
import numpy as np


import pprint
pp = pprint.PrettyPrinter(indent=4)


data_dir = "/Users/annaolsen/Desktop/Speciale/DS_thesis/data"

os.chdir(data_dir)
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_BMN_Cleaned.csv")

df = df[df['Year'] == 2013]
df = df.sort_values(by='Date')
df = df[["Sample ID", "Latitude", "Longitude", "Sea Surface Temp",
         "Date", "OS region"]]
df = df.dropna(subset=['Longitude', 'Latitude'])

dates = df['Date'].unique()

# # Load external SST data
# sst_data = xr.open_dataset("SST/sst.day.mean.2013.nc")

# # Convert latitude and longitude to match the format of the SST dataset
# # Round latitude to match resolution of SST data
# df['Latitude'] = df['Latitude'].round(2)
# # Round longitude to match resolution of SST data
# df['Longitude'] = df['Longitude'].round(2)

# # Sort longitude values
# sst_data = sst_data.sortby('lon')

# # Convert longitude values from 0 to 360 to -180 to 180
# sst_data['lon'] = xr.where(sst_data['lon'] > 180,
#                            sst_data['lon'] - 360, sst_data['lon'])

# # Sort longitude values
# sst_data = sst_data.sortby('lon')


# # Convert the 'time' coordinate to pandas datetime index in sst_data
# sst_data['time'] = pd.to_datetime(sst_data['time'].values)

# # Convert the 'time' column to datetime type in DataFrame df
# df['Date'] = pd.to_datetime(df['Date'])


# # Create a function to find the closest match for a given date, latitude, and longitude
# def find_closest_match(date, lat, lon, sst_data):
#     # Find the nearest time point
#     nearest_time = pd.to_datetime(sst_data.sel(
#         time=date, method='nearest')['time'].values)

#     # Find the nearest latitude and longitude
#     nearest_lat = sst_data.sel(time=nearest_time)['lat'].sel(
#         lat=lat, method='nearest').values
#     nearest_lon = sst_data.sel(time=nearest_time)['lon'].sel(
#         lon=lon, method='nearest').values

#     # Find the 'sst' value corresponding to the closest date, latitude, and longitude
#     sst_value = sst_data.sel(time=nearest_time, lat=nearest_lat, lon=nearest_lon)[
#         'sst'].values.item()

#     return nearest_time, nearest_lat, nearest_lon, sst_value


# # Apply the function to each row in 'df'
# df[['sst_date', 'sst_lat', 'sst_lon', 'sst_daily']] = \
#     df.apply(lambda row: pd.Series(find_closest_match(
#         row['Date'], row['Latitude'], row['Longitude'], sst_data)), axis=1)

# # Display the DataFrame with closest matches
# print(df)

# df.to_csv("Tara_SST_daily.csv", index=False)


# sst_data = xr.open_dataset("SST/sst.day.mean.2009.nc")
# sst_data = xr.open_dataset("SST/sst.day.mean.2010.nc")
# sst_data = xr.open_dataset("SST/sst.day.mean.2011.nc")
# sst_data = xr.open_dataset("SST/sst.day.mean.2012.nc")
# sst_data = xr.open_dataset("SST/sst.day.mean.2013.nc")

# sst_data = xr.open_dataset("SST/sst.day.anom.2009.nc")
# sst_data = xr.open_dataset("SST/sst.day.anom.2010.nc")
# sst_data = xr.open_dataset("SST/sst.day.anom.2011.nc")
# sst_data = xr.open_dataset("SST/sst.day.anom.2012.nc")
sst_data = xr.open_dataset("SST/sst.day.anom.2013.nc")


# Convert the 'time' coordinate to pandas datetime index
sst_data['time'] = pd.to_datetime(sst_data['time'].values)


# Sort longitude values
sst_data = sst_data.sortby('lon')

# Convert longitude values from 0 to 360 to -180 to 180
sst_data['lon'] = xr.where(sst_data['lon'] > 180,
                           sst_data['lon'] - 360, sst_data['lon'])

# Sort longitude values
sst_data = sst_data.sortby('lon')


# Convert the 'time' column to datetime type in DataFrame df
df['Date'] = pd.to_datetime(df['Date'])


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
    # sst_value = sst_data.sel(time=nearest_time, lat=nearest_lat, lon=nearest_lon)[
    #     'sst'].values.item()

    anom_value = sst_data.sel(time=nearest_time, lat=nearest_lat, lon=nearest_lon)[
        'anom'].values.item()

    return nearest_time, nearest_lat, nearest_lon, anom_value


# Apply the function to each row in 'df'
df[['sst_date', 'sst_lat', 'sst_lon', 'sst_anom']] = \
    df.apply(lambda row: pd.Series(find_closest_match(
        row['Date'], row['Latitude'], row['Longitude'], sst_data)), axis=1)

# Display the DataFrame with closest matches
print(df)

df.to_csv("Tara_SST_ano_13.csv", index=False)

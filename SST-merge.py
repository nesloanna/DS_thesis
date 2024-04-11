import json
import time
import pandas as pd
import os
import xarray as xr
import numpy as np
import pprint
from tqdm import tqdm
pp = pprint.PrettyPrinter(indent=4)


# data_dir = "/Users/annaolsen/Desktop/Speciale/DS_thesis/data/SST/Daily"
sst_data_dir = "/Volumes/PortableSSD/Speciale/SST/SST_daily"

os.chdir(sst_data_dir)
print(os.getcwd())


def get_nc_files(folder_path):
    nc_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".nc") and file.startswith("sst"):
            nc_files.append(file)

    return sorted(nc_files)


nc_files_list = get_nc_files(sst_data_dir)
print(nc_files_list)


# sst_data = xr.open_dataset("sst.day.mean.1984.nc")


# # Convert longitude values from 0 to 360 to -180 to 180
# sst_data['lon'] = xr.where(sst_data['lon'] > 180,
#                            sst_data['lon'] - 360, sst_data['lon'])


# # Sort longitude values
# sst_data = sst_data.sortby('lon')

# # Load datasets
# df = pd.read_csv(
#     "/Users/annaolsen/Desktop/Speciale/DS_thesis/data/Tara_BMN_Cleaned.csv")

# df = df[["Sample ID", "Latitude", "Longitude", "Sea Surface Temp",
#          "Date", "OS region"]]

# df = df.dropna(subset=['Longitude', 'Latitude'])


# Create a function to find the closest match for a given latitude, and longitude
# def find_closest_location(lat, lon, sst_data):

#     # Find the nearest latitude and longitude
#     nearest_lat = sst_data['lat'].sel(lat=lat, method='nearest').values
#     nearest_lon = sst_data['lon'].sel(lon=lon, method='nearest').values

#     return nearest_lat, nearest_lon


# # Apply the function to each row in 'df'
# df[['lat', 'lon']] = \
#     df.apply(lambda row: pd.Series(find_closest_location(
#         row['Latitude'], row['Longitude'], sst_data)), axis=1)

# Display the DataFrame with closest matches
# print(df)


# df.to_csv("Tara_SST_locations.csv", index=False)


# # Convert 'lat' and 'lon' columns to tuples
# df['location'] = list(zip(df['lat'], df['lon']))

# # Extract unique combinations of latitudes and longitudes
# df_unique_locations = df[['location']].drop_duplicates()

# # Convert the 'location' column back to separate 'lat' and 'lon' columns
# df_unique_locations[['lat', 'lon']] = pd.DataFrame(
#     df_unique_locations['location'].tolist(), index=df_unique_locations.index)

# Drop the 'location' column
# df_unique_locations.drop(columns=['location'], inplace=True)

# Reset the index after dropping rows
# df_unique_locations.reset_index(drop=True, inplace=True)

# # Display the result
# print(df_unique_locations)


# df_unique_locations.to_csv("Tara_SST_unique_locations.csv", index=False)
df_unique_locations = pd.read_csv("Tara_SST_unique_locations.csv")


def merge_subset_sst_data(file_paths, locations_df):
    """
    Merge and subset SST data from multiple files based on the given locations DataFrame.

    Parameters:
        file_paths (list): List of file paths containing SST data.
        locations_df (DataFrame): DataFrame containing 'lat' and 'lon' columns.

    Returns:
        merged_data (DataFrame): Merged and subsetted SST data in DataFrame format.
    """

    # Create an empty list to store the DataFrames
    dfs = []

    # Extract latitude and longitude values
    lats = locations_df['lat'].values
    lons = locations_df['lon'].values

    # Loop through each file path
    for file_path in tqdm(file_paths[30:35]):

        # Load external SST data
        dataset = xr.open_dataset(file_path)
        dataset.load()

        rows = []

        for lon, lat in zip(lons, lats):

            # Subset the data for the specified locations
            subset_data = dataset.sel(lon=lon, lat=lat, method='nearest')

            # Subset only the 'sst' variable
            sst_data = subset_data['sst']

            for row in sst_data:

                date = row['time'].values
                temp = row.values

                rows.append({'lon': lon, 'lat': lat,
                            'date': date, 'temp': temp})

        # Create DataFrame for the current file
        df = pd.DataFrame(rows)
        dfs.append(df)

        # Close the file
        dataset.close()

    # Concatenate all DataFrames into a single DataFrame
    merged_data = pd.concat(dfs, ignore_index=True)

    merged_data.to_csv("SST_2011_2013.csv", index=False)

    return merged_data


# merged_data = merge_subset_sst_data(nc_files_list, df_unique_locations)
# nc_files_list[0:5]   -> 1981-1985
# nc_files_list[5:10]  -> 1986-1990
# nc_files_list[10:15] -> 1991-1995
# nc_files_list[15:20] -> 1996-2000
# nc_files_list[20:25] -> 2001-2005
# nc_files_list[25:30] -> 2006-2010
# nc_files_list[30:35] -> 2011-2015 (2011-2013)
sst_csv_folder = "/Users/annaolsen/Desktop/Speciale/DS_thesis/data/SST/merged"

os.chdir(sst_csv_folder)
print(os.getcwd())


def get_csv_files(folder_path):
    csv_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".csv") and file.startswith("SST"):
            csv_files.append(file)

    return sorted(csv_files)


csv_files_list = get_csv_files(sst_csv_folder)
print(csv_files_list)


dataframes = []

for file in csv_files_list:
    dataframes.append(pd.read_csv(file))

merged_df = pd.concat(dataframes, ignore_index=True)

# Write the merged DataFrame to a new CSV file
merged_df.to_csv('merged_SST.csv', index=False)


# merged_data.to_csv("SST_1981_2013.csv", index=False)


# def merge_subset_sst_data(file_paths, lon_min, lon_max, lat_min, lat_max):
#     """
#     Merge and subset SST data from multiple files based on the given bounding box coordinates and time range.

#     Parameters:
#         file_paths (list): List of file paths containing SST data.
#         lon_min (float): Minimum longitude of the bounding box.
#         lon_max (float): Maximum longitude of the bounding box.
#         lat_min (float): Minimum latitude of the bounding box.
#         lat_max (float): Maximum latitude of the bounding box.
#         time_range (tuple, optional): Tuple specifying the start and end dates for the time range (in the format 'YYYY-MM-DD'). Defaults to None.

#     Returns:
#         merged_data (xarray.Dataset): Merged and subsetted SST data.

#     """
#     # Initialize an empty list to store individual subsets
#     subset_data_list = []

#     # Loop through each file path
#     for file_path in file_paths:
#         # Load external SST data
#         dataset = xr.open_dataset(file_path)

#         # Subset the data for the specified bounding box
#         subset_data = dataset.sel(lon=slice(lon_min, lon_max),
#                                   lat=slice(lat_min, lat_max))

#         # Subset only the 'sst' variable
#         sst_data = subset_data['sst']

#         # Append the subsetted 'sst' data to the list
#         subset_data_list.append(sst_data)

#         # # Subset the data for the specified time range (if provided)
#         # if time_range is not None:
#         # data = data.sel(time=slice(*time_range))

#         # Append the subsetted 'sst' data to the list
#         subset_data_list.append(sst_data)

#         # Close the file
#         dataset.close()

#     # Merge all the subsetted datasets into a single dataset
#     merged_data = xr.concat(subset_data_list, dim='time')

#     # # Save the merged data to a file if save_path is provided
#     # if save_path:
#     #     merged_data.to_netcdf(save_path)

#     return merged_data


# # Example usage
# file_paths = [
#     'sst.day.mean.2005.nc',
#     'sst.day.mean.2006.nc',
#     # 'sst.day.mean.2007.nc',
#     # 'sst.day.mean.2008.nc',
#     # 'sst.day.mean.2009.nc',
#     # 'sst.day.mean.2010.nc',
#     # 'sst.day.mean.2011.nc',
#     # 'sst.day.mean.2012.nc',
#     # 'sst.day.mean.2013.nc',
# ]

# lon_min, lon_max = 169, 216
# lat_min, lat_max = 29.5, 45.5
# # time_range = ('1982-01-01', '2014-01-01')
# save_path = "merged_sst_2005_06.nc"


# merged_data = merge_subset_sst_data(
#     file_paths, lon_min, lon_max, lat_min, lat_max)


# merged_data.to_netcdf(save_path)


# merged_data.to_netcdf(save_path)


# # Open one of the NetCDF files to check its structure
# example_dataset = xr.open_dataset(file_paths[8])

# # Print the dataset information
# print(example_dataset)

# # Check if the 'lat' variable exists in the dataset
# if 'lat' not in example_dataset.variables:
#     print("Latitude variable ('lat') not found in the dataset.")

# # Check if the 'lon' variable exists in the dataset
# if 'lon' not in example_dataset.variables:
#     print("Longitude variable ('lon') not found in the dataset.")

# # Check if the 'time' variable exists in the dataset
# if 'time' not in example_dataset.variables:
#     print("Time variable ('time') not found in the dataset.")

# # Check the bounding box coordinates against the dataset's latitude and longitude ranges
# print("Latitude range:", example_dataset['lat'].min(
# ).values, example_dataset['lat'].max().values)
# print("Longitude range:", example_dataset['lon'].min(
# ).values, example_dataset['lon'].max().values)

# # Close the example dataset
# example_dataset.close()


# # Load external SST data
# dataset = xr.open_dataset("SST/sst.wkmean.1990-present.nc")

# # Define bounding box coordinates for the Mediterranean Sea
# # You may need to adjust these coordinates based on your specific requirements
# lon_min, lon_max = 169, 216  # Longitude range
# lat_min, lat_max = 45.5, 29.5  # Latitude range

# # Subset the data for the Mediterranean Sea
# data = dataset.sel(lon=slice(lon_min, lon_max), lat=slice(lat_min, lat_max))

# # You can further narrow down the time range if needed
# data = data.sel(time=slice('1982-01-01', '2014-01-01'))


# import xarray as xr

# data_dir = "/Users/annaolsen/Desktop/Speciale/DS_thesis/data/SST/Daily"

# os.chdir(data_dir)

# # List the filenames of the NetCDF files you want to merge
# file_list = ['sst.day.mean.2009.nc', 'sst.day.mean.2010.nc',
#              'sst.day.mean.2011.nc', 'sst.day.mean.2012.nc',
#              'sst.day.mean.2013.nc'
#              ]

# # Open each NetCDF file and load them into xarray Dataset objects
# datasets = [xr.open_dataset(filename) for filename in file_list]

# # Merge the datasets into one
# merged_dataset = xr.concat(datasets, dim='time')  # Assuming time is the dimension along which you want to concatenate

# # Close the individual datasets to release resources
# for dataset in datasets:
#     dataset.close()

# # Save the merged dataset to a new NetCDF file
# merged_dataset.to_netcdf('sst_day_2009-2010.nc')

# # Close the merged dataset
# merged_dataset.close()

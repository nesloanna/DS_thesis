import pandas as pd
import os
import xarray as xr
import numpy as np


import pprint
pp = pprint.PrettyPrinter(indent=4)


data_dir = "/Users/annaolsen/Desktop/Speciale/DS_thesis/data/SST/Daily"

os.chdir(data_dir)
print(os.getcwd())


def merge_subset_sst_data(file_paths, lon_min, lon_max, lat_min, lat_max):
    """
    Merge and subset SST data from multiple files based on the given bounding box coordinates and time range.

    Parameters:
        file_paths (list): List of file paths containing SST data.
        lon_min (float): Minimum longitude of the bounding box.
        lon_max (float): Maximum longitude of the bounding box.
        lat_min (float): Minimum latitude of the bounding box.
        lat_max (float): Maximum latitude of the bounding box.
        time_range (tuple, optional): Tuple specifying the start and end dates for the time range (in the format 'YYYY-MM-DD'). Defaults to None.

    Returns:
        merged_data (xarray.Dataset): Merged and subsetted SST data.

    """
    # Initialize an empty list to store individual subsets
    subset_data_list = []

    # Loop through each file path
    for file_path in file_paths:
        # Load external SST data
        dataset = xr.open_dataset(file_path)

        # Subset the data for the specified bounding box
        subset_data = dataset.sel(lon=slice(lon_min, lon_max),
                                  lat=slice(lat_min, lat_max))

        # Subset only the 'sst' variable
        sst_data = subset_data['sst']

        # Append the subsetted 'sst' data to the list
        subset_data_list.append(sst_data)

        # # Subset the data for the specified time range (if provided)
        # if time_range is not None:
        # data = data.sel(time=slice(*time_range))

        # Append the subsetted 'sst' data to the list
        subset_data_list.append(sst_data)

        # Close the file
        dataset.close()

    # Merge all the subsetted datasets into a single dataset
    merged_data = xr.concat(subset_data_list, dim='time')

    # # Save the merged data to a file if save_path is provided
    # if save_path:
    #     merged_data.to_netcdf(save_path)

    return merged_data


# Example usage
file_paths = [
    'sst.day.mean.2005.nc',
    'sst.day.mean.2006.nc',
    # 'sst.day.mean.2007.nc',
    # 'sst.day.mean.2008.nc',
    # 'sst.day.mean.2009.nc',
    # 'sst.day.mean.2010.nc',
    # 'sst.day.mean.2011.nc',
    # 'sst.day.mean.2012.nc',
    # 'sst.day.mean.2013.nc',
]

lon_min, lon_max = 169, 216
lat_min, lat_max = 29.5, 45.5
# time_range = ('1982-01-01', '2014-01-01')
save_path = "merged_sst_2005_06.nc"

merged_data = merge_subset_sst_data(
    file_paths, lon_min, lon_max, lat_min, lat_max)


merged_data.to_netcdf(save_path)

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

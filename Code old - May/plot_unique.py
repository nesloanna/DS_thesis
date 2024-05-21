import geopandas as gpd
import numpy as np
import xarray as xr
import pandas as pd
import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
# %matplotlib widget

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df_meso = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")

# New column names for Meso SL
new_column_names = {
    'Sample ID (TARA_barcode#, registered at ...)': 'Sample ID (TARA_barcode#)',
    'Station (TARA_station#, registered at ...)': 'Station'
}

# Rename the columns
df_meso = df_meso.rename(columns=new_column_names)

# Find unique sample IDs
ids_df_meso = set(df_meso["Sample ID (TARA_barcode#)"])
ids_df_depth = set(df_depth["Sample ID (TARA_barcode#)"])

# Find the Sample IDs that are not common between the DataFrames
unique_ids_meso = ids_df_meso - ids_df_depth
unique_ids_depth = ids_df_depth - ids_df_meso


# print("Unique IDs meso:", len(unique_ids_meso))
# print("Unique IDs depth:", len(unique_ids_depth))
# print()
# print("Original shape of meso:", df_meso.shape)
# print("Original shape of depth:", df_depth.shape)
# print()


# Filter unique IDs from df_meso
meso_df = df_meso[df_meso["Sample ID (TARA_barcode#)"].isin(
    unique_ids_meso)]

# Filter unique IDs from df_bio
depth_df = df_depth[df_depth["Sample ID (TARA_barcode#)"].isin(
    unique_ids_depth)]

# # Display the lengths of the unique dataframes
# print("Shape of unique meso df:", unique_df_meso.shape)
# print("Shape of unique depth df:", unique_df_depth.shape)


# Combine "Lat" and "Lon" columns into a new "Location" column
meso_df['Location'] = meso_df['Latitude'].astype(
    str) + ', ' + meso_df['Longitude'].astype(str)

depth_df['Location'] = depth_df['Latitude'].astype(
    str) + ', ' + depth_df['Longitude'].astype(str)


meso_locations = set(meso_df["Location"])
depth_locations = set(depth_df["Location"])

unique_meso_loc = meso_locations - depth_locations
unique_depth_loc = depth_locations - meso_locations

print(unique_meso_loc)
print(unique_depth_loc)

# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# fig, ax = plt.subplots(figsize=(15, 15))

# # Plot world map
# world.plot(ax=ax, color='lightgray', edgecolor='black')

# # Plot original points
# ax.scatter(meso_df['Longitude'], meso_df['Latitude'],
#            color='mediumblue', label='Meso', s=12)

# # Plot closest match points
# # ax.scatter(depth_df['Longitude'], depth_df['Latitude'],
# #            color='darkorange', label='Depth', s=12)

# # Set title
# ax.set_title('Unique IDS (meso and depth)')
# # Add legend
# ax.legend()

# plt.show()

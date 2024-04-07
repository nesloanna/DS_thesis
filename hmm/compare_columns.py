import pandas as pd
from tqdm import tqdm
import os

import pprint
pp = pprint.PrettyPrinter(indent=4)


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


df = pd.read_csv("Tara_merged_NEW_sorted.csv")
df_bio = pd.read_csv("Tara_Biodiversity.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
df_meso = pd.read_csv("Tara_Environmental_Mesoscale.csv")
df_meso_SL = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")


# Get the unique Sample IDs from each DataFrame
print()
ids_df_bio = set(df_bio["Sample ID (TARA_barcode#)"])
ids_df_depth = set(df_depth["Sample ID (TARA_barcode#)"])
ids_df_meso = set(df_meso["Sample ID (TARA_barcode#)"])
ids_df_meso_SL = set(
    df_meso_SL["Sample ID (TARA_barcode#, registered at ...)"])

# Find the Sample IDs that are not common between the DataFrames
unique_ids_bio = ids_df_bio - ids_df_depth - ids_df_meso
unique_ids_depth = ids_df_depth - ids_df_bio - ids_df_meso
unique_ids_meso = ids_df_meso - ids_df_bio - ids_df_depth
unique_ids_meso_SL = ids_df_meso_SL - ids_df_bio - ids_df_depth

unique_bio_meso = ids_df_bio - ids_df_meso
unique_depth_meso = ids_df_depth - ids_df_meso
unique_depth_mesoSL = ids_df_depth - ids_df_meso_SL


# print(f"\nUnique IDs in Meso SL (not Depth/Bio):\n{unique_ids_meso_SL}")
# print(f"\nUnique IDs in Depth (not in Meso SL):\n{unique_depth_mesoSL}")


# Define the set of sample IDs to be removed
ids_to_remove_meso = unique_ids_meso_SL

# Remove rows with the specified sample IDs
df_meso_SL = df_meso_SL[~df_meso_SL['Sample ID (TARA_barcode#, registered at ...)'].isin(
    ids_to_remove_meso)]

# Output the resulting DataFrame
print(f"New shape of df_meso: {df_meso_SL.shape}")


ids_to_remove_depth = unique_depth_mesoSL

# Remove rows with the specified sample IDs
df_depth = df_depth[~df_depth['Sample ID (TARA_barcode#)'].isin(
    ids_to_remove_depth)]

# Output the resulting DataFrame
print(f"New shape of df_depth: {df_depth.shape}")


# new_col_names = {
#     'Campaign (TARA_event-datetime_station#_...)': 'Campaign',
#     'Event (TARA_event-datetime_station#_...)': 'Event',
#     'Date/Time (TARA_event-datetime_station#_...)': 'Date/Time',
#     'Latitude (TARA_event-datetime_station#_...)': 'Latitude',
#     'Longitude (TARA_event-datetime_station#_...)': 'Longitude',
#     'Env feature ([abbreviation] description (E...)': 'Env feature (abbreviation)',
#     'Moon phase proportion (at the sampling location and ...)': 'Moon phase proportion (indicates the proportion of i...)',
#     'SSD [min] (at the sampling location and ...)': 'SSD [min] (day length)',
#     'NPP C [mg/m**2/day] (at the sampling location for ...)': 'NPP C [mg/m**2/day] (for a period of 8 days around...)',
#     'NPP C [mg/m**2/day] (at the sampling location for ...).1': 'NPP C [mg/m**2/day] (for a period of 30 days aroun...)',
#     'MLE [1/day] (at the sampling location and ...)': 'MLE [1/day] (indicates the presence of a t...)',
#     'OW (at the sampling location and ...)': 'OW (indicates the presence of an ...)',
#     'Season (at the sampling location and ...)': 'Season (spring, summer, autumn, or wi...)',
#     'Season (at the sampling location and ...).1': 'Season (early, middle, or late)',
#     'u [cm/s] (at the sampling location and ...)': "u [cm/s] (Calculated (d'Ovidio et al. 2...)",
#     'v [cm/s] (at the sampling location and ...)': "v [cm/s] (Calculated (d'Ovidio et al. 2...)",
#     'RT [days] (of the water mass at the samp...)': 'RT [days] (of the water mass. Values>30 ...)',
#     'SST grad h [°C/100 km] (at the sampling location and ...)': "SST grad h [°C/100 km] (Calculated (d'Ovidio et al. 2...)",
#     'PAR [mol quanta/m**2/day] (at the sampling location for ...)': 'PAR [mol quanta/m**2/day] (for a period of 8 days around...)',
#     'PAR [mol quanta/m**2/day] (at the sampling location for ...).1': 'PAR [mol quanta/m**2/day] (for a period of 30 days aroun...)',
#     'fCDOM [ppb (QSE)] (at the sampling location and ...)': 'fCDOM [ppb (QSE)] (at the sampling location, exp...)'
# }

new_column_names = {
    'Sample ID (TARA_barcode#, registered at ...)': 'Sample ID (TARA_barcode#)',
    'Station (TARA_station#, registered at ...)': 'Station (TARA_station#)',
    'Moon phase proportion (at the sampling location and ...)': 'Moon phase proportion (indicates the proportion of i...)',
    'SSD [min] (at the sampling location and ...)': 'SSD [min] (day length)',
    'NPP C [mg/m**2/day] (at the sampling location for ...)': 'NPP C [mg/m**2/day] (for a period of 30 days aroun...)',

}


# Rename the columns
df_meso_SL = df_meso_SL.rename(columns=new_column_names)


# Get the intersection of column names between the two dataframes
common_columns = set(df_meso_SL.columns) & set(df_depth.columns)

# Iterate over the common columns
for column_name in tqdm(common_columns):
    # Convert column into list
    meso_list = df_meso_SL[column_name].tolist()
    depth_list = df_depth[column_name].tolist()

    # Find elements unique to each list
    difference_meso_depth = [
        item for item in meso_list if item not in depth_list]
    difference_depth_meso = [
        item for item in depth_list if item not in meso_list]

    # Print the results
    print(f"Column: {column_name}")
    print(f"Elements unique to df_meso: {difference_meso_depth}")
    print(f"Elements unique to df_depth: {difference_depth_meso}")
    print()


def column_stats(df, column_name):

    nan_values = df[column_name].isna().sum()
    cleaned_column = df[column_name].dropna()

    # Calculate mean of a column
    mean_value = cleaned_column.mean()

    # Calculate minimum value of a column
    min_value = cleaned_column.min()

    # Calculate maximum value of a column
    max_value = cleaned_column.max()

    # Calculate median of a column
    median_value = cleaned_column.median()

    # Calculate standard deviation of a column
    std_deviation = cleaned_column.std()

    # Calculate sum of values in a column
    sum_value = cleaned_column.sum()

    print("NaN-values:", nan_values)
    print("Mean:", mean_value)
    print("Minimum:", min_value)
    print("Maximum:", max_value)
    print("Median:", median_value)
    print("Standard Deviation:", std_deviation)
    print("Sum:", sum_value)


# column_stats(df_meso, "MLE [1/day] (indicates the presence of a t...)")

import pandas as pd
from difflib import SequenceMatcher
import os
from itertools import chain
from collections import defaultdict
import pprint
from tqdm import tqdm
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
ids_df_meso_SL = set(df_meso_SL["Sample ID (TARA_barcode#)"])

# Find the Sample IDs that are not common between the DataFrames
unique_ids_bio = ids_df_bio - ids_df_depth - ids_df_meso
unique_ids_depth = ids_df_depth - ids_df_bio - ids_df_meso
unique_ids_meso = ids_df_meso - ids_df_bio - ids_df_depth
unique_ids_meso_SL = ids_df_meso_SL - ids_df_bio - ids_df_depth

unique_bio_meso = ids_df_bio - ids_df_meso
unique_depth_meso = ids_df_depth - ids_df_meso

print(f"Sample IDs in bio and NOT in meso: {len(unique_bio_meso)}")
print(f"Sample IDs in depth and NOT in meso: {len(unique_depth_meso)}")
print(f"Sample IDs in meso and NOT in bio or depth: {len(unique_ids_meso)}")
print(
    f"Sample IDs in meso (SL) and NOT in bio or depth: {len(unique_ids_meso_SL)}")


print(f"\nUnique IDs in mesoscale:\n{unique_ids_meso}")
print(f"\nUnique IDs in depth:\n{unique_depth_meso}")


# Define the set of sample IDs to be removed
ids_to_remove_meso = {'TARA_X000000401', 'TARA_Z000000200', 'TARA_Z000000075',
                      'TARA_X000001253', 'TARA_X000000962', 'TARA_X000000583',
                      'TARA_Z000000201', 'TARA_X000000316', 'TARA_Z000000207',
                      'TARA_X000000558', 'TARA_Z000000174', 'TARA_Z000000206',
                      'TARA_Z000000164', 'TARA_Z000000187', 'TARA_X000000505',
                      'TARA_Z000000210', 'TARA_Z000000190', 'TARA_Z000000186',
                      'TARA_Z000000176', 'TARA_Z000000209', 'TARA_G100004395',
                      'TARA_X000000817', 'TARA_Z000000196', 'TARA_X000000642',
                      'TARA_Z000000175', 'TARA_X000000698', 'TARA_Z000000184',
                      'TARA_G000001726c', 'TARA_Z000000179', 'TARA_X000001050',
                      'TARA_Z000000211', 'TARA_Z000000189', 'TARA_X000000397',
                      'TARA_Z000000194', 'TARA_Z000000198', 'TARA_Z000000177',
                      'TARA_Z000000202', 'TARA_Z000000214', 'TARA_Z000000195',
                      'TARA_G100019014', 'TARA_Z000000180', 'TARA_X000000399',
                      'TARA_Z000000204', 'TARA_Z000000188', 'TARA_G100004396',
                      'TARA_Z000000193', 'TARA_X000000613', 'TARA_X000001228',
                      'TARA_G100019013', 'TARA_Z000000182', 'TARA_X000000634',
                      'TARA_Z000000074', 'TARA_Z000000205', 'TARA_Z000000213',
                      'TARA_X000000334', 'TARA_X000000495', 'TARA_X000001155',
                      'TARA_Z000000203', 'TARA_Z000000181', 'TARA_Z000000130',
                      'TARA_X000000960', 'TARA_X000001046', 'TARA_X000000403',
                      'TARA_X000000617', 'TARA_Z000000178', 'TARA_Z000000212',
                      'TARA_Z000000192', 'TARA_G100008842', 'TARA_X000000633',
                      'TARA_Z000000215', 'TARA_X000000560', 'TARA_Z000000183',
                      'TARA_Z000000197', 'TARA_X000001276', 'TARA_Z000000185',
                      'TARA_Z000000217', 'TARA_X000001230', 'TARA_X000001226'}

# Remove rows with the specified sample IDs
df_meso = df_meso[~df_meso['Sample ID (TARA_barcode#)'].isin(
    ids_to_remove_meso)]

# Output the resulting DataFrame
print(f"New shape of df_meso: {df_meso.shape}")


ids_to_remove_depth = {'TARA_X000000052', 'TARA_X000000699', 'TARA_X000000559',
                       'TARA_X000000088', 'TARA_X000001051', 'TARA_X000000058',
                       'TARA_X000000069', 'TARA_X000000115', 'TARA_X000000098',
                       'TARA_X000000482', 'TARA_X000000147', 'TARA_X000000054',
                       'TARA_X000000149', 'TARA_X000000152', 'TARA_X000000143',
                       'TARA_X000000017', 'TARA_X000001231', 'TARA_X000000818',
                       'TARA_G100008842b', 'TARA_X000000145', 'TARA_X000000018',
                       'TARA_X000000030', 'TARA_X000000398', 'TARA_X000001047',
                       'TARA_X000001227', 'TARA_X000001254', 'TARA_X000000101',
                       'TARA_X000000104', 'TARA_X000000050', 'TARA_X000000716',
                       'TARA_X000000031', 'TARA_X000001229', 'TARA_X000000402',
                       'TARA_X000000150', 'TARA_X000000618', 'TARA_X000000717',
                       'TARA_X000000146', 'TARA_X000000029', 'TARA_X000000070',
                       'TARA_X000000963', 'TARA_X000000103', 'TARA_X000000404',
                       'TARA_G100000282', 'TARA_X000000614', 'TARA_X000000064',
                       'TARA_X000000561', 'TARA_X000000056', 'TARA_X000000584',
                       'TARA_Z000000072', 'TARA_X000000122', 'TARA_X000000097',
                       'TARA_X000000062', 'TARA_X000001156', 'TARA_X000000055',
                       'TARA_X000000060', 'TARA_X000000335', 'TARA_X000000099',
                       'TARA_X000000028', 'TARA_G100008842a', 'TARA_X000000100',
                       'TARA_X000000643', 'TARA_X000000506', 'TARA_X000000032',
                       'TARA_X000000048', 'TARA_X000000148', 'TARA_X000000120',
                       'TARA_X000000144', 'TARA_X000000102', 'TARA_X000000121',
                       'TARA_X000000027', 'TARA_X000000961', 'TARA_X000000151',
                       'TARA_X000000400'}

# Remove rows with the specified sample IDs
df_depth = df_depth[~df_depth['Sample ID (TARA_barcode#)'].isin(
    ids_to_remove_depth)]

# Output the resulting DataFrame
print(f"New shape of df_depth: {df_depth.shape}")


new_column_names = {
    'Campaign (TARA_event-datetime_station#_...)': 'Campaign',
    'Event (TARA_event-datetime_station#_...)': 'Event',
    'Date/Time (TARA_event-datetime_station#_...)': 'Date/Time',
    'Latitude (TARA_event-datetime_station#_...)': 'Latitude',
    'Longitude (TARA_event-datetime_station#_...)': 'Longitude',
    'Env feature ([abbreviation] description (E...)': 'Env feature (abbreviation)',
    'Moon phase proportion (at the sampling location and ...)': 'Moon phase proportion (indicates the proportion of i...)',
    'SSD [min] (at the sampling location and ...)': 'SSD [min] (day length)',
    'NPP C [mg/m**2/day] (at the sampling location for ...)': 'NPP C [mg/m**2/day] (for a period of 8 days around...)',
    'NPP C [mg/m**2/day] (at the sampling location for ...).1': 'NPP C [mg/m**2/day] (for a period of 30 days aroun...)',
    'MLE [1/day] (at the sampling location and ...)': 'MLE [1/day] (indicates the presence of a t...)',
    'OW (at the sampling location and ...)': 'OW (indicates the presence of an ...)',
    'Season (at the sampling location and ...)': 'Season (spring, summer, autumn, or wi...)',
    'Season (at the sampling location and ...).1': 'Season (early, middle, or late)',
    'u [cm/s] (at the sampling location and ...)': "u [cm/s] (Calculated (d'Ovidio et al. 2...)",
    'v [cm/s] (at the sampling location and ...)': "v [cm/s] (Calculated (d'Ovidio et al. 2...)",
    'RT [days] (of the water mass at the samp...)': 'RT [days] (of the water mass. Values>30 ...)',
    'SST grad h [°C/100 km] (at the sampling location and ...)': "SST grad h [°C/100 km] (Calculated (d'Ovidio et al. 2...)",
    'PAR [mol quanta/m**2/day] (at the sampling location for ...)': 'PAR [mol quanta/m**2/day] (for a period of 8 days around...)',
    'PAR [mol quanta/m**2/day] (at the sampling location for ...).1': 'PAR [mol quanta/m**2/day] (for a period of 30 days aroun...)',
    'fCDOM [ppb (QSE)] (at the sampling location and ...)': 'fCDOM [ppb (QSE)] (at the sampling location, exp...)'
}

# Rename the columns
df_meso = df_meso.rename(columns=new_column_names)


# Get the intersection of column names between the two dataframes
common_columns = set(df_meso.columns) & set(df_depth.columns)

# Iterate over the common columns
for column_name in tqdm(common_columns):
    # Convert column into list
    meso_list = df_meso[column_name].tolist()
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

import pandas as pd
import os


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


df_bio = pd.read_csv("Tara_Biodiversity.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
df_meso = pd.read_csv("Tara_Environmental_Mesoscale.csv")


new_column_names = {
    'Campaign (TARA_event-datetime_station#_...)': 'Campaign',
    'Event (TARA_event-datetime_station#_...)': 'Event',
    'Date/Time (TARA_event-datetime_station#_...)': 'Date/Time',
    'Latitude (TARA_event-datetime_station#_...)': 'Latitude',
    'Longitude (TARA_event-datetime_station#_...)': 'Longitude',
    'Moon phase proportion (at the sampling location and ...)': 'Moon phase proportion (indicates the proportion of i...)',
    'SSD [min] (at the sampling location and ...)': 'SSD [min] (day length)'
}

# Rename the columns
df_meso = df_meso.rename(columns=new_column_names)


# Initialize a list to store the names of identical columns
identical_columns = []

# Iterate over the columns of df_bio
for col in df_bio.columns:
    # Check if the column exists in df_depth and if its values are identical
    if col in df_depth.columns and (df_bio[col] == df_depth[col]).all():
        identical_columns.append(col)

# Print the list of identical columns
if identical_columns:
    print("Identical columns found:", identical_columns)
else:
    print("No identical columns found.")


# Columns we don't want to duplicate
duplicate_cols = ['Sample ID (TARA_barcode#)', 'Campaign',
                  'Station (TARA_station#)', 'Event',
                  'Env feature (abbreviation)',
                  'Env feature (full name (ENVO:ID), terms re...)']

# Merge df_bio and df_depth
df_merged = pd.merge(df_bio, df_depth, on=duplicate_cols, how="inner")

print(df_merged.shape)

# Merge df_merged and df_meso
df_merged = pd.merge(df_merged, df_meso, on="Sample ID (TARA_barcode#)",
                     how="outer")

print(df_merged.shape)


# Sort all columns (but Sample ID) alphabetically
columns_to_sort = sorted(
    [col for col in df_merged.columns if col not in ['Sample ID (TARA_barcode#)']])

# Reorder the columns
desired_columns = ['Sample ID (TARA_barcode#)'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df_merged = df_merged[desired_columns]

# Save merged and sorted dataframe to csv
df_merged.to_csv("Tara_merged_NEW_sorted.csv", index=False)

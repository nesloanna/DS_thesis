import pandas as pd
import os


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


df_bio = pd.read_csv("Tara_Biodiversity.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
df_meso_SL = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")

# Find unique sample IDs
ids_df_depth = set(df_depth["Sample ID (TARA_barcode#)"])
ids_df_meso = set(
    df_meso_SL["Sample ID (TARA_barcode#, registered at ...)"])

# Find the Sample IDs that are not common between the DataFrames
unique_ids_depth = ids_df_depth - ids_df_meso
unique_ids_meso = ids_df_meso - ids_df_depth


new_column_names = {
    'Sample ID (TARA_barcode#, registered at ...)': 'Sample ID (TARA_barcode#)',
    'Station (TARA_station#, registered at ...)': 'Station (TARA_station#)'
}

# Rename the columns
df_meso_SL = df_meso_SL.rename(columns=new_column_names)


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

print("Shape after merging bio and depth:", df_merged.shape)

new_meso_ids = sorted(list(unique_ids_meso))
df_meso_ids = pd.DataFrame({'Sample ID (TARA_barcode#)': new_meso_ids})

df_merged = pd.concat([df_merged, df_meso_ids], ignore_index=True)
print("Shape after adding meso IDs:", df_merged.shape)

# Reset index after concatenating
df_merged = df_merged.reset_index(drop=True)

new_depth_ids = sorted(list(unique_ids_depth))
df_depth_ids = pd.DataFrame({'Sample ID (TARA_barcode#)': new_depth_ids})
df_meso_SL = pd.concat([df_meso_SL, df_depth_ids], ignore_index=True)
print("Shape (meso) after adding depth IDs:", df_meso_SL.shape)

# Reset index after concatenating
df_meso_SL = df_meso_SL.reset_index(drop=True)

df_merged = df_merged.sort_values(by='Sample ID (TARA_barcode#)')
df_meso_SL = df_meso_SL.sort_values(by='Sample ID (TARA_barcode#)')

duplicate_cols_meso = ['Sample ID (TARA_barcode#)', 'Campaign',
                       'Station (TARA_station#)', 'Event', 'Basis',
                       'Date/Time', 'Method/Device']

# Merge df_merged and df_meso
df_merged = pd.merge(df_merged, df_meso_SL, on='Sample ID (TARA_barcode#)',
                     how="inner")

print(df_merged.shape)


# Sort all columns (but Sample ID) alphabetically
# columns_to_sort = sorted(
#     [col for col in df_merged.columns if col not in ['Sample ID (TARA_barcode#)']])

# # Reorder the columns
# desired_columns = ['Sample ID (TARA_barcode#)'] + columns_to_sort

# # Create a new dataframe with the desired column order, sorted alphabetically
# df_merged = df_merged[desired_columns]

# # Save merged and sorted dataframe to csv
# df_merged.to_csv("Tara_merged_mesoSL.csv", index=False)

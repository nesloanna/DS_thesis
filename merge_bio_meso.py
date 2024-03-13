import pandas as pd
import os


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df_bio = pd.read_csv("Tara_Biodiversity.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
df_meso = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")

# New column names for Meso SL
new_column_names = {
    'Sample ID (TARA_barcode#, registered at ...)': 'Sample ID (TARA_barcode#)',
    'Station (TARA_station#, registered at ...)': 'Station (TARA_station#)'
}

# Rename the columns
df_meso = df_meso.rename(columns=new_column_names)

# Find unique sample IDs
ids_df_bio = set(df_bio["Sample ID (TARA_barcode#)"])
ids_df_meso = set(df_meso["Sample ID (TARA_barcode#)"])
ids_df_depth = set(df_depth["Sample ID (TARA_barcode#)"])

# Find the Sample IDs that are not common between the DataFrames
unique_ids_bio = ids_df_bio - ids_df_meso
unique_ids_meso = ids_df_meso - ids_df_bio
unique_ids_depth = ids_df_depth - ids_df_meso

print("Unique IDs bio:", len(unique_ids_bio))
print("Unique IDs meso:", len(unique_ids_meso))
print("Unique IDs depth:", len(unique_ids_depth))

print("Original shape of bio:", df_bio.shape)
print("Original shape of meso:", df_meso.shape)


# Filter unique IDs from df_bio
unique_df_bio = df_bio[df_bio["Sample ID (TARA_barcode#)"].isin(
    unique_ids_bio)]

# Filter unique IDs from df_meso
unique_df_meso = df_meso[df_meso["Sample ID (TARA_barcode#)"].isin(
    unique_ids_meso)]

# Filter unique IDs from df_meso
unique_df_depth = df_depth[df_depth["Sample ID (TARA_barcode#)"].isin(
    unique_ids_depth)]

# Display the lengths of the unique dataframes
print("Shape of unique bio df:", unique_df_bio.shape)
print("Shape of unique meso df:", unique_df_meso.shape)
print("Shape of unique depth df:", unique_df_depth.shape)

# unique_df_bio.to_csv("Bio_Unique.csv", index=False)
# unique_df_meso.to_csv("Meso_Unique.csv", index=False)
# unique_df_depth.to_csv("Depth_Unique.csv", index=False)

columns_to_keep = ['Sample ID (TARA_barcode#)',
                   '[PO4]3- [µmol/l] (in the selected environmental...)']
df_depth = df_depth[columns_to_keep]

# ------- Add extra IDs -------

new_ids_for_bio = sorted(list(unique_ids_meso))
df_new_bio_ids = pd.DataFrame(
    {'Sample ID (TARA_barcode#)': new_ids_for_bio})

df_bio = pd.merge(df_bio, df_depth,
                  on='Sample ID (TARA_barcode#)', how="inner")

df_bio = pd.concat([df_bio, df_new_bio_ids], ignore_index=True)
df_bio = df_bio.sort_values(by='Sample ID (TARA_barcode#)')

print("Shape (bio) after adding meso IDs:", df_bio.shape)


# Create a boolean mask where IDs are in the list of IDs to remove
mask = df_bio['Sample ID (TARA_barcode#)'].isin(unique_ids_bio)

# Invert the mask to keep the rows that are not in the list of IDs to remove
df_bio = df_bio[~mask]

# Reset index after concatenating
df_bio = df_bio.reset_index(drop=True)

print("Shape (bio) after removing unique IDs:", df_bio.shape)

# Initialize a list to store the names of identical columns
identical_columns = []

# # Iterate over the columns of df_bio
# for col in df_bio.columns:
#     # Check if the column exists in df_depth and if its values are identical
#     if col in df_depth.columns and (df_bio[col] == df_depth[col]).all():
#         identical_columns.append(col)

# # Print the list of identical columns
# if identical_columns:
#     print("Identical columns found:", identical_columns)
# else:
#     print("No identical columns found.")


df_bio = df_bio.sort_values(by='Sample ID (TARA_barcode#)')
df_meso = df_meso.sort_values(by='Sample ID (TARA_barcode#)')

columns_to_drop = ['Campaign', 'Station (TARA_station#)', 'Event',
                   'Env feature (abbreviation)',
                   'Env feature (full name (ENVO:ID), terms re...)']

df_bio = df_bio.drop(columns=columns_to_drop)

# Columns we don't want to duplicate
duplicate_cols = ['Sample ID (TARA_barcode#)']

# Merge df_bio and df_meso
df_merged = pd.merge(df_meso, df_bio, on=duplicate_cols, how="inner")

print("Shape after merging bio and meso:", df_merged.shape)

# # df_merged = df_merged.sort_values(by='Sample ID (TARA_barcode#)')
# # df_meso_SL = df_meso_SL.sort_values(by='Sample ID (TARA_barcode#)')

# duplicate_cols_meso = ['Sample ID (TARA_barcode#)', 'Campaign',
#                        'Station (TARA_station#)', 'Event', 'Basis',
#                        'Date/Time', 'Method/Device']

# # Merge df_merged and df_meso
# df_merged = pd.merge(df_meso, df_merged, on='Sample ID (TARA_barcode#)',
#                      how="outer", suffixes=['_D', '_M'])

# print(df_merged.shape)


# # Sort all columns (but Sample ID) alphabetically
# columns_to_sort = sorted(
#     [col for col in df_merged.columns if col not in ['Sample ID (TARA_barcode#)']])

# # Reorder the columns
# desired_columns = ['Sample ID (TARA_barcode#)'] + columns_to_sort

# # Create a new dataframe with the desired column order, sorted alphabetically
# df_merged = df_merged[desired_columns]

# # Print the updated dataframe
# print(df_merged.shape)


# # Save merged and sorted dataframe to csv
# df_merged.to_csv("Tara_merged_BM.csv", index=False)

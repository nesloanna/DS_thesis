import pandas as pd
import os


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df_bio = pd.read_csv("Tara_Biodiversity.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
df_meso_SL = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")

# New column names for Meso SL
new_column_names = {
    'Sample ID (TARA_barcode#, registered at ...)': 'Sample ID (TARA_barcode#)',
    'Station (TARA_station#, registered at ...)': 'Station (TARA_station#)'
}

# Rename the columns
df_meso_SL = df_meso_SL.rename(columns=new_column_names)

# Find unique sample IDs
ids_df_depth = set(df_depth["Sample ID (TARA_barcode#)"])
ids_df_meso = set(df_meso_SL["Sample ID (TARA_barcode#)"])

# Find the Sample IDs that are not common between the DataFrames
unique_ids_depth = ids_df_depth - ids_df_meso
unique_ids_meso = ids_df_meso - ids_df_depth


print("Original shape of meso:", df_meso_SL.shape)


# ------- Add extra IDs -------

new_ids_for_depth = sorted(list(unique_ids_meso))
df_new_depth_ids = pd.DataFrame(
    {'Sample ID (TARA_barcode#)': new_ids_for_depth})

df_depth = pd.concat([df_depth, df_new_depth_ids], ignore_index=True)
df_depth = df_depth.sort_values(by='Sample ID (TARA_barcode#)')

df_bio = pd.concat([df_bio, df_new_depth_ids], ignore_index=True)
df_bio = df_bio.sort_values(by='Sample ID (TARA_barcode#)')

print("Shape (depth) after adding meso IDs:", df_depth.shape)
print("Shape (bio) after adding meso IDs:", df_bio.shape)

# Reset index after concatenating
df_depth = df_depth.reset_index(drop=True)
df_bio = df_bio.reset_index(drop=True)


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

# df_merged = df_merged.sort_values(by='Sample ID (TARA_barcode#)')
# df_meso_SL = df_meso_SL.sort_values(by='Sample ID (TARA_barcode#)')

duplicate_cols_meso = ['Sample ID (TARA_barcode#)', 'Campaign',
                       'Station (TARA_station#)', 'Event', 'Basis',
                       'Date/Time', 'Method/Device']

# Merge df_merged and df_meso
df_merged = pd.merge(df_meso_SL, df_merged, on='Sample ID (TARA_barcode#)',
                     how="outer", suffixes=['_D', '_M'])

print(df_merged.shape)

print(df_merged.shape)


# Set of columns to check
cols_to_check = ['Event_D', 'Event_M']


def handle_duplicate_cols(df, list_of_cols):

    # Initialize an empty list to store the values for the new column
    new_column = []

    # Loop through the set of columns
    for index, row in df.iterrows():
        value = None
        for col in list_of_cols:
            if pd.notna(row[col]):
                if value is None:
                    value = row[col]
                elif value != row[col]:
                    value = "?"
                    break
        new_column.append(value)

    return new_column


# Add the new column "Date" to the dataframe
df_merged['Event'] = handle_duplicate_cols(df_merged, ['Event_D', 'Event_M'])
df_merged['Station (TARA_station#)'] = handle_duplicate_cols(
    df_merged, ['Station (TARA_station#)_D', 'Station (TARA_station#)_M'])
df_merged['Date/Time'] = handle_duplicate_cols(
    df_merged, ['Date/Time_D', 'Date/Time_M'])
df_merged['Basis'] = handle_duplicate_cols(df_merged, ['Basis_D', 'Basis_M'])
df_merged['Campaign'] = handle_duplicate_cols(
    df_merged, ['Campaign_D', 'Campaign_M'])


# Sort all columns (but Sample ID) alphabetically
columns_to_sort = sorted(
    [col for col in df_merged.columns if col not in ['Sample ID (TARA_barcode#)']])

# Reorder the columns
desired_columns = ['Sample ID (TARA_barcode#)'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df_merged = df_merged[desired_columns]

# Print the updated dataframe
print(df_merged.shape)

# List of columns to drop
cols_to_drop = ['Event_D', 'Event_M', 'Station (TARA_station#)_D',
                'Station (TARA_station#)_M', 'Date/Time_D', 'Date/Time_M',
                'Basis_D', 'Basis_M', 'Campaign_D', 'Campaign_M']

# Drop the columns
df_merged = df_merged.drop(columns=cols_to_drop)

# Print the dataframe after dropping the columns
print(df_merged.shape)

# Save merged and sorted dataframe to csv
df_merged.to_csv("Tara_merged_mesoSL.csv", index=False)

import os
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Navigate to the 'data' folder
os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df_bio = pd.read_csv("Tara_Biodiversity.csv")
df_depth = pd.read_csv("Tara_Environmental_Depth.csv")
df_meso = pd.read_csv("Tara_Environmental_Mesoscale.csv")
df_meso_SL = pd.read_csv("Tara_Env_Meso_SampleLocation.csv")


# ---------------- Column names -------------------
# Extract column names from each dataframe
columns_bio = set(df_bio.columns)
columns_depth = set(df_depth.columns)
columns_meso = set(df_meso.columns)
columns_meso_SL = set(df_meso_SL.columns)

# Find unique columns for each dataframe
unique_columns_bio = columns_bio - columns_depth - columns_meso
unique_columns_depth = columns_depth - columns_bio - columns_meso
unique_columns_meso = columns_meso - columns_bio - columns_depth
unique_columns_meso_SL = columns_meso_SL - columns_bio - columns_depth
unique_mesoSL_meso = columns_meso_SL - columns_meso


unique_cols_dict = {"Bio": unique_columns_bio,
                    "Depth": unique_columns_depth,
                    "Meso": unique_columns_meso,
                    "Meso (SL)": unique_columns_meso_SL,
                    "Meso (SL) and not Meso": unique_mesoSL_meso}


for key, value in unique_cols_dict.items():
    print(f"\nUnique Columns in {key} ({len(value)}):")
    pp.pprint(value)


# ---------------- Sample IDs -------------------
# Extract Sample IDs from each dataframe
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

print(f"Sample IDs in bio and NOT in meso: {len(unique_bio_meso)}")
print(f"Sample IDs in depth and NOT in meso: {len(unique_depth_meso)}")
print(f"Sample IDs in meso and NOT in bio/depth: {len(unique_ids_meso)}")
print(
    f"Sample IDs in meso (SL) and NOT in bio/depth: {len(unique_ids_meso_SL)}")

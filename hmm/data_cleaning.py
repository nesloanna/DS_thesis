import pandas as pd
import os

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_merged_mesoSL.csv")

# Remove row with 'TARA_X000001277' as Sample ID (this ID causes trouble!)
df = df[df['Sample ID (TARA_barcode#)'] != 'TARA_X000001277']

# If you want to reset the index after dropping rows
df.reset_index(drop=True, inplace=True)


new_column_names = {'OS region ([abbreviation] full name (MRG...)_D': 'OS region_D',
                    'OS region ([abbreviation] full name (MRG...)_M': 'OS region_M'}

# Rename the columns
df = df.rename(columns=new_column_names)

meso_pattern = r'\[MRGID:(\d+)\]'
depth_pattern = r'\(MRGID:(\d+)\)'

# Extracting "(MRGID:[number])" part into a new column
df['OS MRGID_M'] = df['OS region_M'].str.extract(meso_pattern, expand=False)
df['OS MRGID_D'] = df['OS region_D'].str.extract(depth_pattern, expand=False)

# Removing the extracted part from the original column
df['OS region_M'] = df['OS region_M'].str.replace(meso_pattern, '', regex=True)
df['OS region_D'] = df['OS region_D'].str.replace(
    depth_pattern, '', regex=True)

df['OS region_M'] = df['OS region_M'].str.replace("(", "[")
df['OS region_M'] = df['OS region_M'].str.replace(")", "]")
df['OS region_M'] = df['OS region_M'].str.replace("[O]", "[NAO]")


def check_similar_cols(df, list_of_cols):

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


# Add new colums to the dataframe
df['Event'] = check_similar_cols(df, ['Event_D', 'Event_M'])
df['Station'] = check_similar_cols(
    df, ['Station (TARA_station#)_D', 'Station (TARA_station#)_M'])
df['Date/Time'] = check_similar_cols(df, ['Date/Time_D', 'Date/Time_M'])
df['Basis'] = check_similar_cols(df, ['Basis_D', 'Basis_M'])
df['Campaign'] = check_similar_cols(df, ['Campaign_D', 'Campaign_M'])
df['Latitude'] = check_similar_cols(df, ['Latitude_D', 'Latitude_M'])
df['Longitude'] = check_similar_cols(df, ['Longitude_D', 'Longitude_M'])
df['OS region'] = check_similar_cols(df, ['OS region_D', 'OS region_M'])
# df['Sunshine duration'] = check_similar_cols(
#     df, ['Sunshine duration_D', 'Sunshine duration_M'])
# df['NP carbon (30)'] = check_similar_cols(df, ['NPP C (30)_D', 'NPP C (30)_M'])
# df['Marine Biome'] = check_similar_cols(
#     df, ['MP biome (Longhurst (2007))_D', 'MP biome (Longhurst (2007))_M'])

# List of columns to drop
cols_to_drop = ['Event_D', 'Event_M', 'Station (TARA_station#)_D',
                'Station (TARA_station#)_M', 'Date/Time_D', 'Date/Time_M',
                'Basis_D', 'Basis_M', 'Campaign_D', 'Campaign_M',
                'Latitude_D', 'Latitude_M', 'Longitude_D', 'Longitude_M',
                'OS region_D', 'OS region_M'
                ]

# Drop the columns
df = df.drop(columns=cols_to_drop)

print(df.shape)


# Convert the 'DateTime' column to datetime format
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# Extract date and year into new columns
df['Date'] = df['Date/Time'].dt.date
df['Year'] = df['Date/Time'].dt.year

# print(df['Date'])
# print(df['Year'])

# Sort all columns (but Sample ID) alphabetically
columns_to_sort = sorted(
    [col for col in df.columns if col not in ['Sample ID (TARA_barcode#)']])

# Reorder the columns
desired_columns = ['Sample ID (TARA_barcode#)'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df = df[desired_columns]


df.to_csv("Tara_Plot.csv", index=False)

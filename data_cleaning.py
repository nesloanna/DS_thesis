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


# New column names for Meso SL
new_column_names = {
    'Sample ID (TARA_barcode#)': 'Sample ID',
    'Station (TARA_station#)': 'Station',
    'Age [days] (number of days since the samp...)': 'Age',
    'BG province ([abbreviation] full name (MRG...)_D': 'BG province_D',
    'BG province ([abbreviation] full name (MRG...)_M': 'BG province_M',
    'Bathy depth [m] (at the sampling location and ...)': 'Bathy depth',
    'Chl a [mg/m**3] (in the selected environmental...)': 'Chlorophyll_D',
    'Chl a [mg/m**3] (in the selected environmental...).1': 'Chlorophyll_D_1',
    'Chl a conc [mg/m**2] (at the sampling location and ...)': 'Chlorophyll_M',
    'OS region ([abbreviation] full name (MRG...)_D': 'OS region_D',
    'OS region ([abbreviation] full name (MRG...)_M': 'OS region_M',
    "v [cm/s] (Calculated (d'Ovidio et al. 2...)": 'v [cm/s]_D',
    'v [cm/s] (at the sampling location and ...)': 'v [cm/s]_M',
    'wFDc (originally reported as miTAG....)': 'wFDc'
}

# Rename the columns
df = df.rename(columns=new_column_names)


# Extracting "(MRGID:[number])" part into a new column
df['OS MRGID_M'] = df['OS region_M'].str.extract(
    r'\[MRGID:(\d+)\]', expand=False)
df['OS MRGID_D'] = df['OS region_D'].str.extract(
    r'\(MRGID:(\d+)\)', expand=False)


# Removing the extracted part from the original column
df['OS region_M'] = df['OS region_M'].str.replace(
    r'\[MRGID:(\d+)\]', '', regex=True)
df['OS region_D'] = df['OS region_D'].str.replace(
    r'\(MRGID:(\d+)\)', '', regex=True)

df['OS region_M'] = df['OS region_M'].str.replace("(", "[")
df['OS region_M'] = df['OS region_M'].str.replace(")", "]")
df['OS region_M'] = df['OS region_M'].str.replace("[O]", "[NAO]")


print(df['OS region_M'])
print(df['OS region_D'])


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
df['Station (TARA_station#)'] = check_similar_cols(
    df, ['Station (TARA_station#)_D', 'Station (TARA_station#)_M'])
df['Date/Time'] = check_similar_cols(df, ['Date/Time_D', 'Date/Time_M'])
df['Basis'] = check_similar_cols(df, ['Basis_D', 'Basis_M'])
df['Campaign'] = check_similar_cols(df, ['Campaign_D', 'Campaign_M'])
df['Latitude'] = check_similar_cols(df, ['Latitude_D', 'Latitude_M'])
df['Longitude'] = check_similar_cols(df, ['Longitude_D', 'Longitude_M'])
df['OS region'] = check_similar_cols(df, ['OS region_D', 'OS region_M'])


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
    [col for col in df.columns if col not in ['Sample ID']])

# Reorder the columns
desired_columns = ['Sample ID'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df = df[desired_columns]


df.to_csv("Tara_Plot.csv", index=False)

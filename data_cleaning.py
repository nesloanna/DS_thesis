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
    'Age [days] (number of days since the samp...)': 'Age',
    'BG province ([abbreviation] full name (MRG...)_D': 'BG province_D',
    'BG province ([abbreviation] full name (MRG...)_M': 'BG province_M',
    'Bathy depth [m] (at the sampling location and ...)': 'Bathy depth',
    'Chl a [mg/m**3] (in the selected environmental...)': 'Chlorophyll_D',
    'Chl a [mg/m**3] (in the selected environmental...).1': 'Chlorophyll_D_1',
    'Chl a conc [mg/m**2] (at the sampling location and ...)': 'Chlorophyll_M',
    'Cond [mS/cm] (in the selected environmental...)': 'Cond [mS/cm]',
    'D chl m [m] (in the selected environmental...)': 'D chl m',
    'Depth bot [m] (from which this sample was co...)': 'Depth bot',
    'Depth max Brunt Väisälä freq [m] (in the selected environmental...)': 'Depth max Brunt Väisälä',
    'Depth max O2 [m] (in the selected environmental...)': 'Depth max O2',
    'Depth min O2 [m] (in the selected environmental...)': 'Depth min O2',
    'Depth nitracline [m] (in the selected environmental...)': 'Depth nitracline',
    'Depth nominal (from which this sample was co...)': 'Depth nominal',
    'Depth ref [m] (in the selected environmental...)': 'Depth ref',
    'Depth top [m] (from which this sample was co...)': 'Depth top',
    'Distance [km] (from the closest geographic c...)': 'Distance',
    'FEve (originally reported as OG.Eve...)': 'FEve',
    'Fe std dev [±] (standard deviation value at a...)': 'Fe std dev',
    'Fe tot [µmol/l] (mean value at a depth of 5 m ...)': 'Fe tot',
    'Fraction lower [µm] (used on board to prepare samp...)': 'Fraction lower',
    'Fraction upper [µm] (used on board to prepare samp...)': 'Fraction upper',
    'Functional richness (originally reported as OG.Ric...)': 'Functional richness',
    'Latitude (of the closest geographic coo...)': 'Latitude (closest geo)',
    'Latitude (of the continental shelf with...)': 'Latitude (continental shelf)',
    'Latitude (of the geographic coordinate ...)': 'Latitude (geo coordinate)',
    'Longitude (of the closest geographic coo...)': 'Longitude (closest geo)',
    'Longitude (of the continental shelf with...)': 'Longitude (continental shelf)',
    'Longitude (of the geographic coordinate ...)': 'Longitude (geo coordinate)',

    'MLD [m] (in the selected environmental...)': 'MLD',
    'MLD [m] (in the selected environmental...).1': 'MLD.1',
    'MLE [1/day] (at the sampling location and ...)': 'MLE_M',
    'MLE [1/day] (indicates the presence of a t...)': 'MLE_D',
    'MP biome (Longhurst (2007))_D': 'Marine biome_D',
    'MP biome (Longhurst (2007))_M': 'Marine biome_M',

    'NO3 std dev [±] (standard deviation value at a...)': 'Nitrate std',
    'NPP C [mg/m**2/day] (at the sampling location and ...)': 'NPP C_M',
    'NPP C [mg/m**2/day] (at the sampling location for ...)': 'NPP C (30)_M',
    'NPP C [mg/m**2/day] (for a period of 30 days aroun...)': 'NPP C (30)_D',
    'NPP C [mg/m**2/day] (for a period of 8 days around...)': 'NPP C (8)_D',
    'O2 [µmol/kg] (in the selected environmental...)': 'Oxygen',
    'O2 [µmol/kg] (in the selected environmental...).1': 'Oxygen.1',

    'OS region ([abbreviation] full name (MRG...)_D': 'OS region_D',
    'OS region ([abbreviation] full name (MRG...)_M': 'OS region_M',

    'S (originally reported as miTAG....)': 'Species richness',
    'SSD [min] (at the sampling location and ...)': 'Sunshine duration_M',
    'SSD [min] (day length)': 'Sunshine duration_D',

    'Sal (in the selected environmental...)': 'Salinity',
    'Samp mat (TARA_station#_environmental-f...)': 'Sample material',

    'Species div (originally reported as Shanno...)': 'Species div',
    'Species div (originally reported as Shanno...).1': 'Species div.1',
    'Species div (originally reported as Shanno...).2': 'Species div.2',
    'Species div (originally reported as Shanno...).3': 'Species div.3',
    'Species div (originally reported as Shanno...).4': 'Species div.4',
    'Species div (originally reported as Shanno...).5': 'Species div.5',
    'Species div (originally reported as miTAG....)': 'Species miTAG chaos',
    'Species div (originally reported as miTAG....).1': 'Species miTAG ace',
    'Species div (originally reported as miTAG....).2': 'Species miTAG shannon',
    'Ssphi sat [%] (at the sampling location for ...)': 'Ssphi sat',

    'TSS [mg/l] (at the sampling location for ...)': 'Total suspended matter',
    'Tpot [°C] (in the selected environmental...)': 'Temperature',
    'Time of day (at the sampling location, dat...)': 'Time of day',

    'bac660 [1/m] (in the selected environmental...)': 'bac660',
    'bacp [1/m] (in the selected environmental...)': 'bacp',
    'bb470 [1/m] (in the selected environmental...)': 'bb470',
    'bbp470 [1/m] (in the selected environmental...)': 'bbp470',
    'beta470 [m/sr] (in the selected environmental...)': 'beta470',
    'beta470 [m/sr] (in the selected environmental...).1': 'beta470.1',
    'beta470 [m/sr] (in the selected environmental...).2': 'beta470.2',

    "v [cm/s] (Calculated (d'Ovidio et al. 2...)": 'v_D',
    'v [cm/s] (at the sampling location and ...)': 'v_M',
    'wFDc (originally reported as miTAG....)': 'wFDc'
}

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
    [col for col in df.columns if col not in ['Sample ID']])

# Reorder the columns
desired_columns = ['Sample ID'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df = df[desired_columns]


df.to_csv("Tara_Plot.csv", index=False)

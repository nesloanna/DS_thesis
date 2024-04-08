import pandas as pd
import os

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_merged_BMN.csv")


# If you want to reset the index after dropping rows
df.reset_index(drop=True, inplace=True)

# print(df.columns)


new_column_names = [
    'Sample ID', 'Sample ID (Bio)', 'Sample ID (ENA)', 'Basis', 'Campaign',
    'Station', 'Method/Device', 'Event', 'Date/Time', 'Latitude', 'Longitude',
    'Depth layer zone', 'Depth nominal', 'Depth top', 'Depth bot',
    'Frac lower', 'Frac upper', 'Sample material', 'Sample method',
    'Sample label', 'MP biome', 'OS region', 'BG province',
    'Sea ice conc', 'Sea ice free start', 'Sea ice free days',
    'Sea ice free end', 'Season (spring)', 'Season (early)',
    'Moon phase nom', 'Moon phase prop', 'Time of day', 'Sunshine duration',
    'Radiation', 'Radiation 8.1', 'Radiation 8.2', 'Radiation 30',
    'Sea Surface Temp', 'Iron', 'Iron std', 'Ammonium', 'Ammonium std',
    'Nitrite', 'Nitrite std', 'Nitrate', 'Nitrate std',
    'Sea surface fluorescence', 'Sea surface chlorophyll a',
    'Chlorophyll a', 'Sea surface quantum fluorescence',
    'Net PP carbon', 'Net PP carbon 30', 'Total suspended matter',
    'Particulate Organic Carbon', 'Particulate Inorganic Carbon',
    'Depth bathy', 'Latitude.1', 'Longitude.1', 'Distance closest',
    'Sea surface temp grad', 'Strain sub-mesoscale', 'u', 'v',
    'Okubo-Weiss', 'Max Lyapunov Exp', 'Residence time',
    'Latitude.2', 'Longitude.2', 'Age', 'Latitude.3', 'Longitude.3',
    'Shannon_Darwin_mean_all', 'Shannon_Darwin_month_all',
    'Shannon_Darwin_mean_grp', 'Shannon_Darwin_month_grp',
    'Shannon_Physat_month', 'Shannon_Physat_mean', 'SILVA_Chao', 'SILVA_ace',
    'SILVA_Shannon', 'SILVA_species_rich', 'SILVA_func_diversity',
    'OG_func_rich', 'OG_func_even', 'Distance interval',
    'Duration (ISO)', 'No of observations', 'Phosphate min', 'Phosphate lower',
    'Phosphate median', 'Phosphate upper', 'Phosphate max'
]


df.columns = new_column_names

# print(df.columns)

# Removing the ID pattern from OS region and BG province
ID_pattern = r'\(MRGID:(\d+)\)'

df['OS region'] = df['OS region'].str.replace(ID_pattern, '', regex=True)
df['BG province'] = df['BG province'].str.replace(ID_pattern, '', regex=True)


# Removing the ENVO pattern from Depth layer zone
ENVO_pattern = r'\(ENVO:(\d+)\)'

df['Depth layer zone'] = df['Depth layer zone'].str.replace(
    ENVO_pattern, '', regex=True)


# Define your replacements in a dictionary
depth_layer_replace = {
    '[SRF] surface water layer ': '[SRF] Surface Water',
    '[DCM] deep chlorophyll maximum layer ': '[DCM] Deep Chlorophyll Maximum',
    '[ZZZ] marine water layer ': '[ZZZ] Marine Water',
    '[MES] marine water layer  within the mesopelagic zone ': '[MES] Marine Water Mesopelagic Zone',
    '[MIX] marine epipelagic wind mixed layer ': '[MIX] Marien Epipelagic Wind Mixed',
    '[FSW] filtered sea water, used to control protocols': '[FSW] Filtered Sea Water',
}

# Replace values using the dictionary
df['Depth layer zone'] = df['Depth layer zone'].replace(depth_layer_replace)


# Convert the 'DateTime' column to datetime format
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# Extract date and year into new columns
df['Date'] = df['Date/Time'].dt.date
df['Year'] = df['Date/Time'].dt.year


# Columns to apply the operation to
columns_to_process = ['Depth layer zone', 'BG province', 'OS region']

# Loop over the specified columns
for col in columns_to_process:
    # Split the strings and select the second part
    df[col] = df[col].str.split("] ", expand=True)[1]
    df[col] = df[col].str.strip()

# Display the DataFrame
print(df)


# # Sort all columns (but Sample ID) alphabetically
# columns_to_sort = sorted(
#     [col for col in df.columns if col not in ['Sample ID']])

# # Reorder the columns
# desired_columns = ['Sample ID'] + columns_to_sort

# # Create a new dataframe with the desired column order, sorted alphabetically
# df = df[desired_columns]


df.to_csv("Tara_BMN_Cleaned.csv", index=False)

df = df.sort_values(by='Date')

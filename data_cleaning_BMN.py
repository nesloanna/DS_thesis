import pandas as pd
import os

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load merged dataset
df = pd.read_csv("Tara_merged_BMN.csv")


# --------- Column names ---------

# List of new column names
new_column_names = [
    'Sample ID', 'Sample ID (Bio)', 'Sample ID (ENA)', 'Basis', 'Campaign',
    'Station', 'Method/Device', 'Event', 'Date/Time', 'Latitude', 'Longitude',
    'Depth Layer Zone', 'Depth nominal', 'Depth top', 'Depth bot',
    'Frac lower', 'Frac upper', 'Sample material', 'Sample method',
    'Sample label', 'MP biome', 'OS region', 'BG province',
    'Sea ice conc', 'Sea ice free start', 'Sea ice free days',
    'Sea ice free end', 'Season', 'Season (early)',
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
    'Functional richness', 'Functional evenness', 'Distance interval',
    'Duration (ISO)', 'No of observations', 'Phosphate min', 'Phosphate lower',
    'Phosphate median', 'Phosphate upper', 'Phosphate max'
]

# Change column names to list of new column names
df.columns = new_column_names


# --------- Data cleaning ---------

# Remove the ID pattern from columns - Example: (MRGID:1905)
ID_pattern = r'\(MRGID:(\d+)\)'

df['OS region'] = df['OS region'].str.replace(ID_pattern, '', regex=True)
df['BG province'] = df['BG province'].str.replace(ID_pattern, '', regex=True)


# Remove the ENVO pattern from column - Example: (ENVO:00010504)
ENVO_pattern = r'\(ENVO:(\d+)\)'

df['Depth Layer Zone'] = df['Depth Layer Zone'].str.replace(
    ENVO_pattern, '', regex=True)

# Remove the text in brackets from columns - Examples: [SRF] and [MS]
bracket_columns = ['Depth Layer Zone', 'BG province', 'OS region']

for col in bracket_columns:
    df[col] = df[col].str.split("] ", expand=True)[1]  # Keep text after "] "
    df[col] = df[col].str.strip()  # Strip for trailing whitespace


# Replace values in Depth Layer Zone ('original': 'replace with')
depth_layer_replace = {
    'surface water layer': 'Surface Water',
    'deep chlorophyll maximum layer': 'Deep Chlorophyll Maximum',
    'marine water layer': 'Marine Water',
    'marine water layer  within the mesopelagic zone': 'Marine Water Mesopelagic Zone',
    'marine epipelagic wind mixed layer': 'Marien Epipelagic Wind Mixed',
    'filtered sea water, used to control protocols': 'Filtered Sea Water',
}

# Apply replacements to Depth Layer Zone
df['Depth Layer Zone'] = df['Depth Layer Zone'].replace(depth_layer_replace)


# --------- Add columns ---------

# Convert the 'Date/Time' column to datetime format
df['Date/Time'] = pd.to_datetime(df['Date/Time'])

# Extract date and year into new columns
df['Date'] = df['Date/Time'].dt.date
df['Year'] = df['Date/Time'].dt.year


# --------- Drop columns and sort dataframe ---------

cols_to_drop = ['Sample ID (Bio)', 'Sample ID (ENA)', 'Season',
                'Season (early)', 'Moon phase nom', 'Moon phase prop',
                'Latitude.1', 'Longitude.1', 'Distance closest',
                'Latitude.2', 'Longitude.2', 'Latitude.3', 'Longitude.3',
                'Phosphate lower', 'Phosphate upper']

df = df.drop(cols_to_drop, axis=1)

df = df.sort_values(by='Date/Time')

# Sort all columns (but Sample ID) alphabetically
columns_to_sort = sorted(
    [col for col in df.columns if col not in ['Sample ID']])

# Reorder the columns
desired_order = ['Sample ID'] + columns_to_sort

# Create a new dataframe with the desired column order, sorted alphabetically
df = df[desired_order]

# Reset the index after dropping rows
df.reset_index(drop=True, inplace=True)

# Save dataframe to a new CSV file
df.to_csv("Tara_BMN_Cleaned.csv", index=False)

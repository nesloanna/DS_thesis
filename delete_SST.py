import pandas as pd
import os


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_BMN_Cleaned.csv")

# Removing rows with empty longitude or latitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Reset the index after dropping rows
df.reset_index(drop=True, inplace=True)


df_sst = pd.read_csv("Tara_SST_Plot.csv")


# Extract unique combinations of Lat and Lon
unique_lat_lon = df_sst[['sst_lat', 'sst_lon']].drop_duplicates()

# Reset the index after dropping rows
unique_lat_lon.reset_index(drop=True, inplace=True)

# Display the result
print(unique_lat_lon)


# Extract unique combinations of Lat and Lon
unique_location_df = df[['Latitude', 'Longitude']].drop_duplicates()

# Reset the index after dropping rows
unique_location_df.reset_index(drop=True, inplace=True)

# Display the result
print(unique_location_df)

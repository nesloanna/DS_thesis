import pandas as pd
import os
import numpy as np

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


# Read the Excel file
df = pd.read_csv('Tara_Campaign.csv')

df['Date/Time'] = pd.to_datetime(df['Date/Time'])
df['Date/Time 2'] = pd.to_datetime(df['Date/Time 2'])

df['Year'] = df['Date/Time'].dt.year
df['Year 2'] = df['Date/Time 2'].dt.year

# Grouping by 'Year' column
grouped = df.groupby('Year')

# Iterating over each group and printing the values in 'Locality' column
for year, group in grouped:
    print(f'Year: {year} to {group['Year 2'].values}')
    print(f"From: {group['Locality (from port)'].values} to {
          group['Locality (to port)'].values}")
    print()

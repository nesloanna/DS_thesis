import pandas as pd
import os
import numpy as np

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())


# Read the Excel file
df1 = pd.read_excel('TARA_SAMPLES_CONTEXT_ENV-DEPTH-NUT_20170515.xlsx',
                    header=None, skiprows=17)

# Set the column names from the values in the 18th row
df1.columns = df1.iloc[0]  # Set new column names

col_info = df1.iloc[3]  # Get additional info about columns (row 21 in Excel)

# Remove first 4 rows (19-22 in Excel) from data
df1 = df1.iloc[5:].reset_index(drop=True)

# Remove the "PARAMTER" column
df1.drop(columns=['PARAMETER'], inplace=True)

# New column names
new_col_names = ['Sample ID', 'Sample ID (Bio)', 'Sample ID (ENA)', 'Station',
                 'Event', 'Env feature', 'Depth nominal', 'Depth top/min',
                 'Depth bot/max', 'Size frac lower', 'Size frac upper',
                 'Sample material', 'Sample method', 'Sample code/label',
                 'File name', 'Distance', 'Duration(ISO)',
                 'Number of observations', 'Nitrite min', 'Nitrite lower',
                 'Nitrite median', 'Nitrite upper', 'Nitrite max',
                 'Phosphate min', 'Phosphate lower', 'Phosphate median',
                 'Phosphate upper', 'Phosphate max', 'Nitrate/Nitrite min',
                 'Nitrate/Nitrite lower', 'Nitrate/Nitrite median',
                 'Nitrate/Nitrite upper', 'Nitrate/Nitrite max', 'Silicate min',
                 'Silicate lower', 'Silicate median', 'Silicate upper',
                 'Silicate max']

# Change column names
df1.columns = new_col_names

# Save the DataFrame as CSV file
df1.to_csv('Tara_Env_Nut.csv', index=False)


def main():
    depth_file_path = "TARA_sample_enviro.tab"
    df = read_tab_file(depth_file_path)
    df.to_csv("Tara_Environmental_Depth.csv", index=False)

    bio_file_path = "TARA_sample_biodiv.tab"
    df = read_tab_file(bio_file_path)
    df.to_csv("Tara_Biodiversity.csv", index=False)

    meso_file_path = "TARA_registies_mesoscale.tab"
    df = read_tab_file(meso_file_path)
    df.to_csv("Tara_Environmental_Mesoscale.csv", index=False)

    meso_sl_file_path = "TARA_SAMPLES_CONTEXT_ENV-WATERCOLUMN.tab"
    df = read_tab_file(meso_sl_file_path)
    df.to_csv("Tara_Env_Meso_SampleLocation.csv", index=False)

    campaign_path = "TARA_campaign_registries.tab"
    df = read_tab_file(campaign_path)
    df.to_csv("Tara_Campaign.csv", index=False)


def read_tab_file(tab_file_path):

    data_rows = []
    file = open(tab_file_path, 'r')
    while True:
        line = file.readline().strip()
        if line == '*/':
            break

    while True:
        line = file.readline().strip()
        if line.strip() == '':
            break
        data_rows.append(line.split("\t"))

    file.close()
    df = pd.DataFrame(data_rows[1:], columns=data_rows[0])

    return df


if __name__ == '__main__':
    main()

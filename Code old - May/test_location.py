import pandas as pd
import numpy as np
from scipy.spatial import distance


# Load datasets
df_A = pd.read_csv(
    "/Users/annaolsen/Desktop/Speciale/DS_thesis/data/Tara_BMN_Cleaned.csv")

df_A = df_A[["Sample ID", "Latitude", "Longitude", "Sea Surface Temp",
             "Date", "OS region"]]

df_A = df_A.dropna(subset=['Longitude', 'Latitude'])

# df_A = df_A[:1000]

df_W = pd.read_csv(
    "/Volumes/PortableSSD/Speciale/SST/SST_daily/water_locations.csv")


# df_W = df_W[:6000]


# Function to calculate Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2) ** 2 + np.cos(np.radians(lat1)) * \
        np.cos(np.radians(lat2)) * np.sin(dlon/2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distance = R * c
    return distance

# Function to find closest point in dataframe A to a given point (lat, lon)


def find_closest_point_to_point(lat, lon, df):
    distances = haversine(lat, lon, df['Latitude'], df['Longitude'])
    min_index = distances.idxmin()
    closest_lat = df.loc[min_index, 'Latitude']
    closest_lon = df.loc[min_index, 'Longitude']
    return closest_lat, closest_lon


# Apply the function to each row of dataframe A and add the closest coordinates as new columns
closest_coordinates = df_A.apply(lambda row: find_closest_point_to_point(
    row['Latitude'], row['Longitude'], df_W), axis=1)
df_A[['Closest_Latitude', 'Closest_Longitude']] = pd.DataFrame(
    closest_coordinates.tolist(), index=df_A.index)

print(df_A)


# print(df_A.head())
# print(df_W.head())

# Function to find the closest match in df_W for each row in df_A
# def find_closest_match(row):
#     distances = df_W.apply(lambda x: distance.euclidean(
#         (row['Latitude'], row['Longitude']), (x['Latitude'], x['Longitude'])), axis=1)
#     closest_index = distances.idxmin()
#     closest_row = df_W.loc[closest_index]
#     return pd.Series({'lat': closest_row['Latitude'], 'lon': closest_row['Longitude']})


# # Apply the function to each row in df_A
# df_A[['lat', 'lon']] = df_A.apply(find_closest_match, axis=1)

# print(df_A)


# # Initialize empty lists to store closest matches
# closest_LA = []
# closest_LO = []

# # Iterate over each row in df_A
# for idx, row_A in df_A.iterrows():
#     closest_dist = float('inf')  # Initialize with infinity
#     closest_row_W = None  # Initialize with None
#     # Iterate over each row in df_W to find the closest match
#     for idx_W, row_W in df_W.iterrows():
#         dist = distance.euclidean((row_A['LAA'], row_A['LOA']), (row_W['LA'], row_W['LO']))
#         if dist < closest_dist:
#             closest_dist = dist
#             closest_row_W = row_W
#     closest_LA.append(closest_row_W['LA'])
#     closest_LO.append(closest_row_W['LO'])

# # Add closest matches as new columns to df_A
# df_A['Closest_LA'] = closest_LA
# df_A['Closest_LO'] = closest_LO

# print(df_A)

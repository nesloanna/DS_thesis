from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("data/TARA_mhws_Dash.csv")


df['category'].fillna(0, inplace=True)

# Define the mapping of values to integers
mapping = {'Moderate': 1, 'Moderate/Strong': 2, 'Strong': 3}

# Replace values in the 'category' column using the mapping
df['category'] = df['category'].replace(mapping)

# Convert the 'category' column to integer data type
df['category'] = df['category'].astype(int)


# filtered_df = df.dropna(subset=['Shannon_Darwin_mean_all'])
# filtered_df = df.dropna(subset=['SILVA_ace'])

filtered_df = df.select_dtypes(include=['float64', 'int64'])

# filtered_df = filtered_df.select_dtypes(include=['float64', 'int64'])
filtered_df = filtered_df.drop(columns=['Net PP carbon', 'Sea ice conc', 'Sea ice free days', 'Sea ice free end',
                                        'Sea ice free start', 'Year'])

print(filtered_df.shape)
cols = list(filtered_df.columns)

# Create StandardScaler object
# scaler = StandardScaler()


# Create MinMaxScaler object
# scaler = MinMaxScaler()


scaler = RobustScaler()
# scaled_data = scaler.fit_transform(data)

# Fit and transform the data
# scaled_data = scaler.fit_transform(data)

# Fit and transform the data
scaled_data = scaler.fit_transform(filtered_df)

# Convert the scaled data array back to a DataFrame
scaled_data = pd.DataFrame(scaled_data, columns=cols)

# Calculate correlation matrix
corr_matrix = scaled_data.corr()


# Plot correlation matrix as a heatmap
plt.figure(figsize=(30, 28))
sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r',
            fmt=".2f", linewidths=.5, annot_kws={"size": 9})
plt.show()

selected_columns = ['Functional evenness', 'Functional richness', 'Depth top',
                    'SILVA_Chao', 'SILVA_Shannon', 'SILVA_ace',
                    'SILVA_func_diversity', 'SILVA_species_rich', 'Shannon_Darwin_mean_all',
                    'Sea Surface Temp', 'Nitrate',
                    'Phosphate median', 'Chlorophyll a', 'Sea surface chlorophyll a',
                    'category', 'MHWs']

# Select relevant columns
selected_df = df[selected_columns]

# Calculate correlation matrix
correlation_matrix = selected_df.corr()

# Plot correlation matrix as a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True,
            cmap='RdBu_r', fmt=".2f", linewidths=.5)

plt.show()
# plt.close()

# Select only numeric columns
# numeric_df = df.select_dtypes(include=['float64', 'int64'])

# # Calculate correlation matrix
# cor_matrix = numeric_df.corr()

# # Plot correlation matrix as a heatmap
# plt.figure(figsize=(25, 22))
# # plt.figure()
# sns.heatmap(cor_matrix, annot=True, cmap='RdBu_r', fmt=".2f", linewidths=.5)
# plt.title('')
# plt.show()
# plt.close()

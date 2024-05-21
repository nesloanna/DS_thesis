import matplotlib.dates as mdates
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px

os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_Cleaned.csv")

df['Date'] = pd.to_datetime(df['Date'])

# Plot all missing values
# plt.figure(figsize=(10, 6))
# sns.heatmap(df.isnull(), cmap='plasma', cbar=False)
# plt.title('Missing Values Heatmap')
# ax = plt.gca()
# ax.set_xticks([])
# plt.show()


# Divide columns into two subsets
# half_columns = len(df.columns) // 2
# first_half_columns = df.columns[:half_columns]
# second_half_columns = df.columns[half_columns:]

# Visualize missing values for the first half of columns
# plt.figure(figsize=(10, 6))
# sns.heatmap(df[first_half_columns].isnull(), cmap='tab20b', cbar=False)
# plt.title('Missing Values Heatmap (first half of columns)')
# ax = plt.gca()
# ax.set_xticks([])
# plt.show()

# Visualize missing values for the second half of columns
# plt.figure(figsize=(10, 6))
# sns.heatmap(df[second_half_columns].isnull(), cmap='ocean', cbar=False)
# plt.title('Missing Values Heatmap (second half of columns)')
# ax = plt.gca()
# ax.set_xticks([])
# plt.show()


# ----------- Difference in similar attributes -----------
# Plotting
plt.plot(df['Date'], df['Nitrate_D'], label='depth')
plt.plot(df['Date'], df['Nitrate_M'], label='mesoscale')

# Adding labels and legend
plt.xlabel('Date')
plt.ylabel('Nitrate')
plt.title('Nitrate')
plt.legend()
ax = plt.gca()
ax.set_xticks([])

# Display the plot
plt.show()


# Group DataFrame by year
df_grouped = df.groupby(df['Date'].dt.year)

# Plotting each year separately
for year, group in df_grouped:
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(group['Date'], group['Nitrate_D'].fillna(
        method='ffill'), color='steelblue', ls='--', lw=1.1)
    ax.plot(group['Date'], group['Nitrate_D'],
            lw=1.5, marker='o', markersize=2.1, color='steelblue', label='depth')
    ax.plot(group['Date'], group['Nitrate_M'].fillna(
        method='ffill'), ls='--', lw=1.1, color='darkorange')
    ax.plot(group['Date'], group['Nitrate_M'],
            lw=1.5, marker='o', color='darkorange', markersize=2.1, label='mesoscale')

    # Plot markers for each sample
    for date in group['Date']:
        ax.plot(date, -3, marker='o', color='black', markersize=2.3)

    plt.title(f'Nitrate Levels (Year {year})', fontsize=16)
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Nitrate', fontsize=14)
    plt.legend()

    # Set x-axis ticks to display only months
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.tick_params(axis='x', labelsize=11)
    ax.tick_params(axis='y', labelsize=11)

    plt.show()

import plotly.graph_objects as go
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

# # Group DataFrame by year
# df_grouped = df.groupby(df['Year'])

# # Plotting each year separately
# for year, group in df_grouped:
#     fig, ax = plt.subplots(figsize=(10, 7))
#     ax.plot(group['Date'], group['Temperature'].fillna(
#         method='ffill'), color='steelblue', ls='--', lw=0.9)
#     ax.plot(group['Date'], group['Temperature'],
#             lw=1.5, marker='o', markersize=2.1, color='steelblue', label='Temperature')
#     ax.plot(group['Date'], group['Sea surface temp_M'].fillna(
#         method='ffill'), ls='--', lw=0.9, color='darkorange')
#     ax.plot(group['Date'], group['Sea surface temp_M'],
#             lw=1.5, marker='o', color='darkorange', markersize=2.1, label='SST (meso)')

#     # Plot markers for each sample
#     for date in group['Date']:
#         ax.plot(date, 0, marker='o', color='black', markersize=2.1)

#     plt.title(f'Temperature (Year {year})', fontsize=16)
#     plt.xlabel('Date', fontsize=14)
#     plt.ylabel('Temperature (°C)', fontsize=14)
#     plt.legend()

#     # Set x-axis ticks to display only months
#     ax.xaxis.set_major_locator(mdates.MonthLocator())
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
#     ax.tick_params(axis='x', labelsize=11)
#     ax.tick_params(axis='y', labelsize=11)

#     plt.show()


# -------- OS region ----------
# Group DataFrame by "OS region" column
# grouped = df.groupby('OS region')

# # Calculate total number of missing values for each region
# total_missing_count = grouped.apply(lambda x: x.isnull().sum().sum())

# # Calculate total percentage of missing values for each region
# total_missing_percentage = grouped.apply(
#     lambda x: x.isnull().mean().mean() * 100)

# # Plot the results
# ax = total_missing_percentage.plot(
#     kind='bar', figsize=(9, 6), color='skyblue')
# plt.title('Total percentage of missing values (OS region)', fontsize=14)
# plt.xlabel('OS region', fontsize=10)
# plt.ylabel('Total percentage of missing values', fontsize=10)
# plt.xticks(rotation=70, fontsize=8)

# # Set y-axis limits to 90
# ax.set_ylim([0, 90])

# # Add total number and percentage of missing values on top of the bars
# for i, value in enumerate(total_missing_count):
#     ax.text(i, total_missing_percentage[i] + 1, f'({value})', ha='center')
#     ax.text(i, total_missing_percentage[i] + 4,
#             f'{total_missing_percentage[i]:.2f}%', ha='center', fontsize=11)

# plt.show()


# --------- Year --------
# # Group DataFrame by "Year" column
# grouped = df.groupby('Year')

# # Calculate total number of missing values for each year
# total_missing_count = grouped.apply(lambda x: x.isnull().sum().sum())

# # Calculate total percentage of missing values for each year
# total_missing_percentage = grouped.apply(
#     lambda x: x.isnull().mean().mean() * 100)

# # Plot the results
# ax = total_missing_percentage.plot(
#     kind='bar', figsize=(8, 6), color='skyblue')
# plt.title('Total percentage of missing values (Year)', fontsize=16)
# plt.xlabel('Year', fontsize=13)
# plt.ylabel('Total percentage of missing values', fontsize=11)
# plt.xticks(rotation=0)

# # Set y-axis limits to 60
# ax.set_ylim([0, 60])

# # Add total number and percentage of missing values on top of the bars
# for i, (value, percentage) in enumerate(zip(total_missing_count, total_missing_percentage)):
#     ax.text(i, percentage + 1, f'({value})', ha='center')
#     ax.text(i, percentage + 3, f'{percentage:.2f}%', ha='center', fontsize=11)

# plt.show()


def plot_missing_values(df, column_name, plot_name):
    # Group DataFrame by "OS region" column
    grouped = df.groupby('OS region')

    # Calculate total number of missing values for each region
    total_missing_count = grouped.apply(
        lambda x: x[column_name].isnull().sum())

    # Calculate total percentage of missing values for each region
    total_missing_percentage = grouped.apply(
        lambda x: (x[column_name].isnull().mean()) * 100)

    # Plot the results
    ax = total_missing_percentage.plot(
        kind='bar', figsize=(9, 6), color='skyblue')
    plt.title(f'Missing values ({plot_name}) in OS regions', fontsize=14)
    plt.xlabel('OS region', fontsize=10)
    plt.ylabel('Total percentage of missing values', fontsize=10)
    plt.xticks(rotation=70, fontsize=8)

    # Set y-axis limits to 90
    ax.set_ylim([0, 110])

    # Add total number and percentage of missing values on top of the bars
    for i, value in enumerate(total_missing_count):
        ax.text(i, total_missing_percentage[i] + 1, f'({value})', ha='center')
        ax.text(i, total_missing_percentage[i] + 4, f'{
                total_missing_percentage[i]:.2f}%', ha='center', fontsize=11)

    plt.show()


# plot_missing_values(df, 'Nitrate_D', "Nitrate - depth")
# plot_missing_values(df, 'Nitrate_M', "Nitrate - meso")
# plot_missing_values(df, 'Phosphate', "Phosphate")
# plot_missing_values(df, 'Temperature', "Temperature")
# plot_missing_values(df, 'Sea surface temp_M', "Sea surface temp - meso")
# plot_missing_values(df, 'Chlorophyll_D', "Chlorophyll - depth")
# plot_missing_values(df, 'Chlorophyll_M', "Chlorophyll - meso")
# plot_missing_values(df, 'Depth ref', "Depth ref - depth")
# plot_missing_values(df, 'Depth top', "Depth top - meso")
# plot_missing_values(df, 'NPP C (30)_D', "Net primary production of carbon")


# Plot boxplot
# Plot boxplot with enhanced styling
plt.figure(figsize=(8, 6))
df.boxplot(column=['Nitrate_D', 'Nitrate_M'], patch_artist=True, boxprops=dict(facecolor='skyblue', color='black'),
           whiskerprops=dict(color='black', linestyle='-'), capprops=dict(color='black'), medianprops=dict(color='black'))
plt.title('Box Plot of Nitrate (depth and mesoscale)', fontsize=14)
plt.ylabel('Nitrate Value', fontsize=12)
plt.xticks([1, 2], ['depth', 'mesoscale'], fontsize=10)
# Add grid lines with dashed style and reduced opacity
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


# data = df[['Nitrate_M', 'Nitrate_D']]
# # Create box plot using Plotly
# fig = go.Figure()

# for column_name in data.columns:
#     fig.add_trace(go.Box(y=data[column_name], name=column_name, boxmean='sd'))

# # Update layout
# fig.update_layout(
#     title='Box Plot of Nitrate (depth and mesoscale)',
#     yaxis_title='Nitrate value',
#     xaxis_title='Nitrate type',
#     boxmode='group',  # Group box plots
#     showlegend=False  # Show legend
# )

# # Show plot
# fig.show()

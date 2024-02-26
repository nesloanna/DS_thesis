from dash_bootstrap_templates import load_figure_template
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go  # or plotly.express as px
from dash import Dash, dcc, html
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import sys
import plotly.graph_objects as go


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_Cleaned.csv")

# Removing rows with empty longitude or latitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Reset the index after dropping rows
df.reset_index(drop=True, inplace=True)

all_data_points = len(df)

# Year ...
year_min, year_max = df['Year'].min(), df['Year'].max()

# Temperature
df['Temperature-NaN'] = df['Temperature'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

temperature_values = df['Temperature-NaN'].unique()

df['Temperature'].fillna('NaN', inplace=True)  # NaN -> 'Unknown'


# Marine biome (depth)
df['Marine biome_D'].fillna('Unknown', inplace=True)  # NaN -> 'Unknown'

marine_biomes = df['Marine biome_D'].unique()

# Depth
df['Depth-NaN'] = df['Depth ref'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

depth_values = df['Depth-NaN'].unique()

df['Depth ref'].fillna('NaN', inplace=True)  # NaN -> 'Unknown'


# Env feature (depth layer zone)
df['Env feature (abbreviation)'].fillna(
    'Unknown', inplace=True)  # NaN -> 'Unknown'

env_features = df['Env feature (abbreviation)'].unique()

# ---------- Data for scatter plot and dropdown menus ----------
cols_x = ['Temperature', 'Depth ref', 'Env feature (abbreviation)', 'Nitrate_D',
          'Nitrate_M', 'Phosphate', 'NPP C (30)_D', 'NPP C (30)_M']

# Create dropdown menu for selecting attributes
scatter_options_x = [{'label': col, 'value': col} for col in cols_x]


cols_y = ['Species div', 'Species miTAG chao',
          'Species miTAG ace', 'Species richness', 'Functional richness']

# Create dropdown menu for selecting attributes
scatter_options_y = [{'label': col, 'value': col} for col in cols_y]


# ---------- Plotly, dash and mapbox ----------
px.set_mapbox_access_token(
    'pk.eyJ1Ijoia29ydHBsb3RseSIsImEiOiJjbHBoNDZmZm0wMHUyMnJwNm5yM3RtcjY1In0.qxuHfESjhBp1wqT9ByZc0g')


# create the dash application using the above layout definition
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# load_figure_template('FLATLY')
# Makes the Bootstrap Themed Plotly templates available
load_figure_template("cerulean")


# ---------- Dashboard layout ----------

app.layout = html.Div([
    dbc.Container([
        dbc.Row(  # Row with title and subtitle
            dbc.Col(
                html.Div([
                    html.H3(children='TARA Ocean'),
                ], style={'textAlign': 'center', 'marginTop': 20,
                          'marginBottom': 0}))),
        dbc.Row([  # Row with sidebar and map
                dbc.Col(
                    html.Div([
                        html.P('Years', style={'fontWeight': "bold",
                                               'marginBottom': 10,
                                               'marginTop': 15}),
                        dcc.RangeSlider(id='year_range_slider',
                                        min=year_min,
                                        max=year_max,
                                        step=1,
                                        marks={int(year_min): str(year_min),
                                               int(year_max): str(year_max)},
                                        value=[year_min, year_max],
                                        tooltip={"placement": "bottom",
                                                 "always_visible": False}),

                        html.P('Marine biome', style={'fontWeight': "bold",
                                                      'marginTop': 15,
                                                      'marginBottom': 5}),
                        dbc.Checklist(id='marine_biomes',
                                      options=marine_biomes,
                                      value=marine_biomes,
                                      style={'marginLeft': 20,
                                             'marginRight': 20}),

                        html.P('Temperature', style={'fontWeight': "bold",
                                                     'marginTop': 15,
                                                     'marginBottom': 5}),
                        dbc.Checklist(id='temperatures',
                                      options=temperature_values,
                                      value=temperature_values,
                                      inline=True,
                                      style={'marginLeft': 20,
                                             'marginRight': 20}),

                        html.P('Depth', style={'fontWeight': "bold",
                                               'marginTop': 15,
                                               'marginBottom': 5}),
                        dbc.Checklist(id='depths',
                                      options=depth_values,
                                      value=depth_values,
                                      inline=True,
                                      style={'marginLeft': 20,
                                             'marginRight': 20}),

                        html.P('Depth layer zone',
                               style={'fontWeight': "bold", 'marginTop': 15,
                                      'marginBottom': 5}),
                        dbc.Checklist(id='env_features',
                                      options=env_features,
                                      value=env_features,
                                      inline=True,
                                      style={'marginLeft': 20,
                                             'marginRight': 20}),

                        html.Div([
                            html.P("Filtered data:", style={
                                   'marginBottom': 0, 'marginLeft': 10,
                                   'marginTop': 15, 'font-size': '16px'}),
                            html.Div(id='filtered-count', style={
                                     'marginBottom': 0, 'font-size': '16px',
                                     'marginTop': 15,
                                     'font-weight': 'bold', 'marginLeft': 30}),
                        ], style={'display': 'flex'}),

                        html.Div([
                            html.P("All data:",
                                   style={'textAlign': 'left',
                                          #   'fontWeight': "bold",
                                          'marginBottom': 20, 'marginLeft': 10,
                                          'font-size': '16px'}),
                            html.P(f"{all_data_points}",
                                   style={'textAlign': 'left',
                                          'fontWeight': "bold",
                                          'marginBottom': 20,
                                          'marginLeft': 65,
                                          'font-size': '16px'})
                        ], style={'display': 'flex'}),

                    ]), width=2,
                ),
                dbc.Col(
                    html.Div([
                        dcc.Graph(id='ocean_map'),
                        dcc.Input(id='dummy-input', type='hidden',
                                  value='trigger-callback'),
                    ]), width=10, className="scatter_map"),
                ]),
        dbc.Row([
            html.Div([
                html.P('', style={'marginBottom': 10, 'marginTop': 15})
            ])
        ]),
        dbc.Row([  # Row with scatter plot and bar chart
            dbc.Col(
                html.Div([
                    html.P('Choose an attribute for x-axis:',
                           style={'fontWeight': "bold",
                                  'marginTop': 30,
                                  'marginBottom': 5,
                                  'font-size': 16}),
                    dcc.Dropdown(id='scatter_dropdown_x',
                                 options=scatter_options_x,
                                 multi=False,
                                 clearable=False,
                                 value='Temperature',
                                 style={'marginTop': 0}),
                    html.P('Choose an attribute for y-axis:',
                           style={'fontWeight': "bold",
                                  'marginTop': 30,
                                  'marginBottom': 5,
                                  'font-size': 16}),
                    dcc.Dropdown(id='scatter_dropdown_y',
                                 options=scatter_options_y,
                                 multi=False,
                                 clearable=False,
                                 value='Species richness',
                                 style={'marginTop': 0}),

                ]), width=2),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='scatter_plot')]),
                width=7, className="scatter_plot"),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='sample_count_bar'),
                ]), width=4, className="sample_count_bar"),
        ]),

    ], fluid=True),
])


# ---------- Scatter plot (updates based on selected attributes) ----------
@app.callback(
    Output('scatter_plot', 'figure'),
    [Input('year_range_slider', 'value'),
     Input('scatter_dropdown_x', 'value'),
     Input('scatter_dropdown_y', 'value')]
)
def update_scatter_plot(year_range, attribute_x, attribute_y):

    dff = df[df['Year'].between(year_range[0], year_range[1])]

    # Ensure Latitude and Longitude are always included
    # plot_columns = ['Latitude', 'Longitude']
    plot_columns_x = ['Temperature']
    plot_columns_y = ['Species richness']

    # Add selected attributes to the plot columns if they exist
    if attribute_x:
        plot_columns_x[0] = attribute_x

    if attribute_y:
        plot_columns_y[0] = attribute_y

    print(f"Plot Columns x: {plot_columns_x} and y: {plot_columns_y}")

    # Create scatter plot
    fig = px.scatter(dff,
                     height=600,
                     x=plot_columns_x[0],
                     y=plot_columns_y[0],
                     color='Latitude',
                     hover_name='Year',
                     title='Scatter Plot')

    # fig.update_layout(plot_bgcolor='#ffffff')

    # fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    return fig


# ---------- Map - Plot sample locations ----------
@app.callback(
    [Output('ocean_map', 'figure'),
     Output('filtered-count', 'children')],
    [Input('year_range_slider', 'value'),
     Input('marine_biomes', 'value'),
     Input('depths', 'value'),
     Input('temperatures', 'value'),
     Input('env_features', 'value')]
)
def plot_samples_map(year_range, marine_biome, depth, temperature, env_feature):

    dff = df[df['Year'].between(year_range[0], year_range[1])]
    dff = dff[dff['Marine biome_D'].isin(marine_biome)]

    dff = dff[dff['Depth-NaN'].isin(depth)]
    dff = dff[dff['Temperature-NaN'].isin(temperature)]
    dff = dff[dff['Env feature (abbreviation)'].isin(env_feature)]

    fig = px.scatter_mapbox(dff,
                            lat=dff['Latitude'],
                            lon=dff['Longitude'],
                            color='OS region',
                            zoom=0.8, height=600,
                            title=None, opacity=.5,
                            custom_data=['OS region',
                                         'Year', 'Date', 'Marine biome_D',
                                         'Temperature', 'Depth ref',
                                         'Env feature (abbreviation)'],
                            )

    # Define a custom hover template
    hover_template = '<b>%{customdata[0]}</b><br>' \
        'Year: %{customdata[1]}<br>' \
        'Date: %{customdata[2]}<br>' \
        'Marine biome: %{customdata[3]}<br>' \
        'Temperature: %{customdata[4]}<br>' \
        'Depth: %{customdata[5]}<br>' \
        'Depth layer zone: %{customdata[6]}<extra></extra>'

    # Update the hover template
    fig.update_traces(hovertemplate=hover_template)

    fig.update_layout(mapbox_style='mapbox://styles/kortplotly/clsyukswv002401p8a4xtbbm3',
                      margin={"r": 0, "l": 0, "b": 0, "t": 20})

    # to preserve the UI settings such as zoom and panning in the update
    fig['layout']['uirevision'] = 'unchanged'

    # Get the count of filtered records
    count = len(dff)

    return [fig, f"{count}"]


# ---------- Bar chart (sample counts) ----------
@app.callback(
    Output('sample_count_bar', 'figure'),
    [Input('year_range_slider', 'value')]
)
def plot_sample_count(year_range):

    dff = df[df['Year'].between(year_range[0], year_range[1])]

    counts_per_year = dff['Year'].value_counts().sort_index()

    fig = px.bar(x=counts_per_year.index, y=counts_per_year.values,
                 labels={'x': 'Year', 'y': 'Sample Count'},
                 title='Sample Count per Year')

    return fig


# start the web application
if __name__ == '__main__':
    app.run_server(debug=True, port=8056)

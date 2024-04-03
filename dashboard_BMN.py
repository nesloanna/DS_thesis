import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import dash
import dash_bootstrap_components as dbc


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_BMN_Cleaned.csv")

# Removing rows with empty longitude or latitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Reset the index after dropping rows
df.reset_index(drop=True, inplace=True)


df_sst = pd.read_csv("Tara_SST_Plot.csv")

# df = df[:1000]

all_data_points = len(df)


h6_style = {'fontWeight': "bold", 'marginTop': 20, 'marginBottom': 10}


# ---- Year slider ----
year_min, year_max = df['Year'].min(), df['Year'].max()

all_years = list(range(year_min, year_max + 1))  # Find all years within range

year_marks = {year: str(year)
              for year in all_years}  # Create marks for each year

# ---- Temperature ----
df['Temperature_NaN'] = df['Sea Surface Temp'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

temperature_values = df['Temperature_NaN'].unique()

df['Sea Surface Temp'].fillna('NaN', inplace=True)  # NaN -> 'NaN'

df['Nitrate'].fillna('NaN', inplace=True)  # NaN -> 'NaN'
df['Chlorophyll a'].fillna('NaN', inplace=True)  # NaN -> 'NaN'
df['Net PP carbon'].fillna('NaN', inplace=True)
df['Net PP carbon 30'].fillna('NaN', inplace=True)

# ---- Marine biome (depth) ----
df['MP biome'].fillna('NaN', inplace=True)  # NaN -> 'NaN'

marine_biomes = df['MP biome'].unique()

# ---- Depth ----
df['Depth_NaN'] = df['Depth top'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

depth_values = df['Depth_NaN'].unique()

df['Depth top'].fillna('NaN', inplace=True)  # NaN -> 'Unknown'
df['Depth nominal'].fillna('NaN', inplace=True)


# ---- Phosphate ----
df['Phosphate_NaN'] = df['Phosphate median'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

phosphate_values = df['Phosphate_NaN'].unique()

df['Phosphate median'].fillna('NaN', inplace=True)  # NaN -> 'Unknown'


# ---- Biodiversity ----
df['Shannon_mean_all_NaN'] = df['Shannon_Darwin_mean_all'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

shannon_values = df['Shannon_mean_all_NaN'].unique()

df['Shannon_Darwin_mean_all'].fillna('NaN', inplace=True)  # NaN -> 'Unknown'

df['SILVA_Chao_NaN'] = df['SILVA_Chao'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

silva_chao_values = df['SILVA_Chao_NaN'].unique()

df['SILVA_ace_NaN'] = df['SILVA_ace'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

silva_ace_values = df['SILVA_ace_NaN'].unique()


df['SILVA_species_NaN'] = df['SILVA_species_rich'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

silva_species_values = df['SILVA_species_NaN'].unique()


df['SILVA_func_div_NaN'] = df['SILVA_func_diversity'].apply(
    lambda x: 'NaN' if pd.isna(x) else 'Value')

silva_func_div_values = df['SILVA_func_div_NaN'].unique()


# ---- Env feature (depth layer zone) ----
df['Depth layer zone'].fillna(
    'Unknown', inplace=True)  # NaN -> 'Unknown'

env_features = df['Depth layer zone'].unique()


# ---------- Data for scatter plot and dropdown menus ----------
cols_x = ['Sea Surface Temp', 'Depth top',
          'Depth nominal', 'Depth layer zone',
          'Nitrate', 'Chlorophyll a',
          'Phosphate median', 'Phosphate max' 'Net PP carbon']

# Options for dropdown menu (x-axis)
scatter_options_x = [{'label': col, 'value': col} for col in cols_x]


cols_y = ['Shannon_Darwin_mean_all', 'SILVA_Chao', 'SILVA_ace',
          'SILVA_species_rich', 'SILVA_func_diversity', 'Sea Surface Temp',
          'Depth top', 'Depth nominal', 'Nitrate', 'Chlorophyll a']


# Options for dropdown menu (y-axis)
scatter_options_y = [{'label': col, 'value': col} for col in cols_y]


# ---- Left side bar ----
SIDEBAR_STYLE = {
    "top": 0,
    "left": 0,
    "bottom": 0,
    "paddingLeft": '20px',
    "paddingRight": '10px',
    "paddingTop": "32px",
    "paddingBottom": '10px',
    "background-color": "#f8f9fa",
}

sidebar = html.Div([
    html.H4("Filters"),
    html.Hr(),
    html.H6('Color points by category:', style=h6_style),
    dbc.RadioItems(
        options=[
            {"label": 'Marine biome', "value": 'MP biome'},
            {"label": 'Ocean and sea region', "value": 'OS region'},
            {"label": 'Depth layer zone', "value": 'Depth layer zone'},
            {"label": 'Biogeographical province', "value": 'BG province'},
        ],
        value="OS region",
        id="map-color-input",
        style={'marginTop': 10, 'marginBottom': 25},
    ),
    html.H6('Years',
            style={'fontWeight': "bold", 'marginTop': 15, 'marginBottom': 15}),
    dcc.RangeSlider(
        id='year_range_slider',
        min=year_min,
        max=year_max,
        step=1,
        marks=year_marks,
        value=[year_min, year_max],
    ),
    html.H6('Temperature', style=h6_style),
    dbc.Checklist(
        id='temperatures',
        options=temperature_values,
        value=temperature_values,
        inline=True,
    ),
    html.H6('Phosphate', style=h6_style),
    dbc.Checklist(
        id='phosphates',
        options=phosphate_values,
        value=phosphate_values,
        inline=True,
    ),
    html.H6('Shannon (mean all)', style=h6_style),
    dbc.Checklist(
        id='shannon_mean',
        options=shannon_values,
        value=shannon_values,
        inline=True,
    ),
    html.H6('SILVA ace', style=h6_style),
    dbc.Checklist(
        id='silva_ace',
        options=silva_ace_values,
        value=silva_ace_values,
        inline=True,
    ),
    # shannon_values silva_chao_values
    # silva_species_values silva_func_div_values

    html.Div([
        html.P("Filtered data:",
               style={'marginBottom': 0, 'marginLeft': 0,
                      'marginTop': 25, 'font-size': '16px'}),
        html.Div(id='filtered-count', style={
            'marginBottom': 0, 'font-size': '16px',
            'marginTop': 25,
            'font-weight': 'bold', 'marginLeft': 30}),
    ], style={'display': 'flex'}),
    html.Div([
        html.P("All data:",
               style={'textAlign': 'left',
                      'marginBottom': 20, 'marginLeft': 0,
                      'font-size': '16px'}),
        html.P(f"{all_data_points}",
               style={'textAlign': 'left',
                      'fontWeight': "bold",
                      'marginBottom': 0,
                      'marginLeft': 65,
                      'font-size': '16px'})
    ], style={'display': 'flex'}),
],
    style=SIDEBAR_STYLE)


# ---- Info box ----

# Define the style for the card containing the info
info_box_style = {'margin-top': '0px', 'marginBottom': '20px',
                  'padding': '15px', 'background-color': '#f0f0f0',
                  'line-height': '1.1'}

info_box_style_a = {'margin-top': '0px', 'marginBottom': '20px',
                    'marginLeft': '0px',
                    'padding': '0px', 'background-color': '#f0f0f0',
                    'line-height': '1.1'}

# Define the layout for the info box
info_box = dbc.Card([
    dbc.CardBody([
        html.H5("Explore points", className="card-title",
                style={'marginBottom': '10px'},
                id='selected_point_info_header'),
        html.P("Click on a point to display its information.",
               className="card-text", id='selected_point_info_text')
    ])
], style=info_box_style)


box_options = [
    {'label': 'Sea Surface Temp', 'value': 'Sea Surface Temp'},
    {'label': 'Nitrate', 'value': 'Nitrate'},
    {'label': 'Phosphate', 'value': 'Phosphate median'},
    {'label': 'Depth top', 'value': 'Depth top'},
    {'label': 'Depth nominal', 'value': 'Depth nominal'},
    {'label': 'Chlorophyll a', 'value': 'Chlorophyll a'},
]


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
        dbc.Row(  # Row with title of dashboard
            dbc.Col(
                html.Div([
                    html.H3(children='TARA Ocean'),
                ], style={'textAlign': 'center', 'marginTop': 20,
                          'marginBottom': 10}))),

        dbc.Row(  # Row with sidebar, ocean map, info box
            [dbc.Col(
                sidebar, width=2),  # Sidebar
             dbc.Col(
                html.Div([  # Ocean map
                    dcc.Graph(id='ocean_map',
                              clickData={'points': [{'customdata': ''}]}
                              ),
                    dcc.Input(id='dummy-input', type='hidden',
                              value='trigger-callback'),
                ]), width=7, className="scatter_map"),
             dbc.Col(  # Info box
                html.Div([
                    html.Div(id='selected_point_info_box'),
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Attribute for box plot"),
                            dcc.Dropdown(
                                id='boxplot_dropdown',
                                options=box_options,
                                value='Sea Surface Temp',  # Default value
                                clearable=False,
                                style={'width': '90%', 'marginBottom': '10px',
                                       'marginTop': '10px'}),
                            dcc.Graph(id='box_plot', figure={}),
                            # Add a hidden div to store the selected point information
                            html.Div(id='selected_point_info',
                                     style={'display': 'none'}),
                        ])
                    ], style=info_box_style)
                ]),
                width=3),
             ]),
        dbc.Row([
            html.Div([
                html.P('', style={'marginBottom': 10, 'marginTop': 15})
            ])
        ]),
        dbc.Row([  # Row with scatter plot and bar chart
            dbc.Col(
                html.Div([  # Dropdown for scatter plot
                    html.P('Attribute for x-axis:',
                           style={'fontWeight': "bold",
                                  'marginTop': 30,
                                  'marginBottom': 5,
                                  'font-size': 16}),
                    dcc.Dropdown(id='scatter_dropdown_x',
                                 options=scatter_options_x,
                                 multi=False,
                                 clearable=False,
                                 value='Sea Surface Temp',
                                 style={'marginTop': 0}),
                    html.P('Attribute for y-axis:',
                           style={'fontWeight': "bold",
                                  'marginTop': 30,
                                  'marginBottom': 5,
                                  'font-size': 16}),
                    dcc.Dropdown(id='scatter_dropdown_y',
                                 options=scatter_options_y,
                                 multi=False,
                                 clearable=False,
                                 value='SILVA_species_rich',
                                 style={'marginTop': 0}),
                    html.P('Color by attribute:',
                           style={'fontWeight': "bold",
                                  'marginTop': 30,
                                  'marginBottom': 5,
                                  'font-size': 16}),
                    dcc.Dropdown(id='scatter_color',
                                 options=[
                                    {'label': 'Sea Surface Temp',
                                        'value': 'Sea Surface Temp'},
                                    {'label': 'Latitude', 'value': 'Latitude'},
                                    {'label': 'Depth', 'value': 'Depth top'},
                                 ],
                                 multi=False,
                                 clearable=False,
                                 value='Latitude',
                                 style={'marginTop': 0}),

                ]), width=2),
            dbc.Col(
                html.Div([  # Scatter plot
                    dcc.Graph(id='scatter_plot')]),
                width=7, className="scatter_plot"),
            dbc.Col(
                html.Div([  # Bar chart
                    dcc.Graph(id='sample_count_bar'),
                ]), width=4, className="sample_count_bar"),
        ]),

    ], fluid=True),
])


# ---------- Box plot ----------

@app.callback(
    Output('box_plot', 'figure'),
    [Input('selected_point_info', 'children'),
     Input('boxplot_dropdown', 'value'),
     Input('map-color-input', 'value')]
)
def update_box_plot(selected_point_info, selected_column, color_category):

    # fig = px.box(df, y=selected_column, title=f'Box Plot of {selected_column}')

    fig = go.Figure(
        data=[go.Box(y=df[selected_column],
                     boxpoints=False,  # 'all', 'outliers', or 'suspectedoutliers'
                     jitter=0.7,  # add some jitter for a better separation between points
                     pointpos=-1.8,  # relative position of points wrt box
                     name="All",  # Set the name for the first box plot
                     showlegend=False,
                     hoverinfo='y',
                     )])

    # If a point is selected, add a marker for the selected point on the box plot
    if selected_point_info and 'lat' in selected_point_info and 'lon' in selected_point_info:
        lat = selected_point_info['lat']
        lon = selected_point_info['lon']
        selected_row = df[(df['Latitude'] == lat) &
                          (df['Longitude'] == lon)]

        if not selected_row.empty:
            selected_row = selected_row.iloc[0]
            selected_value = selected_row[selected_column]

            if selected_value != "NaN":
                # If selected value is not NaN, show legend as "point"
                legend_name = 'Point'
                marker_style = dict(color='red', size=10)
            else:
                # If selected value is NaN, show legend as "NaN"
                legend_name = 'NaN'
                marker_style = dict(color='black', size=10)

            fig.add_trace(go.Scatter(
                x=["All"], y=[selected_value], mode='markers',
                marker=marker_style, name=legend_name, hoverinfo='y',
                showlegend=True))

            # If a color category is selected, add a box plot only for the selected subcategory
            if color_category:
                selected_category = selected_row[color_category]
                category_data = df[df[color_category] ==
                                   selected_category][selected_column]
                fig.add_trace(go.Box(
                    y=category_data,
                    boxpoints=False,
                    jitter=0.7,
                    pointpos=-1.8,
                    name=f"{selected_category}",
                    showlegend=False,
                    hoverinfo='y'
                ))

                # Add red marker for selected point in the second box plot
                fig.add_trace(go.Scatter(
                    x=[selected_category],
                    y=[selected_value],
                    mode='markers',
                    marker=dict(color='red', size=10),
                    name='Point',
                    hoverinfo='y',
                    showlegend=False
                ))

    # Adjust the margins
    fig.update_layout(
        title=f'{selected_column}',  # Set the title
        title_x=0.5,  # Center the title
        title_y=0.94,
        margin=dict(t=40, l=40, b=20, r=0),  # Margin of plot
        legend=dict(x=0.82, y=1.05),
        height=300,
        width=310,
    )

    return fig


# Callback to store the selected point information when a point is clicked on the map
@app.callback(
    Output('selected_point_info', 'children'),
    [Input('ocean_map', 'clickData')]
)
def store_selected_point_info(clickData):
    if clickData:
        selected_point_info = clickData['points'][0]
        return selected_point_info
    else:
        return None


# ---------- Ocean map - Plot sample locations ----------

# Define your list of colors
custom_colors = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd',
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# Define the labels dictionary
legend_labels = {
    "MP biome": "Marine biome",
    "OS region": "Ocean and sea region",
    "Depth layer zone": "Depth layer zone",
    "BG province": "Biogeographical province"
}


@app.callback(
    [Output('ocean_map', 'figure'),
     Output('filtered-count', 'children')],
    [Input('year_range_slider', 'value'),
     Input('phosphates', 'value'),
     Input('temperatures', 'value'),
     Input('shannon_mean', 'value'),
     Input('silva_ace', 'value'),
     Input('map-color-input', 'value')])
def plot_samples_map(year_range, phosphate, temperature, shannon_mean, silva_ace, color_by):

    dff = df[df['Year'].between(year_range[0], year_range[1])]

    dff = dff[dff['Phosphate_NaN'].isin(phosphate)]
    dff = dff[dff['Temperature_NaN'].isin(temperature)]
    dff = dff[dff['Shannon_mean_all_NaN'].isin(shannon_mean)]
    dff = dff[dff['SILVA_ace_NaN'].isin(silva_ace)]

    fig = px.scatter_mapbox(dff,
                            lat=dff['Latitude'],
                            lon=dff['Longitude'],
                            color=color_by,
                            color_discrete_sequence=custom_colors,
                            zoom=0.8, height=700,
                            title=None, opacity=.5,
                            custom_data=['Sample ID',
                                         'OS region',
                                         'Date', 'MP biome',
                                         'Sea Surface Temp', 'Depth top',
                                         'Depth nominal', 'Depth layer zone',
                                         'Sea ice conc', 'Net PP carbon',
                                         'Station', 'Phosphate median',
                                         'Latitude', 'Longitude'],
                            )

    # Define a custom hover template
    hover_template = '<b>%{customdata[0]}</b><br>' \
        'Station: %{customdata[10]}</b><br>' \
        'Region: %{customdata[1]}<br>' \
        'Date: %{customdata[2]}<br>' \
        'Marine biome: %{customdata[3]}<br>' \
        'Temperature: %{customdata[4]:.2f}<br>' \
        'Depth: %{customdata[5]}<br>' \
        'Depth nominal: %{customdata[6]}<br>' \
        'Phosphate: %{customdata[11]}<br>' \
        '%{customdata[7]}<br>' \
        'Sea Ice Concentration: %{customdata[8]}<br>' \
        'Net primary production of carbon: %{customdata[9]}<br>' \
        'Lat: %{customdata[12]:.3f}, Lon: %{customdata[13]:.3f}<extra></extra>'

    # Update the hover template
    fig.update_traces(hovertemplate=hover_template)

    # Add points from df2 as a separate scatter plot
    fig.add_scattermapbox(
        lat=df_sst['sst_lat'],
        lon=df_sst['sst_lon'],
        mode='markers',
        # marker=dict(color=df_sst['OS region'],
        #             colorscale='Viridis',  # Use the same color scale as the main plot
        #             # Add colorbar for temperature
        #             colorbar=dict(title='OS region')),
        text=df_sst['Sample ID'],  # Display Sample ID as hover text
        name='Additional Points',  # Name for the legend
        # Custom data for hover
        customdata=df_sst[['Sample ID', 'sst_daily', 'Sea Surface Temp',
                           'sst_lat', 'sst_lon', 'Latitude', 'Longitude']],
        hovertemplate="<b>%{customdata[0]}</b><br>" +
        "Temperature (SST): %{customdata[1]:.2f}<br>" +
        "Tara SST: %{customdata[2]:.2f}<br>" +
        "Lat: %{customdata[3]}, Lon: %{customdata[4]}<br>" +
        "(Tara Lat: %{customdata[5]:.3f}, Lon: %{customdata[6]:.3f}<extra></extra>"

    )

    # Update the legend title dynamically based on the selected option
    # Default to "Legend" if color_by not found

    legend_title = legend_labels.get(color_by, "Legend")
    fig.update_layout(
        mapbox_style='mapbox://styles/kortplotly/clsyukswv002401p8a4xtbbm3',
        margin={"r": 0, "l": 0, "b": 0, "t": 0},
        showlegend=True,
        legend=dict(
            orientation="h",
            x=0,
            yanchor="top",
            y=1.05,
            title=legend_title  # Set the legend title dynamically
        )
    )

    # to preserve the UI settings such as zoom and panning in the update
    fig['layout']['uirevision'] = 'unchanged'

    # Get the count of filtered records
    count = len(dff)

    return [fig, f"{count}"]


# ---------- Clicks on map ----------

# Define the style for the table
table_style = {
    'margin-top': '0px',
    'margin-bottom': '0px',
    'padding': '3px',
    'background-color': '#f0f0f0',
    'line-height': '1.7',
    'overflowX': 'auto',
    'width': '100%',
}


@app.callback(
    Output('selected_point_info_box', 'children'),
    [Input('ocean_map', 'clickData')]
)
def display_selected_point_info(clickData):
    if clickData is not None:
        selected_point = clickData['points'][0] if clickData['points'] else None
        if selected_point:
            lat = selected_point.get('lat')
            lon = selected_point.get('lon')

            # Find the row in the DataFrame corresponding to the clicked point
            selected_rows = df[(df['Latitude'] == lat) &
                               (df['Longitude'] == lon)]

            if not selected_rows.empty:
                selected_row = selected_rows.iloc[0]

                sample_id = selected_row['Sample ID']
                date = selected_row['Date']
                os_region = selected_row['OS region']
                marine_biome = selected_row['MP biome']

                depth_layer = selected_row['Depth layer zone']
                depth_top = selected_row['Depth top']
                depth_nom = selected_row['Depth nominal']
                sea_surface_temp = selected_row['Sea Surface Temp']

                nitrate = selected_row['Nitrate']
                phosphate_med = selected_row['Phosphate median']
                phosphate_max = selected_row['Phosphate max']
                chlorophyll = selected_row['Chlorophyll a']
                carbon_production = selected_row['Net PP carbon 30']

                if lat is not None and lon is not None:
                    data = [
                        {"Col": "Sample ID", "Value": sample_id},
                        {"Col": "Date", "Value": date},
                        {"Col": "Region", "Value": os_region},
                        {"Col": "Marine biome", "Value": marine_biome},
                        {"Col": "Depth Layer Zone", "Value": depth_layer},
                        {"Col": "Depth (top)", "Value": depth_top},
                        {"Col": "Depth (nominal)", "Value": depth_nom},
                        {"Col": "Sea Surface Temp",
                            "Value": sea_surface_temp},

                        {"Col": "Nitrate (M)", "Value": nitrate},
                        {"Col": "Phosphate (median)", "Value": phosphate_med},
                        {"Col": "Phosphate (max)", "Value": phosphate_max},
                        {"Col": "Chlorophyll", "Value": chlorophyll},
                        {"Col": "Carbon production", "Value": carbon_production},
                    ]

                    # Define the DataTable for selected point information
                    selected_info_table = dash_table.DataTable(
                        columns=[{"name": "Attribute", "id": "Col"},
                                 {"name": "Value", "id": "Value"}],
                        data=data,
                        style_table=table_style,
                        style_data_conditional=[
                            {'if': {'row_index': 'odd'},
                             'backgroundColor': '#f8f9fa',
                             }],
                        style_cell={'fontSize': '13px',
                                    'whiteSpace': 'normal',
                                    'paddingLeft': '10px',
                                    'paddingRight': '10px',
                                    'textAlign': 'left'},

                        style_header={
                            # 'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        page_size=8,   # Display 8 values per page
                    )

                    return dbc.Card([
                        html.H5("Explore points", className="card-title",
                                style={'marginTop': '15px',
                                       'marginBottom': '0px',
                                       'marginLeft': '15px',
                                       'paddingLeft': '15px',
                                       'paddingTop': '15px'}),
                        dbc.CardBody(selected_info_table)
                    ], style=info_box_style_a)
    # If no point is clicked, display default message
    return info_box


# ---------- Scatter plot (updates based on selected attributes) ----------
@app.callback(
    Output('scatter_plot', 'figure'),
    [Input('year_range_slider', 'value'),
     Input('scatter_dropdown_x', 'value'),
     Input('scatter_dropdown_y', 'value'),
     Input('scatter_color', 'value')]
)
def update_scatter_plot(year_range, attribute_x, attribute_y, color_by):

    dff = df[df['Year'].between(year_range[0], year_range[1])]

    plot_columns_x = ['Sea Surface Temp']
    plot_columns_y = ['SILVA_species_rich']

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
                     color=color_by,
                     hover_name='Year',
                     title='Scatter Plot')

    return fig


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

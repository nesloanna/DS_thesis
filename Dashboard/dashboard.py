import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table, State
import dash
import dash_bootstrap_components as dbc
import math


# os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
# print(os.getcwd())

# ------- Load and prepare datasets -------
df = pd.read_csv(
    "https://github.com/nesloanna/TARA_deploy_app/releases/download/data_new/dash_Tara_2024.csv")


# df = pd.read_csv("dash_Tara_2024.csv")

all_data_points = len(df)

# Make new column 'No category' for coloring
df = df.assign(**{"No category": "Sample point"})

df_time = df.copy()

df = df.sort_values(by=['Date/Time'])


# Function to find numeric columns

def numeric_columns(df):
    numeric_cols = []
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
    return numeric_cols


numeric_cols = numeric_columns(df)
# print(numeric_cols)

# Fill missing values in the entire DataFrame
df.fillna('NaN', inplace=True)


# ------- Year slider -------
year_min, year_max = df['Year'].min(), df['Year'].max()

all_years = list(range(year_min, year_max + 1))  # Find all years within range

# year_marks = {year: str(year)
#               for year in all_years}  # Create marks for each year

year_marks = {str(year): '' if year != year_min and year != year_max else str(
    year) for year in range(year_min, year_max + 1)}


# ------- Dropdown options -------

# Dropdown - Explore missing values
dropdown_options = [{'label': col, 'value': col} for col in df.columns[1:]]

# Dropdown - numerical attributes
dropdown_numerical = [{'label': col, 'value': col}
                      for col in numeric_cols if col != 'Year']

scatter_color_cols = ['Depth Layer', 'MHW count',
                      'MHW category', 'MP biome'] + numeric_cols

dropdown_scatter_color = [{'label': col, 'value': col}
                          for col in scatter_color_cols if col != 'Year']


# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home – Overview", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Focus", href="/focus", active="exact")),
        dbc.NavItem(dbc.NavLink("About", href="/about", active="exact")),
    ],
    brand="Tara Oceans Dashboard",
    brand_href="/",
    color="#233d4a",
    # sticky="top",
    dark=True,
    style={'paddingLeft': '2%', 'paddingRight': '2%'},
    fluid=True,
)


# Define the layout for the Focus page
layout_focus = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([  # Row with sidebar, ocean map, info box
            dbc.Col([
                html.Div([  # Dropdown for scatter plot
                    html.H3("Scatterplot"),
                    html.H6('Attribute for y-axis:'),
                    dcc.Dropdown(id='scatter_dropdown_y',
                                 options=dropdown_numerical,
                                 multi=False,
                                 clearable=False,
                                 value='SILVA_species_rich'),
                    html.H6('Attribute for x-axis:'),
                    dcc.Dropdown(id='scatter_dropdown_x',
                                 options=dropdown_numerical,
                                 multi=False,
                                 clearable=False,
                                 value='Sea Surface Temp'),
                    html.H6('Attribute for color:'),
                    dcc.Dropdown(id='scatter_color',
                                 options=dropdown_scatter_color,
                                 multi=False,
                                 clearable=True,
                                 value='',
                                 style={'marginTop': 0}),
                ], className="scatter-container"),
            ], width=2),
            dbc.Col(
                html.Div([  # Scatter plot
                    dcc.Graph(id='scatter_plot')
                ], className="figure-container"),
                width=7, className="scatter_plot"),

        ])], fluid=True),

])


# Define the layout for the Info page
layout_about = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2("Tara Oceans Dashboard",
                            style={'text-align': 'center'}),
                    html.H4("A Visualization of Ocean Data",
                            style={'text-align': 'center'}),
                    html.H4("The Dashboard", style={'margin-top': '30px'}),
                    html.P(
                        ["This dashboard application is part of the master's thesis project ",
                         html.Em("Exploration of Ocean Biodiversity Data"),
                         ". It is developed by ",
                         html.A("Anna Olsen",
                                href="https://github.com/nesloanna/"),
                         " using Python, Plotly, Dash, and Pandas."]),
                    html.H4("The Ocean Data"),
                    html.P([
                        "The data used in the dashboard is from the ",
                        html.A(
                            "Tara Oceans", href="https://fondationtaraocean.org/en/expedition/tara-oceans/"),
                        " Expedition (2009-2013) and retrieved from ",
                        html.A("PANGAEA", href="https://www.pangaea.de/"),
                        ". The specific datasets used are: ",
                        html.A("Biodiversity context (2015)",
                               href="https://doi.pangaea.de/10.1594/PANGAEA.853809"),
                        ", and Environmental context about ",
                        html.A("mesoscale features (2017)",
                               href="https://doi.pangaea.de/10.1594/PANGAEA.875577"),
                        " and ",
                        html.A("nutrients (2017)",
                               href="https://doi.pangaea.de/10.1594/PANGAEA.875575"),
                        ".",
                    ]),
                    html.H4("Marine Heatwaves"),
                    html.P(["Marine heatwaves (MHWs) are detected at the Tara Oceans sampling locations using the ",
                            html.A(
                                "marineHeatWaves", href="https://github.com/ecjoliver/marineHeatWaves"),
                            """ module. Additional data about daily Sea Surface
                            Temperatures (from 1981-2013) is from the """,

                            html.A("NOAA OI SST V2 High Resolution Dataset",
                                   href="https://psl.noaa.gov/data/gridded/data.noaa.oisst.v2.highres.html"),
                           ".",
                            ]),

                ], className="about-container"),
            ],
                width=9,
            ),
        ]),
    ])
])


# ------- Left sidebar for filtering -------

sidebar = html.Div([
    html.H4("Map filters", className="sidebar-heading"),
    html.Hr(className="sidebar-divider"),
    html.P('Years'),
    dbc.Container(
        dcc.RangeSlider(
            id='year_range_slider',
            min=year_min,
            max=year_max,
            step=1,
            marks=year_marks,
            value=[year_min, year_max],
            tooltip={"placement": "bottom", "always_visible": False},
            # vertical=False,
        ), style={'marginTop': '-10px', 'marginBottom': '14px',
                  'marginLeft': '-10px', 'marginRight': '-10px',
                  'padding': '0px',
                  'width': '110%'},
    ),
    html.P("Explore missing values"),
    dcc.Dropdown(
        id='value_dropdown',
        options=dropdown_options,
        # value='Nitrate',  # Default value
        placeholder='Choose an attribute',
        clearable=False,
        className="sidebar-dropdown",
    ),
    dbc.RadioItems(
        id='checklist',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'Not missing', 'value': 'values'}
        ],
        value='all',
        inline=True,
        style={'margin-bottom': '22px'},
    ),
    html.Div([
        html.P("Filtered data: ", className="html-p"),
        html.Div(id='filtered-count', className="html-p filtered-count"),
    ], className="flex-container"),

    html.Div([
        html.P("All data: ", className="html-p"),
        html.P(f"{all_data_points}", id="all-data", className="html-p"),
    ], className="flex-container")

],
    className="sidebar-container")


# ------- Info box -------


box_options = [
    {'label': 'Sea Surface Temp', 'value': 'Sea Surface Temp'},
    {'label': 'Nitrate', 'value': 'Nitrate'},
    {'label': 'Phosphate', 'value': 'Phosphate median'},
    {'label': 'Depth top', 'value': 'Depth top'},
    {'label': 'Depth nominal', 'value': 'Depth nominal'},
    {'label': 'Chlorophyll a', 'value': 'Chlorophyll a'},
]


# ------- Plotly, dash and mapbox -------
px.set_mapbox_access_token(
    'pk.eyJ1Ijoia29ydHBsb3RseSIsImEiOiJjbHBoNDZmZm0wMHUyMnJwNm5yM3RtcjY1In0.qxuHfESjhBp1wqT9ByZc0g')


stylesheets = [
    dbc.themes.FLATLY,
    {
        "href": "assets/custom.css",  # Path to custom CSS file
        "rel": "stylesheet",
    },
]

# create the dash application using the above layout definition
app = dash.Dash(__name__, external_stylesheets=stylesheets,
                suppress_callback_exceptions=True)

server = app.server


app.title = "Tara Oceans Dash"  # Title of the dashboard


# load_figure_template('FLATLY')
load_figure_template(["cerulean", "zephyr"])


# -------------------- Dashboard layout --------------------
layout_home = html.Div([
    navbar,
    dbc.Container([
        dbc.Row([  # Row with sidebar, ocean map, info box
            dbc.Col([
                sidebar,
                html.Div([
                    html.H5("Explore categories",
                            className='sidebar-s-heading'),
                    html.P('Color points by:',
                           #    className="sidebar-text"
                           ),
                    dcc.Dropdown(
                        id='map-color-input',
                        options=[
                            {"label": 'Ocean and sea region', "value": 'OS region'},
                            {"label": 'Marine heatwave category',
                                "value": 'MHW category'},
                            {"label": 'Marine heatwave count',
                                "value": 'MHW count'},
                            {"label": 'Marine biome', "value": 'MP biome'},
                            {"label": 'Depth Layer Zone',
                                "value": 'Depth Layer Zone'},
                            {"label": 'Campaign', "value": 'Campaign'},
                            {"label": 'No colors', "value": 'No category'},
                        ],
                        value='OS region',  # Default value
                        clearable=False,
                        className="sidebar-dropdown",
                    ),

                ], className='sidebar-container')
            ],
                # width=2,
                # width={"size": 2, "order": 1, "offset": 0},
                xs=3, sm=3, md=2, lg=2, xl=2, xxl=2,
                # className="column",

            ),
            dbc.Col([
                html.Div([  # Ocean map
                    dcc.Graph(id='ocean_map',
                              clickData={'points': [{'customdata': ''}]}
                              ),
                ], className="map-container")],
                # width=7,
                # width={"size": 7, "order": 2, "offset": 0},
                xs=6, sm=6, md=7, lg=7, xl=7, xxl=7,
                className="column",
            ),
            dbc.Col([  # Info box
                html.Div([
                    dbc.Tabs([
                        dbc.Tab(label="Box plot", tab_id="boxplot"),
                        dbc.Tab(label="Table", tab_id="table"),
                    ], id="tabs"),], className='tabs-container'),
                html.Div([
                    html.Div(id="tab-content"),
                    html.Div(id='selected_point_info',
                             style={'display': 'none'}),
                ], className="box-info-container"
                ),
                # width={"size": 3, "order": 3, "offset": 0, "lg": 2},
            ], xs=3, sm=3, md=3, lg=3, xl=3, xxl=3,
                # className="column",
            ),
        ]),
        dbc.Row([
                dbc.Col(width=2),
                dbc.Col(
                    html.Div([
                        html.P('Select attribute for timeline: ',
                               className="time-container-p"),

                    ], className="time-container"),
                    width=3,
                ),
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_time',
                            options=dropdown_numerical,
                            value='Sea Surface Temp',  # Default value
                            clearable=False,
                            style={'width': '100%', 'text-align': 'left'},
                            className="timeline-dropdown",
                        ),
                    ], className="time-container"),
                    width=5),
                dbc.Col(width=2),
                ]),

        dbc.Row([
                dbc.Col(
                    html.Div(
                        dcc.Graph(id='timeseries',
                                  clickData={'points': [{'text': ''}]},
                                  ), className="timeline-container")
                )
                ]),
        # Add this to your layout
        dcc.Store(id='last_map_clicked', data=None),

    ], fluid=True),
])


# Define the callback to switch between pages
@ app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/about':
        return layout_about
    elif pathname == '/focus':
        return layout_focus
    else:
        return layout_home


# Define the main layout of the app
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', className='dashboard-background')
])


# Callback to switch between tabs
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(active_tab):

    if active_tab == "boxplot":
        return html.Div([
            html.H4("Explore points",
                    style={'text-align': 'left'}),
            html.H6("Click on a point on the map or timeline to see it on the box plot.",
                    style={'text-align': 'left', 'margin-bottom': '30px'}),
            html.P("Select attribute"),
            dcc.Dropdown(
                id='boxplot_dropdown',
                # options=box_options,
                options=dropdown_numerical,
                value='Sea Surface Temp',  # Default value
                clearable=False,
                style={'width': '90%'},
                className="sidebar-dropdown",
            ),
            dcc.Graph(id='box_plot', figure={}),

        ],
            # className="figure-container"
        )

    elif active_tab == "table":
        return html.Div([
            html.H4("Explore points"),
            html.H6("Click on a point on the map or timeline to see its information.",
                    style={'text-align': 'left', 'margin-bottom': '30px'}),
            html.Div(id='selected_point_info_box'),
        ],
            # className="figure-container"
        )


# ------- Box plot (selected point) -------

@ app.callback(
    Output('box_plot', 'figure'),
    [Input('selected_point_info', 'children'),
     Input('boxplot_dropdown', 'value'),
     Input('map-color-input', 'value')]
)
def update_box_plot(selected_point_info, selected_column, color_category):

    extra_box_plot = ['OS region', 'MP biome', 'Depth Layer Zone', 'Campaign']

    fig = go.Figure(
        data=[go.Box(y=df[selected_column],
                     boxpoints=False,  # 'all', 'outliers', or 'suspectedoutliers' or False
                     jitter=0.7,  # add some jitter for a better separation between points
                     pointpos=-1.8,  # relative position of points wrt box
                     name="All",  # Set the name for the first box plot
                     showlegend=False,
                     hoverinfo='y',
                     )])

    # If a point is selected, add a marker for the selected point on the box plot
    if selected_point_info:
        sample_id = selected_point_info

        selected_row = df[(df['Sample ID'] == sample_id)].iloc[0]

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

        # If the color category is in list, add a box plot for the selected subcategory
        if color_category in extra_box_plot:
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
        title=f'<i>{selected_column}</i>',  # Set the title
        title_x=0.75,
        title_y=0.94,
        margin=dict(t=50, l=30, b=20, r=10),  # Margin of plot
        legend=dict(x=0.82, y=1.1),
        height=270,
        # width="50%",
        title_font=dict(size=14)
    )

    return fig


# Callback to store the selected point information when a point is clicked on the map
@ app.callback(
    Output('selected_point_info', 'children'),
    [Input('ocean_map', 'clickData'),
     Input('timeseries', 'clickData')]
)
def store_selected_point_info(map_clicked, timeline_clicked):

    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]

    selected_point_info = None

    if "ocean_map.clickData" in trigger:
        selected_point_info = map_clicked['points'][0]['customdata'][0]

    elif "timeseries.clickData" in trigger:
        selected_point_info = timeline_clicked['points'][0]['text']

    return selected_point_info


# ------- Ocean map - Plot sample locations -------
# Define your list of colors
custom_colors = [
    '#388E3C', '#FFEE58', '#FFA726', '#C2185B', '#EA80FC',
    '#A7FFEB', '#7E57C2', '#EC7063', '#0277BD', '#82E0AA',
    '#795548', '#689F38', '#26C6DA', '#8BC34A', '#239B56',
    '#FFEB3B', '#81C784', '#26A69A', '#EF5350', '#229954',
    '#607D8B', '#AB47BC', '#73C6B6', '#F9A825', '#4DD0E1',
    '#2471A3', '#C39BD3', '#F5B7B1', '#00BCD4', '#AB47BC',
    '#01579B', '#48C9B0', '#16A085', '#388E3C', '#9575CD',
    '#1976D2', '#3F51B5', '#4CAF50', '#626567', '#FF80AB',
    '#00B8D4', '#CE93D8', '#E91E63', '#7D3C98', '#ABEBC6',
    '#2E7D32', '#F4D03F', '#283593', '#80DEEA', '#FF8F00',
    '#1A5276', '#B388FF', '#76448A', '#839192', '#304FFE',
]

# Define the labels dictionary
legend_labels = {
    "OS region": "OS<br>Region",
    "MHW category": "MHWs category",
    "MHW count": "MHWs count",
    "MP biome": "Marine Biome",
    "Depth Layer Zone": "Depth Layer",
    "Campaign": "Campaign",
    "No category": "No color",
}


@ app.callback(
    [Output('ocean_map', 'figure'),
     Output('filtered-count', 'children')],
    [Input('year_range_slider', 'value'),
     Input('value_dropdown', 'value'),
     Input('checklist', 'value'),
     Input('map-color-input', 'value'),
     Input('selected_point_info', 'children')])
def plot_samples_map(year_range, selected_column, checklist, color_by, selected_point):

    dff = df[df['Year'].between(year_range[0], year_range[1])]

    dff['MHW count'] = dff['MHW count'].astype(str)

    # Filter DataFrame based on selected column and checklist options
    if 'values' in checklist:
        dff = dff[dff[selected_column] != 'NaN']  # Filter out rows with 'NaN'

    map_fig = px.scatter_mapbox(dff,
                                lat=dff['Latitude'],
                                lon=dff['Longitude'],
                                color=color_by,
                                color_discrete_sequence=custom_colors,
                                zoom=0.8,
                                height=550,
                                # width=800,
                                title=None, opacity=.6,
                                custom_data=[
                                    'Sample ID', 'Date',
                                    'Station', 'Campaign',
                                    'OS region', 'MP biome',
                                    'Depth Layer Zone', 'Depth top',
                                    'Sea Surface Temp', 'MHW category', 'MHW count',
                                    'Latitude', 'Longitude'],
                                )

    # Define a custom hover template
    hover_template = '<b>%{customdata[0]}</b><br>' \
        'Date: %{customdata[1]}<br>' \
        'Station: %{customdata[2]}<br>' \
        'Campaign: %{customdata[3]}<br>' \
        'Region: %{customdata[4]}<br>' \
        'Marine biome: %{customdata[5]}<br>' \
        '%{customdata[6]}<br>' \
        'Depth: %{customdata[7]}<br>' \
        'SST: %{customdata[8]:.2f}<br>' \
        'Marine Heatwaves: %{customdata[10]} (%{customdata[9]})<br>' \
        'Lat: %{customdata[11]:.3f}, Lon: %{customdata[12]:.3f}<extra></extra>'

    # Update the hover template
    map_fig.update_traces(hovertemplate=hover_template)

    # Add custom legend labels
    legend_title = legend_labels.get(color_by, "Legend")

    map_fig.update_layout(
        mapbox_style='mapbox://styles/kortplotly/clsyukswv002401p8a4xtbbm3',
        margin={"r": 0, "l": 0, "b": 10, "t": 0},
    )

    legend_show = ["MP biome", "OS region", "Depth Layer Zone",
                   "MHW category", "MHW count"]

    if color_by in legend_show:
        map_fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                x=0,
                y=-0.095,
                yanchor="bottom",
                xanchor="left",
                xref='paper',  # paper / container
                yref='paper',
                bordercolor="White",
                borderwidth=5,
                # bgcolor="White",
                # Set the legend title dynamically
                title=legend_title,
                indentation=-6,
                font=dict(size=12),
            ))
    else:

        map_fig.update_layout(
            showlegend=False,
            margin={"r": 0, "l": 0, "b": 0, "t": 0},
        )

    # to preserve the UI settings such as zoom and panning in the update
    # map_fig['layout']['uirevision'] = 'unchanged'
    # Apply the configuration options to the figure
    # Apply the configuration options directly to the figure

    # Get the count of filtered records
    count = len(dff)

    # ---- Update map if point is clicked on timeline ----
    if selected_point:

        selected_row = dff[dff['Sample ID'] == selected_point].iloc[0]

        # Get the latitude and longitude of the corresponding point
        latitude = selected_row['Latitude']
        longitude = selected_row['Longitude']

        # Update the hover text to include additional information
        # hover_text = f'<b>Selected Point</b> <br><br>' \
        #     f'{selected_row['Sample ID']} <br>' \
        #     f'Date:</b> {selected_row['Date']} <br>' \
        #     f'Station: {selected_row['Station']}<br>' \
        #     f'Campaign: {selected_row['Campaign']}<br> ' \
        #     f'{selected_row['OS region']}<br> ' \
        #     f'{selected_row['MP biome']}<br> ' \
        #     f'{selected_row['Depth Layer Zone']}<br> ' \
        #     f'Lat: {selected_row['Latitude']:.3f}, Lon: {
        #         selected_row['Longitude']:.3f}'

        # Update the layout and return the modified figure
        map_fig.update_layout(
            mapbox=dict(
                center=dict(lat=latitude, lon=longitude),
                zoom=1.7,  # Adjust zoom level as needed
            ),
        )

        # Update the marker style of the corresponding point on the map
        map_fig.add_trace(go.Scattermapbox(
            lat=[latitude],
            lon=[longitude],
            mode='markers',
            marker=dict(
                size=15,
                color='red',  # Change marker color to black
                opacity=0.75,
                symbol='circle',  # Change marker symbol to circle
            ),
            name='Selected point',
            hoverinfo='text',
            text="<br><b>Seleced Point </b> <br><br>"
            # text=hover_text,
        ))

        return [map_fig, f"{count}"]

    return [map_fig, f"{count}"]


# ------- Clicks on map -------


@ app.callback(
    Output('selected_point_info_box', 'children'),
    [Input('selected_point_info', 'children')]
)
def display_selected_point_info(selected_point):
    if not selected_point:
        return

    dff = df.copy()
    selected_row = dff[dff['Sample ID'] == selected_point].iloc[0]

    data = [
        {"Attribute": "Sample ID", "Value": selected_row['Sample ID']},
        {"Attribute": "Date", "Value": selected_row['Date']},
        {"Attribute": "Campaign", "Value": selected_row['Campaign']},
        {"Attribute": "Region", "Value": selected_row['OS region']},
        {"Attribute": "Marine biome", "Value": selected_row['MP biome']},
        {"Attribute": "Depth Layer Zone",
            "Value": selected_row['Depth Layer Zone']},
        {"Attribute": "Depth (top)", "Value": selected_row['Depth top']},
        {"Attribute": "SST", "Value": selected_row['Sea Surface Temp']},
        {"Attribute": "Marine Heatwave category",
            "Value": selected_row['MHW category']},
        {"Attribute": "Marine Heatwave count",
            "Value": selected_row['MHW count']},
        {"Attribute": "Nitrate", "Value": selected_row['Nitrate']},
        {"Attribute": "Phosphate",
         "Value": selected_row['Phosphate median']},
        {"Attribute": "Iron", "Value": selected_row['Iron']},
        {"Attribute": "Chlorophyll a", "Value": selected_row['Chlorophyll a']},
        {"Attribute": "Carbon Production",
            "Value": selected_row['Net PP carbon 30']},
        {"Attribute": "Latitude", "Value": selected_row['Latitude']},
        {"Attribute": "Longitude", "Value": selected_row['Longitude']},
    ]

    selected_info_table = dash_table.DataTable(
        columns=[{"name": "Attribute", "id": "Attribute"},
                 {"name": "Value", "id": "Value"}],
        data=data,
        # style_table=table_style,
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'}
        ],
        style_cell={'fontSize': '12px', 'whiteSpace': 'normal',
                    'paddingLeft': '10px', 'paddingRight': '10px',
                    'textAlign': 'left'},
        style_header={'color': 'black', 'fontWeight': 'bold'},
        page_size=9,
    )

    return html.Div(selected_info_table, className="table-style")


# ------- Scatter plot (updates based on selected attributes) -------
@ app.callback(
    Output('scatter_plot', 'figure'),
    [Input('scatter_dropdown_x', 'value'),
     Input('scatter_dropdown_y', 'value'),
     Input('scatter_color', 'value')]
)
def update_scatter_plot(attribute_x, attribute_y, color_by):

    # dff = df[df['Year'].between(year_range[0], year_range[1])]
    dff = df_time.copy()

    plot_columns_x = ['Sea Surface Temp']
    plot_columns_y = ['SILVA_species_rich']

    # Add selected attributes to the plot columns if they exist
    if attribute_x:
        plot_columns_x[0] = attribute_x

    if attribute_y:
        plot_columns_y[0] = attribute_y

    if color_by:
        # Create scatter plot
        fig = px.scatter(dff,
                         height=500,
                         x=plot_columns_x[0],
                         y=plot_columns_y[0],
                         color=color_by,
                         hover_name='Sample ID',
                         template="zephyr",
                         )

    else:
        # Create scatter plot
        fig = px.scatter(dff,
                         height=500,
                         x=plot_columns_x[0],
                         y=plot_columns_y[0],
                         hover_name='Sample ID')

    fig.update_layout(
        margin=dict(t=20, l=20, b=20, r=20),  # Margin of plot

    )

    return fig


# ------- Time series plot -------

def reduce_datapoints(df, focus_attribute, percentage_threshold):
    max_val = df[focus_attribute].max()
    min_val = df[focus_attribute].min()
    val_range = max_val - min_val

    percentage_diff = (
        np.abs(df[focus_attribute][1:].to_numpy() -
               df[focus_attribute][0:-1].to_numpy())
        / val_range
    )

    mask_a = percentage_diff < percentage_threshold
    mask_b = df["Date"][1:].to_numpy() == df["Date"][0:-1].to_numpy()
    mask_a = np.insert(mask_a, 0, False, axis=0)
    mask_b = np.insert(mask_b, 0, False, axis=0)

    mask = mask_a * mask_b
    mask_valid = mask == False

    mask_c = df[focus_attribute].isna()
    mask_nan = (mask_b == False) * mask_c

    df_temp = df[0:]
    df_valid = df_temp[mask_valid]
    df_nan = df_temp[mask_nan]
    df_nan[focus_attribute] = min_val - (val_range * 0.05)
    max_value = max_val + (val_range * 0.1)
    min_value = min_val - (val_range * 0.1)
    # df_nan = df_temp[df_temp[focus_attribute].isna()]

    return df_valid, df_nan, max_value, min_value


@ app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='dropdown_time', component_property='value'),
     Input(component_id='selected_point_info', component_property='children'),
     Input(component_id='map-color-input', component_property='value')]
)
def update_timeline(selected_variable, selected_point_info, color_by):

    fig = go.Figure()

    df_temp = df_time.copy()
    df_temp = df_temp.dropna(subset=["Latitude", "Longitude"])
    df_temp = df_temp.sort_values(by=["Date", selected_variable])
    df_temp.reset_index(drop=True, inplace=True)

    dff, dff_nan, max_value_plot, min_value_plot = reduce_datapoints(
        df_temp, selected_variable, 0.01)

    # Get unique values in the selected category
    unique_values = dff[color_by].unique()

    # Generate a colorscale based on the unique values
    num_unique_values = len(unique_values)
    colorscale = custom_colors[:num_unique_values]

    # Create a mapping dictionary for colors based on the unique values
    category_color_mapping = dict(zip(unique_values, colorscale))

    # Map the colors based on the unique values and create a new 'Color' column
    dff['Color'] = dff[color_by].map(category_color_mapping)

    # Points with values
    fig.add_trace(go.Scatter(
        x=dff['Date'],
        y=dff[selected_variable],
        mode='markers+lines',
        marker=dict(
            color=dff['Color'],  # Use 'Color' column for coloring the points
        ),
        line=dict(color='lightgrey', width=1),
        name="With value",
        text=dff['Sample ID'],
        hovertemplate="<b>%{text}</b><br>" +
        "%{x|%Y-%m-%d}<br>" +
        # f"{color_by}: ...<br>" +
        f"{selected_variable}: " +
        "%{y:.3f}<extra></extra>"
    ))

    # Points with NaN-values
    fig.add_trace(go.Scatter(
        x=dff_nan['Date'],
        y=dff_nan[selected_variable],
        mode='markers', marker=dict(size=6, color='lightgrey'),
        name="Without value",
        text=dff_nan['Sample ID'],
        hovertemplate="<b>%{text}</b><br>" +
        "%{x|%Y-%m-%d}<br>" +
        f"{selected_variable}: NaN<extra></extra>"
    ))

    # If a point is selected, add a marker for the selected point on the box plot
    if selected_point_info:
        sample_id = selected_point_info
        selected_row = df_temp[(df_temp['Sample ID'] == sample_id)].iloc[0]
        selected_value = selected_row[selected_variable]
        selected_date = selected_row['Date']

        if math.isnan(selected_value):
            fig.add_trace(go.Scatter(
                x=[selected_date], y=dff_nan[selected_variable], mode='markers',
                marker=dict(color='red', size=15, opacity=0.75), name="Point",
                showlegend=True,
                text=df_temp['Sample ID'],
                hovertemplate="<b>%{text}</b><br>" +
                "%{x|%Y-%m-%d}<br>" +
                f"{selected_variable}: NaN<extra></extra>"
            ))

        else:
            fig.add_trace(go.Scatter(
                x=[selected_date], y=[selected_value], mode='markers',
                marker=dict(color='red', size=15, opacity=0.75), name="Point",
                showlegend=True,
                text=df_temp['Sample ID'],
                hovertemplate="<b>%{text}</b><br>" +
                "%{x|%Y-%m-%d}<br>" +
                f"{selected_variable}: " +
                "%{y:.3f}<extra></extra>"
            ))

            # Adding vertical lines for specific dates
    years_to_mark = [2010, 2011, 2012, 2013]  # Specify the years

    for year in years_to_mark:

        # January 1st of each year
        line_date = pd.Timestamp(year, 1, 1)

        fig.add_shape(type="line",
                      x0=line_date, y0=min_value_plot,
                      x1=line_date, y1=max_value_plot,
                      line=dict(color="black",
                                width=1, dash="dash"),
                      )

        fig.add_annotation(x=line_date, y=max_value_plot,
                           text=str(year), showarrow=False,
                           xshift=30, yshift=-10,
                           font=dict(color="black", size=11)
                           )

    # fig.update_traces(line_color=dff['Color'].iloc[:, 1])

    fig.update_layout(
        title=f'{selected_variable} over time',
        title_x=0.5,  # Center the title
        title_y=0.95,
        margin=dict(t=30, l=20, b=20, r=20),  # Margin of plot
        showlegend=True,
        legend=dict(x=0.9, y=1.15),
        xaxis=dict(
            tickmode='linear',  # Set tick mode to linear
            dtick='M1',  # Set tick frequency to one month (M1)
            tickformat='%b',  # Format tick labels to display only the month abbreviation
            # Set the range of the x-axis to start from August and end with January
            range=['2009-08-01', '2014-01-01']
        ))

    if color_by != "No category":
        fig.update_layout(
            legend=dict(
                title=f'Colored by<br>{color_by}',
                x=0.9, y=1.15,
            )
        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)


# # start the web application
# if __name__ == '__main__':
#     app.run_server(debug=True, port=8059)

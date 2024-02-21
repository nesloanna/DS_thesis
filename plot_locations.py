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
from dash.exceptions import PreventUpdate
app = Dash()


os.chdir("/Users/annaolsen/Desktop/Speciale/DS_thesis/data")
print(os.getcwd())

# Load datasets
df = pd.read_csv("Tara_plot.csv")

# Removing rows with empty longitude or latitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# If you want to reset the index after dropping rows
df.reset_index(drop=True, inplace=True)

px.set_mapbox_access_token(
    'pk.eyJ1Ijoia29ydHBsb3RseSIsImEiOiJjbHBoNDZmZm0wMHUyMnJwNm5yM3RtcjY1In0.qxuHfESjhBp1wqT9ByZc0g')


# create the dash application using the above layout definition
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# load_figure_template('FLATLY')

# Dashboard layout
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
                        dcc.Graph(id='ocean_map'),
                        dcc.Input(id='dummy-input', type='hidden',
                                  value='trigger-callback'),
                    ]), width=15, className="scatter_map"),
                ]),
        dbc.Row([  # Row with sidebar and map
                dbc.Col(
                    html.Div([
                        dcc.Graph(id='ocean_globe'),
                    ]), width=15, className="scatter_globe"),
                ]),

    ]),
])


# Plot crash locations on map

@app.callback(
    Output('ocean_map', 'figure'),
    [Input('dummy-input', 'value')]  # Dummy input to trigger callback
)
def plot_samples_map(dummy_input):
    fig = px.scatter_mapbox(df, lat=df['Latitude'], lon=df['Longitude'],
                            color='OS region',
                            zoom=0.5, height=700,
                            title=None, opacity=.5,
                            )

    fig.update_layout(mapbox_style='mapbox://styles/kortplotly/clsvyfa7c007e01qz44qfeq61',
                      margin={"r": 0, "l": 0, "b": 0})
    # to preserve the UI settings such as zoom and panning in the update
    fig['layout']['uirevision'] = 'unchanged'

    return fig


# Plot sample locations on globe
@app.callback(
    Output('ocean_globe', 'figure'),
    [Input('dummy-input', 'value')]  # Dummy input to trigger callback
)
def plot_samples_globe(dummy_input):

    fig = go.Figure(go.Scattergeo())
    fig.update_geos(projection_type="orthographic")  # or "natural earth"

    fig.add_trace(
        go.Scattergeo(
            lat=df['Latitude'],
            lon=df['Longitude'],
            mode='markers',
            # color='OS region_D',
            marker=dict(color='red', size=4),
            # hoverinfo='text'
        )
    )

    fig.update_layout(
        mapbox_style='mapbox://styles/kortplotly/clsvyfa7c007e01qz44qfeq61',
        title=None,
        margin={"r": 0, "l": 0, "b": 0}
    )

    # to preserve the UI settings such as zoom and panning in the update
    fig['layout']['uirevision'] = 'unchanged'

    return fig


# start the web application
if __name__ == '__main__':
    app.run_server(debug=True, port=8058)

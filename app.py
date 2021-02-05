import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json

DEFAULT_PLOT_LAYOUT = dict(
    hovermode="x unified",
    plot_bgcolor="#4e5d6c",
    paper_bgcolor="#4e5d6c",
    font=dict(color="#EA526F"),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    # margin=dict(l=10, r=10, b=10, t=10),
    colorway=["#368F8B"],
    clickmode="event+select",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

# CONFIRMED US CASES
df_usa = pd.read_csv("data/time_series_covid_19_confirmed_US.csv")
px.set_mapbox_access_token(open(".mapbox_token").read())
with open("geojson_states.json") as f:
    states_geojson = json.load(f)
states = df_usa.groupby("Province_State").sum()
states = states.drop(
    [
        "American Samoa",
        "Diamond Princess",
        "Grand Princess",
        "Guam",
        "Puerto Rico",
        "Northern Mariana Islands",
        "Virgin Islands",
    ]
)
marks = {
    i: states[states.columns[11:]].columns[::30][i]
    for i in range(len(states[states.columns[11:]].columns[::30]))
}
states = states.reset_index().rename(columns={"Province_State": "name"})

app.layout = html.Div(
    className="grid-container",
    children=[
        html.Div(
            dbc.Card(
                [
                    dbc.CardHeader("Header"),
                    dbc.CardBody(
                        [
                            dcc.Slider(
                                id="map-slider",
                                min=0,
                                max=len(marks) - 1,
                                step=30,
                                marks=marks,
                                value=0,
                                updatemode="drag",
                                persistence=False,
                            ),
                            dcc.Graph(id="map"),  # graph on top
                        ]
                    ),
                ],
                color="secondary",
                style={"height": "100%"},
            ),
            className="geo-map",
        ),
        html.Div(
            dbc.Card(
                [
                    dbc.CardHeader("Header"),
                    dbc.CardBody(
                        dcc.Graph(  # state text on bottom
                            id="selected-state-line-graph",
                            # figure=dict(layout=DEFAULT_PLOT_LAYOUT),
                        ),
                    ),
                ],
                color="secondary",
                style={"height": "100%"},
            ),
            className="cases-graph",
        ),
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody("This is the body")],
                color="secondary",
                style={"height": "100%"},
            ),
            className="death-rate",
        ),
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody("This is the body")],
                color="secondary",
                style={"height": "100%"},
            ),
            className="survival-rate",
        ),
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody("This is the body")],
                color="secondary",
                style={"height": "100%"},
            ),
            className="some-other-rate",
        ),
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody("This is the body")],
                color="secondary",
                style={"height": "100%"},
            ),
            className="county-overview",
        ),
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody("This is the body")],
                color="secondary",
                style={"height": "100%"},
            ),
            className="another-thing",
        ),
    ],
)


@app.callback(
    Output("selected-state-line-graph", "figure"),
    [Input("map", "selectedData")],
)
def update(selected):
    print(selected)
    if selected:
        # selected is an object that looks like {'points': [{'location': ...}]}
        location = selected["points"][0]["location"]
        onestate = (
            df_usa.groupby("Province_State").sum()[df_usa.columns[11:]].loc[location]
        )
        fig = px.line(
            x=pd.to_datetime(onestate.index),
            y=onestate,
            color_discrete_sequence=["#a262a9"],
        )
        fig.update_layout(DEFAULT_PLOT_LAYOUT)
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Frequency")
        fig.update_xaxes(tickangle=315)
        return fig
    else:
        print("Nothing Selected")
        all_states = df_usa.sum()[df_usa.columns[11:]]
        fig = px.line(
            x=pd.to_datetime(all_states.index),
            y=all_states,
            color_discrete_sequence=["#a262a9"],
        )
        fig.update_layout(DEFAULT_PLOT_LAYOUT)
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Frequency")
        fig.update_xaxes(tickangle=315)
        return fig


@app.callback(
    Output("map", "figure"),
    [Input("map-slider", "value")],
    [State("map-slider", "marks")],
)
def update_slider(slide_val, marks):
    color = marks[str(slide_val)]
    fig = px.choropleth_mapbox(
        states,
        geojson=states_geojson,
        locations="name",
        color=color,
        featureidkey="properties.name",  # 'properties.name' in the states_geojson and 'name' in the states df match
        color_continuous_scale="Teal",
        range_color=(
            0,
            states[states.columns[11:]].max().max(),
        ),  # force the color scale to respect global max
        mapbox_style="mapbox://styles/gperrone/ck93esihw1tpa1itdwyjx0coe",
        zoom=2.7,
        center={"lat": 37.0902, "lon": -95.7129},
        opacity=0.8,
    )
    fig.update_layout(clickmode="event+select")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
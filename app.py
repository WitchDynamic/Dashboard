import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

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

app.layout = html.Div(
    className="grid-container",
    children=[
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody(dcc.Graph(figure=dict(layout=DEFAULT_PLOT_LAYOUT)))],
                color="secondary",
                style={"height": "100%"},
            ),
            className="geo-map",
        ),
        html.Div(
            dbc.Card(
                [dbc.CardHeader("Header"), dbc.CardBody("This is the body")],
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


if __name__ == "__main__":
    app.run_server(debug=True)
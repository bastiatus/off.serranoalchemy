import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Clasificación de Jamones", className="text-center"),
            width=12)
    ], style={'margin-top': '40px', 'margin-bottom': '30px'}),

    dbc.Row([
        dbc.Col(
            html.Label("Ingresar nutrientes del jamón:"),
            width=3, style={'text-align': 'center', 'margin': 'auto'}
        ),

        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Input(
                    id="calories".format("number"),
                    type="number",
                    placeholder="KiloCalorias".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),

                dbc.Col(dcc.Input(
                    id="proteins".format("number"),
                    type="number",
                    placeholder="Proteinas".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),

                dbc.Col(dcc.Input(
                    id="carbohydrates".format("number"),
                    type="number",
                    placeholder="Carbohidratos".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),

                dbc.Col(dcc.Input(
                    id="salt".format("number"),
                    type="number",
                    placeholder="Sal".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),
            ], style={'margin-bottom': '10px'}),

            dbc.Row([
                dbc.Col(dcc.Input(
                    id="sugar".format("number"),
                    type="number",
                    placeholder="Azucar".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),

                dbc.Col(dcc.Input(
                    id="saturated_fat".format("number"),
                    type="number",
                    placeholder="Grasas saturadas".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),

                dbc.Col(dcc.Input(
                    id="insaturated_fat".format("number"),
                    type="number",
                    placeholder="Grasas insaturadas".format("number")
                ), width=3, style={'text-align': 'center', 'margin': 'auto'}),
                dbc.Col(width=3)
            ], style={'margin-bottom': '10px'})
        ],
        width=9),
    ], style={'margin-bottom': '10px'}),

    dbc.Row([
        dbc.Col(width=3),
        dbc.Col(
            html.Div(
                dbc.Button("Calcular", id="calculate-button", color="primary", className="d-grid gap-2"),
                className="d-grid gap-2"
            ),
            width=6),
        dbc.Col(width=3)
    ], style={'margin-bottom': '20px'}),

    dbc.Row([
        dbc.Col(width=3),
        dbc.Col(
            html.Div([
                dcc.Graph(id="polar-chart"),
            ], className="d-grid gap-2")),
        dbc.Col(width=3)
    ])
])

@app.callback(
    Output("polar-chart", "figure"),
    [Input("calculate-button", "n_clicks")]
)
def update_output(n_clicks):
    if n_clicks is None or n_clicks == 0:
        # Return an empty figure if the button hasn't been clicked
        return px.line_polar()

    df = pd.DataFrame(dict(
        values = [8, 12, 7, 14, 10, 12, 8,
                  10, 3, 10, 10, 9, 13, 8],
        variable = ['Grasas insaturadas', 'Grasas saturadas', 'Sal', 'Carbohidratos', 'Azúcares', 'Proteinas', 'Kcalorías',
                    'Grasas insaturadas', 'Grasas saturadas', 'Sal', 'Carbohidratos', 'Azúcares', 'Proteinas', 'Kcalorías'],
        ham=['Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón',
               'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido',  'Tipo de jamón más parecido', 'Tipo de jamón más parecido']))
    print(df)
    fig = px.line_polar(df, r='values', theta='variable', line_close=True,
                        color='ham')
    fig.update_traces(fill='toself')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
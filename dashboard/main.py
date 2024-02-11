import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import joblib
import numpy as np

model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
clusters = pd.read_pickle("clusters.pkl")

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
            width=2, style={'text-align': 'right', 'margin': 'auto'}
        ),

        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Label("KiloCalorias"),
                        dcc.Input(
                            id="calories".format("number"),
                            type="number",
                            placeholder="200".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),

                dbc.Col([
                    html.Div([
                        html.Label("Proteinas"),
                        dcc.Input(
                            id="proteins".format("number"),
                            type="number",
                            placeholder="2".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),

                dbc.Col([
                    html.Div([
                        html.Label("Carbohidratos"),
                        dcc.Input(
                            id="carbohydrates".format("number"),
                            type="number",
                            placeholder="15".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),

                dbc.Col([
                    html.Div([
                        html.Label("Sal"),
                        dcc.Input(
                            id="salt".format("number"),
                            type="number",
                            placeholder="3".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'})
            ], style={'margin-bottom': '10px'}),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Label("Azucar"),
                        dcc.Input(
                            id="sugar".format("number"),
                            type="number",
                            placeholder="5".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),

                dbc.Col([
                    html.Div([
                        html.Label("Grasas saturadas"),
                        dcc.Input(
                            id="saturated_fat".format("number"),
                            type="number",
                            placeholder="6".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),

                dbc.Col([
                    html.Div([
                        html.Label("Grasas insaturadas"),
                        dcc.Input(
                            id="insaturated_fat".format("number"),
                            type="number",
                            placeholder="9".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),

                dbc.Col([
                    html.Div([
                        html.Label("Precio €/Kg"),
                        dcc.Input(
                            id="price".format("number"),
                            type="number",
                            placeholder="9".format("number"),
                            style={'width': '70%'}
                        ),
                    ], style={'display': 'flex', 'flexDirection': 'column'})
                ], width=3, style={'margin': 'auto'}),
            ], style={'margin-bottom': '10px'})
        ], width=8)

        ,

        dbc.Col(
            width=2, style={'text-align': 'right', 'margin': 'auto'}
        ),


    ], style={'margin-bottom': '10px'}),

    dbc.Row([
        dbc.Col(width=2),
        dbc.Col(
            html.Div(
                dbc.Button("Calcular", id="calculate-button", color="primary", className="d-grid gap-2",
                           disabled=True),
                className="d-grid gap-2"
            ),
            width=8),
        dbc.Col(width=2)
    ], style={'margin-bottom': '20px'}),

    dbc.Row([
        dbc.Row([
            html.Div([
                html.H5(id="dynamic-text"),
            ], style={'text-align': 'center', 'margin': 'auto'})
        ]),

        dbc.Row([
            html.Div([
                dcc.Graph(id="polar-chart"),
            ])
        ])
    ])
])

@app.callback(
    Output("calculate-button", "disabled"),
    [
        Input("calories", "value"),
        Input("proteins", "value"),
        Input("carbohydrates", "value"),
        Input("salt", "value"),
        Input("sugar", "value"),
        Input("saturated_fat", "value"),
        Input("insaturated_fat", "value"),
        Input("price", "value"),
    ],
)
def update_button_disabled(calories, proteins, carbohydrates, salt, sugar, saturated_fat, insaturated_fat, price):
    if None in [calories, proteins, carbohydrates, salt, sugar, saturated_fat, insaturated_fat, price]:
        return True
    else:
        return False


@app.callback(
    [Output("polar-chart", "figure"),
     Output("dynamic-text", "children")],
    [Input("calculate-button", "n_clicks")],
     [State("calories", "value"),
     State("proteins", "value"),
     State("carbohydrates", "value"),
     State("salt", "value"),
     State("sugar", "value"),
     State("saturated_fat", "value"),
     State("insaturated_fat", "value"),
     State("price", "value"),
     ]
)
def update_output(n_clicks, calories, proteins, carbohydrates, salt, sugar, saturated_fat, insaturated_fat, price):
    if n_clicks is None or n_clicks == 0:
        return px.line_polar(), ""
    else:
        feature_names = ["carbohydrates_100g", "energy-kcal_100g", "proteins_100g", "salt_100g", "saturated-fat_100g",
                         "sugars_100g", "insaturated-fat_100g"]

        input_values = np.array([carbohydrates, calories, proteins, salt, saturated_fat, sugar, insaturated_fat])
        input_data = pd.DataFrame([input_values], columns=feature_names)

        scaled_input = scaler.transform(input_data)
        scaled_input = pd.DataFrame(scaled_input, columns=feature_names)

        pred = model.predict(scaled_input)[0]
        most_similar_ham = clusters[clusters['cluster'] == pred][feature_names]

        df = pd.DataFrame(dict(
            values=list(scaled_input.values[0]) + list(most_similar_ham.values[0]),
            variable=feature_names*2,
            jamones=['Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón',
                 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido',
                 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido']))

        fig = px.line_polar(df, r='values', theta='variable', line_close=True, color='jamones')
        fig.update_traces(fill='toself')

        return fig, (f"Tu jamón pertenece al cluster {pred}, por lo que ha sido detectado como JAMÓN DE BELLOTA, "
                     f"con un precio medio de XX €/Kg")


if __name__ == '__main__':
    app.run_server(debug=True)
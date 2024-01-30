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
    [Input("calculate-button", "n_clicks")],
     [State("calories", "value"),
     State("proteins", "value"),
     State("carbohydrates", "value"),
     State("salt", "value"),
     State("sugar", "value"),
     State("saturated_fat", "value"),
     State("insaturated_fat", "value")
     ]
)
def update_output(n_clicks, calories, proteins, carbohydrates, salt, sugar, saturated_fat, insaturated_fat):
    if n_clicks is None or n_clicks == 0:
        return px.line_polar()
    else:
        feature_names = ["carbohydrates_100g", "energy-kcal_100g", "proteins_100g", "salt_100g", "saturated-fat_100g",
                         "sugars_100g", "insaturated-fat_100g"]
        feature_names_without_kcal = ["carbohydrates_100g", "proteins_100g", "salt_100g", "saturated-fat_100g",
                         "sugars_100g", "insaturated-fat_100g"]

        input_values = np.array([carbohydrates, calories, proteins, salt, saturated_fat, sugar, insaturated_fat])
        input_data = pd.DataFrame([input_values], columns=feature_names)

        scaled_input = scaler.transform(input_data)
        scaled_input = pd.DataFrame(scaled_input, columns=feature_names)

        pred = model.predict(scaled_input)[0]
        most_similar_ham = clusters[clusters['cluster'] == pred][feature_names]

        original_values = scaler.inverse_transform(most_similar_ham.values)
        original_values_without_kcal = [list(original_values[0])[0]] + list(original_values[0])[2:]
        input_data_without_kcal = list(input_data[["carbohydrates_100g", "proteins_100g", "salt_100g", "saturated-fat_100g",
                                          "sugars_100g", "insaturated-fat_100g"]].values[0])

    df = pd.DataFrame(dict(
        values=input_data_without_kcal + original_values_without_kcal,
        variable=feature_names_without_kcal*2,
        jamones=['Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón',
             'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido',
             'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido']))

    fig = px.line_polar(df, r='values', theta='variable', line_close=True, color='jamones')
    fig.update_traces(fill='toself')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
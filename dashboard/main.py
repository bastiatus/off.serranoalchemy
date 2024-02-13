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

# for server:
server = app.server

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
                        html.Label("KCal"),
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
                        html.Label("Azúcar"),
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
        ], width=8),

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
        html.Div([

            dbc.Row([
                dbc.Col(width=4),
                dbc.Col(
                    [
                    html.Div([
                            html.H5("Tu jamón ha sido detectado con la siguiente composición:"),
                            html.Ul([
                                html.Li(id="serrano"),
                                html.Li(id="cebo"),
                                html.Li(id="bellota"),
                                html.Li(id="otros")
                            ]),

                        ])
                    ],
                width=4),
                dbc.Col(width=4),

            ]),

            dbc.Row([
                dbc.Col(width=2),
                dbc.Col([
                    html.Div([
                            html.H5(id="price-text")
                        ], style={'text-align': 'center', 'margin': 'auto'})
                    ], width=8),
                dbc.Col(width=2),
            ]),

            dbc.Row([
                dbc.Col(width=2),
                dbc.Col([
                    html.Div([
                        dcc.Graph(id="polar-chart"),
                    ])
                ], width=8),
                dbc.Col(width=2)
            ])

        ], id="container-results", hidden=True)

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
    Output("serrano", "children"),
    Output("cebo", "children"),
    Output("bellota", "children"),
    Output("otros", "children"),
    Output("price-text", "children"),

     Output("container-results", "hidden")],
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
        return px.line_polar(), "", "", "", "", "", True
    else:
        feature_names = ["carbohydrates_100g", "energy-kcal_100g", "proteins_100g", "salt_100g", "saturated-fat_100g",
                         "sugars_100g", "insaturated-fat_100g"]

        feature_labels_dict = {
            "carbohydrates_100g": "Carbohidratos",
            "energy-kcal_100g": "KCal",
            "proteins_100g": "Proteinas",
            "salt_100g": "Sal",
            "saturated-fat_100g": "Gasas Saturadas",
            "sugars_100g": "Azúcar",
            "insaturated-fat_100g": "Grasas Insaturadas"
        }

        feature_labels_list = [feature_labels_dict[x] for x in feature_names]

        input_values = np.array([carbohydrates, calories, proteins, salt, saturated_fat, sugar, insaturated_fat])
        input_data = pd.DataFrame([input_values], columns=feature_names)

        scaled_input = scaler.transform(input_data)
        scaled_input = pd.DataFrame(scaled_input, columns=feature_names)

        pred = model.predict(scaled_input)[0]
        most_similar_ham = clusters[clusters['cluster'] == pred][feature_names]
        most_similar_ham_price = round(clusters[clusters['cluster'] == pred]["price_100g"].values[0] * 10, 2)

        percentages_hams = clusters[clusters['cluster'] == pred][["categoria_0.0", "categoria_1.0", "categoria_2.0",
                                                                  "categoria_3.0"]]
        percentages_hams = percentages_hams.rename(columns={
            "categoria_0.0": "Otros",
            "categoria_1.0": "Serrano",
            "categoria_2.0": "De Cebo",
            "categoria_3.0": "De Bellota"
        })

        percentages_hams = percentages_hams.multiply(100).round(0).astype(int)
        percentages_hams["Otros"] = (100 - percentages_hams["Serrano"] - percentages_hams["De Cebo"] -
                                     percentages_hams["De Bellota"])
        percentages_hams = percentages_hams.to_dict(orient='records')[0]

        df = pd.DataFrame(dict(
            values=list(scaled_input.values[0]) + list(most_similar_ham.values[0]),
            variable=feature_labels_list*2,
            jamones=['Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón', 'Tu jamón',
                 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido',
                 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido', 'Tipo de jamón más parecido']))

        fig = px.line_polar(df, r='values', theta='variable', line_close=True, color='jamones')
        fig.update_traces(fill='toself')

        text_price = ""
        if price > most_similar_ham_price:
            text_price = (f"El precio medio de este tipo de jamón es de {most_similar_ham_price} €/Kg, pero tu jamón "
                          f"es de {price} €/Kg. Lo cual hace que se encuentre sobrevalorado, con "
                          f"{round(price - most_similar_ham_price, 2)} €/Kg de diferencia.")
        elif price < most_similar_ham_price:
            text_price = (f"El precio medio de este tipo de jamón es de {most_similar_ham_price} €/Kg, pero tu jamón "
                          f"es de {price} €/Kg. Lo cual hace que se encuentre infravalorado, con "
                          f"{round(most_similar_ham_price - price, 2)} €/Kg de diferencia.")
        else:
            text_price = (f"El precio medio de este tipo de jamón es de {most_similar_ham_price} €/Kg, lo cual "
                          f"coincide con el valor del jamón introducido.")

        return (fig,
                f"Serrano: {percentages_hams['Serrano']}%.",
                f"De Cebo: {percentages_hams['De Cebo']}%.",
                f"De Bellota: {percentages_hams['De Bellota']}%.",
                f"Otros: {percentages_hams['Otros']}%.",
                text_price,
                False)


if __name__ == '__main__':
    app.run_server(debug=True)
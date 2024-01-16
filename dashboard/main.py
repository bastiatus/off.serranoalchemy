import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data = [
    {'carbohydrates_100g': 0.01, 'energy-kcal_100g': 0.17, 'proteins_100g': 0.44, 'salt_100g': 0.08,
     'saturated-fat_100g': 0.17, 'sugars_100g': 0.01, 'insaturated-fat_100g': 0.16, 'price_100g': None, 'categoria': 1},

    {'carbohydrates_100g': 0.00, 'energy-kcal_100g': 0.23, 'proteins_100g': 0.44, 'salt_100g': 0.08,
     'saturated-fat_100g': 0.25, 'sugars_100g': 0.00, 'insaturated-fat_100g': 0.27, 'price_100g': None, 'categoria': 0},

    {'carbohydrates_100g': 0.01, 'energy-kcal_100g': 0.15, 'proteins_100g': 0.44, 'salt_100g': 0.09,
     'saturated-fat_100g': 0.11, 'sugars_100g': 0.01, 'insaturated-fat_100g': 0.12, 'price_100g': 0.03, 'categoria': 1},

    {'carbohydrates_100g': 0.01, 'energy-kcal_100g': 0.23, 'proteins_100g': 0.44, 'salt_100g': 0.09,
     'saturated-fat_100g': 0.26, 'sugars_100g': 0.01, 'insaturated-fat_100g': 0.29, 'price_100g': 0.05, 'categoria': 2},

    {'carbohydrates_100g': 0.00, 'energy-kcal_100g': 0.22, 'proteins_100g': 0.48, 'salt_100g': 0.07,
     'saturated-fat_100g': 0.21, 'sugars_100g': 0.00, 'insaturated-fat_100g': 0.26, 'price_100g': 0.52, 'categoria': 3}
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Clasificación de Jamones Dashboard"),

    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter_3d(data, x='proteins_100g', y='salt_100g', z='carbohydrates_100g', color='categoria',
                             title='Clusters de Jamones')
    ),

    html.Label("Ingresar Macronutrientes del Jamón:"),
    dcc.Input(id='input-proteina', type='number', placeholder='Proteína'),
    dcc.Input(id='input-salt', type='number', placeholder='salt_100g'),
    dcc.Input(id='input-carbohidratos', type='number', placeholder='carbohydrates_100g'),

    html.Div(id='output-prediction', style={'margin-top': 20}),
])

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('input-proteina', 'value'),
     Input('input-salt', 'value'),
     Input('input-carbohidratos', 'value')]
)

def update_scatter_plot(proteina, salt_100g, carbohidratos):

    fig = px.scatter_3d(data, x='proteins_100g', y='salt_100g', z='carbohydrates_100g', color='categoria',
                        title='Clusters de Jamones')
    return fig


@app.callback(
    Output('output-prediction', 'children'),
    [Input('input-proteina', 'value'),
     Input('input-salt', 'value'),
     Input('input-carbohidratos', 'value')]
)
def update_prediction(proteina, salt, carbohidratos):
    prediction = 0
    return f"El jamón ingresado pertenece al cluster: {prediction}"


if __name__ == '__main__':
    app.run_server(debug=True)

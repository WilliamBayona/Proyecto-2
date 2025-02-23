import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar los datos
file_path = 'datos_apartamentos_rent.csv'
df = pd.read_csv(file_path, encoding='cp1252', sep=';')

# Filtrar datos con coordenadas y precio válidos
df = df.dropna(subset=['latitude', 'longitude', 'price', 'state'])

# Obtener lista de estados únicos y agregar la opción "Todos los Estados Unidos"
estados = sorted(df["state"].unique())
estados.insert(0, "Todos los Estados Unidos")

# Inicializar la app Dash
app = dash.Dash(__name__)

# Definir estilos con la fuente Roboto desde Google Fonts
styles = {
    'container': {
        'width': '80%',
        'margin': '0 auto',
         'font-family': 'Source Sans Pro, sans-serif'
    },
    'title': {
        'textAlign': 'center',
        'fontSize': '32px',
        'fontWeight': 'bold',
        'margin-bottom': '20px',
        'font-family': 'Roboto, sans-serif'
    },
    'filter-container': {
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'margin-bottom': '20px'
    },
    'dropdown': {
        'width': '50%',
        'textAlign': 'center',
        'fontSize': '16px',
        'font-family': 'Roboto, sans-serif'
    }
}

# Layout con Google Fonts
app.layout = html.Div(style=styles['container'], children=[
    # Incluir Google Fonts en el layout
    html.Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;700&display=swap"
    ),

    html.H1("Mapa Interactivo de Precios de Alquiler", style=styles['title']),
    
    html.Div(style=styles['filter-container'], children=[
        html.Label("Selecciona un Estado:", style={'fontSize': '18px', 'margin-right': '10px'}),
        dcc.Dropdown(
            id="state-filter",
            options=[{"label": estado, "value": estado} for estado in estados],
            value="Todos los Estados Unidos",
            clearable=False,
            style=styles['dropdown']
        ),
    ]),

    dcc.Graph(id="map-graph", style={'height': '75vh'})
])

# Callback para actualizar el mapa según el estado seleccionado
@app.callback(
    Output("map-graph", "figure"),
    Input("state-filter", "value")
)
def update_map(selected_state):
    if selected_state == "Todos los Estados Unidos":
        filtered_df = df
        zoom_level = 3
    else:
        filtered_df = df[df["state"] == selected_state]
        zoom_level = 5

    fig = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="price",
        size="price",
        hover_name="title",
        hover_data=["cityname", "state", "price", "square_feet", "bedrooms", "bathrooms"],
        color_continuous_scale="Plasma",
        size_max=20,
        zoom=zoom_level,
        mapbox_style="carto-positron"
    )

    return fig

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)

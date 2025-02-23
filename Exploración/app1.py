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
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"])

# Layout con clases CSS
app.layout = html.Div(className="container", children=[
    
    html.H1("Mapa Interactivo de Precios de Alquiler", className="title"),
    
    html.Div(className="filter-container", children=[
        html.Label("Selecciona un Estado:", className="filter-label"),
        dcc.Dropdown(
            id="state-filter",
            options=[{"label": estado, "value": estado} for estado in estados],
            value="Todos los Estados Unidos",
            clearable=False,
            className="dropdown"
        ),
    ]),

    dcc.Graph(id="map-graph", className="map-graph")
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

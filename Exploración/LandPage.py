import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

# Inicializar la aplicación
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "/assets/style.css"])

# Navbar
navbar = dbc.NavbarSimple(
    brand="Inmobiliaria de los Andes",
    brand_href="#",
    color="dark",
    dark=True,
    className="navbar-custom",
    children=[
        dbc.NavItem(dbc.NavLink("Visualización de Apartamentos", href="#")),
        dbc.NavItem(dbc.NavLink("Predictor de Precios", href="#")),
        dbc.NavItem(dbc.NavLink("Analizador de Descripciones", href="#")),
    ],
)

# Contenido principal
content = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("¡Bienvenido al sistema Inmobiliario de La Inmobiliaria de los Andes!", className="title-text mb-4"),
            html.P("Selecciona una opción para continuar", className="subtitle-text"),
            dbc.Button("Visualización de Apartamentos", color="primary", className="custom-button mb-2"),
            dbc.Button("Predictor de Precios", color="primary", className="custom-button mb-2"),
            dbc.Button("Analizador de Descripciones", color="primary", className="custom-button"),
        ], width=5, className="left-section"),
        dbc.Col([
            html.Img(src="/assets/image.png", className="image-container")
        ], width=7),
    ], align="center", className="content-row mt-4"),
])

# Layout final
app.layout = html.Div([
    navbar,
    content
])

if __name__ == "__main__":
    app.run_server(debug=True)

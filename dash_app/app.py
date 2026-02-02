import dash
from dash import html
import dash_bootstrap_components as dbc
from layouts.main_layout import create_layout
from callbacks.navigation import register_navigation_callbacks
from callbacks.player_callbacks import register_player_callbacks

# Inicializar la app Dash con tema bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="NBA Stats Dashboard"
)

# Aplicar el layout
app.layout = create_layout()

# Registrar callbacks de navegación
register_navigation_callbacks(app)

# Registrar callbacks de players
register_player_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
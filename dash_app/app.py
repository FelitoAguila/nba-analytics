import dash
from dash import html
import dash_bootstrap_components as dbc
from layouts.main_layout import create_layout
from callbacks.navigation import register_navigation_callbacks
from callbacks.player_callbacks import register_player_callbacks
from config import settings

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="NBA Stats Dashboard"
)

# Expose the server for deployment
server = app.server

# Apply the main layout
app.layout = create_layout()

# Navigation callbacks
register_navigation_callbacks(app)

# Player-related callbacks
register_player_callbacks(app)

if __name__ == '__main__':
    app.run_server(
        debug=settings.DEBUG,
        port=settings.PORT,
        host='0.0.0.0'  # for Render deployment
    )
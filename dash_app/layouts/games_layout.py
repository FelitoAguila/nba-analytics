from dash import html, dcc
import dash_bootstrap_components as dbc

def create_games_layout():
    return html.Div(className='page-container', children=[ 
        # Encabezado de la página
        html.Div(className='page-header', children=[
            html.Div(className='page-header-content', children=[
                html.H1('GAMES', className='page-title'),
                html.P('Work in progress', className='page-subtitle')
            ])
        ]),
        # Main content

    ])
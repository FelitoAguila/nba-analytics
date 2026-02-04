from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return html.Div([
        # Componente de Location para manejar URLs
        dcc.Location(id='url', refresh=False),
        
        html.Div(className='main-container', children=[
            # Header
            html.Div(className='header', children=[
                html.Div(className='header-content', children=[
                    # Logo y título
                    html.Div(className='logo-section', children=[
                        html.Div(className='nba-logo-container', children=[
                            html.Img(
                                src='https://cdn.nba.com/logos/leagues/logo-nba.svg',
                                className='nba-logo',
                                alt='NBA Logo'
                            )
                        ]),
                        html.Div(className='title-section', children=[
                            html.H1('ANALYTICS', className='main-title'),
                            html.P('Advanced Charts & Insights', className='subtitle')
                        ])
                    ]),
                    
                    # Navegación
                    html.Div(className='nav-container', children=[
                        dcc.Link('Dashboard', id='nav-dashboard', className='nav-item active', href='/'),
                        dcc.Link('Players', id='nav-players', className='nav-item', href='/players'),
                        dcc.Link('Teams', id='nav-teams', className='nav-item', href='/teams'),
                        dcc.Link('Games', id='nav-games', className='nav-item', href='/games'),
                        dcc.Link('Analysis', id='nav-analysis', className='nav-item', href='/analysis'),
                    ])
                ])
            ]),
            
            # Área de contenido
            html.Div(className='content-area', children=[
                html.Div(id='page-content', children=[])
            ])
        ])
    ])
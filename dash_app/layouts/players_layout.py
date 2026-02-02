from dash import html, dcc
import dash_bootstrap_components as dbc

def create_players_layout():
    return html.Div(className='page-container', children=[
        # Modal para el perfil del jugador
        dbc.Modal(
            id='player-modal',
            size='xl',
            is_open=False,
            centered=True,
            className='player-modal',
            children=[
                dbc.ModalHeader(
                    dbc.ModalTitle('Perfil del Jugador', style={'fontFamily': 'Bebas Neue', 'fontSize': '2rem'}),
                    close_button=True
                ),
                dbc.ModalBody(
                    id='player-modal-content',
                    style={'backgroundColor': '#0a0e27', 'color': 'white'}
                )
            ]
        ),
        
        # Encabezado de la página
        html.Div(className='page-header', children=[
            html.Div(className='page-header-content', children=[
                html.H1('PLAYERS', className='page-title'),
                html.P('Explora estadísticas detalladas de todos los jugadores de la NBA', className='page-subtitle')
            ])
        ]),
        
        # Sección de búsqueda y filtros
        html.Div(className='search-section', children=[
            html.Div(className='search-container', children=[
                # Barra de búsqueda principal
                html.Div(className='search-bar-wrapper', children=[
                    html.Div(className='search-icon', children='🔍'),
                    dcc.Input(
                        id='player-search-input',
                        type='text',
                        placeholder='Buscar jugador por nombre...',
                        className='search-input',
                        debounce=True
                    ),
                    html.Div(id='search-clear-btn', className='search-clear', children='✕')
                ]),
                
                # Filtros rápidos
                html.Div(className='quick-filters', children=[
                    html.Div(className='filter-group', children=[
                        html.Label('Posición:', className='filter-label'),
                        dcc.Dropdown(
                            id='position-filter',
                            options=[
                                {'label': 'Todas', 'value': 'all'},
                                {'label': 'Guard (G)', 'value': 'G'},
                                {'label': 'Forward (F)', 'value': 'F'},
                                {'label': 'Center (C)', 'value': 'C'},
                                {'label': 'Guard-Forward (G-F)', 'value': 'G-F'},
                                {'label': 'Forward-Center (F-C)', 'value': 'F-C'},
                            ],
                            value='all',
                            className='filter-dropdown',
                            clearable=False
                        )
                    ]),
                    
                    html.Div(className='filter-group', children=[
                        html.Label('Equipo:', className='filter-label'),
                        dcc.Dropdown(
                            id='team-filter',
                            options=[
                                {'label': 'Todos los equipos', 'value': 'all'},
                                {'label': 'Lakers', 'value': 'LAL'},
                                {'label': 'Warriors', 'value': 'GSW'},
                                {'label': 'Celtics', 'value': 'BOS'},
                                {'label': 'Heat', 'value': 'MIA'},
                                {'label': 'Bucks', 'value': 'MIL'},
                                # Más equipos se pueden agregar aquí
                            ],
                            value='all',
                            className='filter-dropdown',
                            clearable=False
                        )
                    ]),
                    
                    html.Div(className='filter-group', children=[
                        html.Label('Ordenar por:', className='filter-label'),
                        dcc.Dropdown(
                            id='sort-filter',
                            options=[
                                {'label': 'Nombre (A-Z)', 'value': 'name_asc'},
                                {'label': 'Nombre (Z-A)', 'value': 'name_desc'},
                                {'label': 'Puntos (Mayor)', 'value': 'pts_desc'},
                                {'label': 'Asistencias (Mayor)', 'value': 'ast_desc'},
                                {'label': 'Rebotes (Mayor)', 'value': 'reb_desc'},
                            ],
                            value='name_asc',
                            className='filter-dropdown',
                            clearable=False
                        )
                    ])
                ])
            ])
        ]),
        
        # Resultados de búsqueda
        html.Div(className='results-section', children=[
            html.Div(className='results-header', children=[
                html.H3(id='results-count', children='Mostrando todos los jugadores', className='results-title'),
                html.Div(className='view-toggle', children=[
                    html.Button('Grid', id='view-grid-btn', className='view-btn active', n_clicks=0),
                    html.Button('Lista', id='view-list-btn', className='view-btn', n_clicks=0)
                ])
            ]),
            
            # Aquí se mostrarán los jugadores (grid o lista)
            html.Div(id='players-container', className='players-grid', children=[
                # Las cards aparecerán dinámicamente al buscar
            ])
        ])
    ])
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
                    dbc.ModalTitle('Player Profile', style={'fontFamily': 'Bebas Neue', 'fontSize': '2rem'}),
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
                html.P('Explore detailed player statistics and performance metrics.', className='page-subtitle')
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
                        placeholder='Search player by name...',
                        className='search-input',
                        debounce=True
                    ),
                    html.Div(id='search-clear-btn', className='search-clear', children='✕')
                ]),
                
                # Filtros rápidos
                html.Div(className='quick-filters', children=[
                    html.Div(className='filter-group', children=[
                        html.Label('Position:', className='filter-label'),
                        dcc.Dropdown(
                            id='position-filter',
                            options=[
                                {'label': 'All', 'value': 'all'},
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
                        html.Label('Team:', className='filter-label'),
                        dcc.Dropdown(
                            id='team-filter',
                            options=[
                                {'label': 'All teams', 'value': 'all'},
                                {'label': 'Atlanta Hawks', 'value': 'ATL'},
                                {'label': 'Boston Celtics', 'value': 'BOS'},
                                {'label': 'Brooklyn Nets', 'value': 'BKN'},
                                {'label': 'Charlotte Hornets', 'value': 'CHA'},
                                {'label': 'Chicago Bulls', 'value': 'CHI'},
                                {'label': 'Cleveland Cavaliers', 'value': 'CLE'},
                                {'label': 'Dallas Mavericks', 'value': 'DAL'},
                                {'label': 'Denver Nuggets', 'value': 'DEN'},
                                {'label': 'Detroit Pistons', 'value': 'DET'},
                                {'label': 'Golden State Warriors', 'value': 'GSW'},
                                {'label': 'Houston Rockets', 'value': 'HOU'},
                                {'label': 'Indiana Pacers', 'value': 'IND'},
                                {'label': 'Los Angeles Clippers', 'value': 'LAC'},
                                {'label': 'Los Angeles Lakers', 'value': 'LAL'},
                                {'label': 'Memphis Grizzlies', 'value': 'MEM'},
                                {'label': 'Miami Heat', 'value': 'MIA'},
                                {'label': 'Milwaukee Bucks', 'value': 'MIL'},
                                {'label': 'Minnesota Timberwolves', 'value': 'MIN'},
                                {'label': 'New Orleans Pelicans', 'value': 'NOP'},
                                {'label': 'New York Knicks', 'value': 'NYK'},
                                {'label': 'Oklahoma City Thunder', 'value': 'OKC'},
                                {'label': 'Orlando Magic', 'value': 'ORL'},
                                {'label': 'Philadelphia 76ers', 'value': 'PHI'},
                                {'label': 'Phoenix Suns', 'value': 'PHX'},
                                {'label': 'Portland Trail Blazers', 'value': 'POR'},
                                {'label': 'Sacramento Kings', 'value': 'SAC'},
                                {'label': 'San Antonio Spurs', 'value': 'SAS'},
                                {'label': 'Toronto Raptors', 'value': 'TOR'},
                                {'label': 'Utah Jazz', 'value': 'UTA'},
                                {'label': 'Washington Wizards', 'value': 'WAS'},
                            ],
                            value='all',
                            className='filter-dropdown',
                            clearable=False
                        )
                    ]),
                    
                    html.Div(className='filter-group', children=[
                        html.Label('Season:', className='filter-label'),
                        dcc.Dropdown(
                            id='season-filter',
                            options=[
                                {'label': '2025-2026', 'value': '2025_26'},
                                {'label': '2024-2025', 'value': '2024_25'},
                                {'label': '2023-2024', 'value': '2023_24'},
                                {'label': '2022-2023', 'value': '2022_23'},
                                {'label': '2021-2022', 'value': '2021_22'},
                                {'label': '2020-2021', 'value': '2020_21'},
                                {'label': '2019-2020', 'value': '2019_20'},
                                {'label': '2018-2019', 'value': '2018_19'},
                                {'label': '2017-2018', 'value': '2017_18'},
                                {'label': '2016-2017', 'value': '2016_17'},
                                {'label': '2015-2016', 'value': '2015_16'},
                                {'label': '2014-2015', 'value': '2014_15'},
                                {'label': '2013-2014', 'value': '2013_14'},
                                {'label': '2012-2013', 'value': '2012_13'},
                                {'label': '2011-2012', 'value': '2011_12'},
                                {'label': '2010-2011', 'value': '2010_11'},
                                {'label': '2009-2010', 'value': '2009_10'},
                                {'label': '2008-2009', 'value': '2008_09'},
                                {'label': '2007-2008', 'value': '2007_08'},
                                {'label': '2006-2007', 'value': '2006_07'},
                                {'label': '2005-2006', 'value': '2005_06'},
                                {'label': '2004-2005', 'value': '2004_05'},
                                {'label': '2003-2004', 'value': '2003_04'},
                                {'label': '2002-2003', 'value': '2002_03'},
                                {'label': '2001-2002', 'value': '2001_02'},
                                {'label': '2000-2001', 'value': '2000_01'},
                            ],
                            value='2025_26',
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
                html.H3(id='results-count', children='Showing all players', className='results-title'),
            ]),
            
            # Aquí se mostrarán los jugadores (grid o lista)
            html.Div(id='players-container', className='players-grid', children=[
                # Las cards aparecerán dinámicamente al buscar
            ])
        ])
    ])
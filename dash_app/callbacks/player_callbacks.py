from dash import Input, Output, State, html, callback_context, dcc
import dash
from utils.database import BigQueryDB
from config import settings
import plotly.graph_objects as go

# Inicializar conexión a BigQuery
try:
    db = BigQueryDB(
        credentials_path=settings.CREDENTIALS_PATH,
        project_id=settings.PROJECT_ID
    )
except Exception as e:
    print(f"Error inicializando BigQuery: {e}")
    db = None

def register_player_callbacks(app):
    """
    Registra los callbacks para la búsqueda y filtrado de jugadores
    """
    
    @app.callback(
        Output('players-container', 'children'),
        Output('results-count', 'children'),
        [
            Input('player-search-input', 'value'),
            Input('position-filter', 'value'),
            Input('team-filter', 'value'),
            Input('season-filter', 'value')
        ]
    )
    def update_players_list(search_query, position, team, season):
        """
        Actualiza la lista de jugadores según los filtros y búsqueda
        """
        if db is None:
            return [
                html.Div(className='no-results', children=[
                    html.H3('⚠️ Error de Conexión'),
                    html.P('No se pudo conectar a la base de datos. Verifica la configuración.')
                ])
            ], 'Error de conexión'
        
        try:
            # Si hay búsqueda, buscar por nombre
            if search_query and search_query.strip():
                df = db.get_player(
                    search_query.strip(),
                    settings.DATASET_ID,
                    season,
                    team
                )
                results_text = f'Showing {len(df)} results for "{search_query}"'
            else:
                # Si no hay búsqueda, no mostrar nada
                return [], 'Enter player name to search'
            
            # Aplicar filtros adicionales si es necesario
            if not df.empty:
                # Filtro de posición (si la columna existe)
                if position and position != 'all' and 'POSITION' in df.columns:
                    df = df[df['POSITION'] == position]
                
            
            # Si no hay resultados
            if df.empty:
                return [
                    html.Div(className='no-results', children=[
                        html.H3('🔍 No players found'),
                        html.P(f'No players match "{search_query}"')
                    ])
                ], 'No results found'
            
            # Crear cards de jugadores
            player_cards = []
            for _, player in df.iterrows():
                player_cards.append(create_player_card(player))
            
            return player_cards, results_text
            
        except Exception as e:
            print(f"Search Error: {e}")
            return [
                html.Div(className='no-results', children=[
                    html.H3('⚠️ Error'),
                    html.P(f'An error occurred: {str(e)}')
                ])
            ], 'Search Error'
    
    @app.callback(
        Output('player-modal', 'is_open'),
        Output('player-modal-content', 'children'),
        [Input({'type': 'player-profile-btn', 'index': dash.dependencies.ALL}, 'n_clicks')],
        [State('player-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_player_modal(n_clicks_list, is_open):
        """
        Abre/cierra el modal del perfil del jugador y carga los datos
        """
        if not any(n_clicks_list):
            return is_open, []
        
        # Obtener el ID del jugador que fue clickeado
        ctx = callback_context
        if not ctx.triggered:
            return is_open, []
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == '':
            return is_open, []
        
        import json
        button_data = json.loads(button_id)
        player_id = button_data['index']
        
        if db is None:
            return True, html.Div([
                html.H3('Error de conexión', style={'color': 'white', 'textAlign': 'center'})
            ])
        
        try:
            # Obtener datos completos del jugador
            player_df = db.get_player_full_stats(player_id, settings.DATASET_ID, settings.TABLE_ID)
            
            if player_df.empty:
                return True, html.Div([
                    html.H3('Jugador no encontrado', style={'color': 'white', 'textAlign': 'center'})
                ])
            
            player_data = player_df.iloc[0]
            
            # Obtener percentiles
            percentiles = db.get_player_percentiles(player_id, settings.DATASET_ID, settings.TABLE_ID)
            
            if percentiles is None:
                return True, html.Div([
                    html.H3('Error al calcular percentiles', style={'color': 'white', 'textAlign': 'center'})
                ])
            
            # Crear el gráfico de radar
            radar_fig = create_radar_chart(percentiles)
            
            # Construir el contenido del modal
            modal_content = html.Div(className='player-profile-content', children=[
                # Header del perfil
                html.Div(className='profile-header', children=[
                    html.Img(
                        src=f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png",
                        className='profile-image'
                    ),
                    html.Div(className='profile-info', children=[
                        html.H2(player_data['PLAYER'], className='profile-name'),
                        html.P(f"{player_data['TEAM']} | #{player_data.get('RANK', 'N/A')}", className='profile-team'),
                        html.Div(className='profile-stats-summary', children=[
                            html.Div([html.Strong('PPG: '), f"{round(player_data['PTS'], 1)}"]),
                            html.Div([html.Strong('APG: '), f"{round(player_data['AST'], 1)}"]),
                            html.Div([html.Strong('RPG: '), f"{round(player_data['REB'], 1)}"]),
                        ])
                    ])
                ]),
                
                # Sección de percentiles
                html.Div(className='percentiles-section', children=[
                    html.H3('Percentiles de Efectividad', className='section-title'),
                    html.P('Posición del jugador respecto a toda la liga', className='section-subtitle'),
                    
                    # Gráfico de radar
                    dcc.Graph(
                        figure=radar_fig,
                        config={'displayModeBar': False},
                        className='radar-chart'
                    ),
                    
                    # Detalles de percentiles
                    html.Div(className='percentile-details', children=[
                        html.Div(className='percentile-item', children=[
                            html.Div(className='percentile-label', children='Field Goal %'),
                            html.Div(className='percentile-bar-container', children=[
                                html.Div(
                                    className='percentile-bar',
                                    style={'width': f"{percentiles['fg_pct_percentile']}%"}
                                ),
                            ]),
                            html.Div(className='percentile-values', children=[
                                html.Span(f"{percentiles['fg_pct']}%", className='actual-value'),
                                html.Span(f"Percentil {percentiles['fg_pct_percentile']}", className='percentile-value')
                            ])
                        ]),
                        html.Div(className='percentile-item', children=[
                            html.Div(className='percentile-label', children='3-Point %'),
                            html.Div(className='percentile-bar-container', children=[
                                html.Div(
                                    className='percentile-bar',
                                    style={'width': f"{percentiles['fg3_pct_percentile']}%"}
                                ),
                            ]),
                            html.Div(className='percentile-values', children=[
                                html.Span(f"{percentiles['fg3_pct']}%", className='actual-value'),
                                html.Span(f"Percentil {percentiles['fg3_pct_percentile']}", className='percentile-value')
                            ])
                        ]),
                        html.Div(className='percentile-item', children=[
                            html.Div(className='percentile-label', children='Free Throw %'),
                            html.Div(className='percentile-bar-container', children=[
                                html.Div(
                                    className='percentile-bar',
                                    style={'width': f"{percentiles['ft_pct_percentile']}%"}
                                ),
                            ]),
                            html.Div(className='percentile-values', children=[
                                html.Span(f"{percentiles['ft_pct']}%", className='actual-value'),
                                html.Span(f"Percentil {percentiles['ft_pct_percentile']}", className='percentile-value')
                            ])
                        ])
                    ])
                ])
            ])
            
            return True, modal_content
            
        except Exception as e:
            print(f"Error al cargar perfil: {e}")
            return True, html.Div([
                html.H3('Error al cargar perfil', style={'color': 'white', 'textAlign': 'center'}),
                html.P(str(e), style={'color': 'rgba(255,255,255,0.6)', 'textAlign': 'center'})
            ])



def create_player_card(player_data):
    """
    Crea una tarjeta de jugador con datos reales de BigQuery
    
    Args:
        player_data: Serie de pandas con los datos del jugador
        
    Returns:
        Componente Dash html.Div con la card del jugador
    """
    # Extraer datos
    player_id = player_data.get('PLAYER_ID', '')
    player_name = player_data.get('PLAYER', 'Unknown Player')
    team = player_data.get('TEAM', 'N/A')
    
    # Estadísticas
    ppg = round(player_data.get('PTS', 0), 1)
    apg = round(player_data.get('AST', 0), 1)
    rpg = round(player_data.get('REB', 0), 1)
    
    # FG%
    fg_pct = round(player_data.get('FG_PCT', 0) * 100, 1) if player_data.get('FG_PCT') else 0
    
    # Games played
    gp = int(player_data.get('GP', 0))
    
    # Generar URL de imagen
    image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    
    # Determinar posición (si existe en los datos)
    # Como no está en la tabla, usaremos una lógica simple basada en estadísticas
    position = get_position_from_stats(player_data)
    
    # Generar número de jugador (no disponible en los datos, usar ranking)
    rank = player_data.get('RANK', '')
    
    return html.Div(className='player-card', children=[
        html.Div(className='player-card-header', children=[
            html.Div(className='player-number', children=f'#{rank}' if rank else ''),
            html.Div(className='player-position', children=position)
        ]),
        html.Div(className='player-image-container', children=[
            html.Img(
                src=image_url, 
                className='player-image', 
                alt=player_name
            )
        ]),
        html.Div(className='player-info', children=[
            html.H3(player_name, className='player-name'),
            html.P(team, className='player-team'),
            html.P(f'{gp} Partidos Jugados', className='player-games', 
                   style={'fontSize': '0.85rem', 'color': 'rgba(255,255,255,0.5)', 'marginTop': '0.3rem'})
        ]),
        html.Div(className='player-stats-preview', children=[
            html.Div(className='stat-item', children=[
                html.Span('PPG', className='stat-label'),
                html.Span(str(ppg), className='stat-value')
            ]),
            html.Div(className='stat-item', children=[
                html.Span('APG', className='stat-label'),
                html.Span(str(apg), className='stat-value')
            ]),
            html.Div(className='stat-item', children=[
                html.Span('RPG', className='stat-label'),
                html.Span(str(rpg), className='stat-value')
            ]),
            html.Div(className='stat-item', children=[
                html.Span('FG%', className='stat-label'),
                html.Span(f'{fg_pct}%', className='stat-value')
            ])
        ]),
        html.Button('Ver Perfil', className='view-profile-btn', id={'type': 'player-profile-btn', 'index': player_id})
    ])


def get_position_from_stats(player_data):
    """
    Infiere la posición del jugador basándose en sus estadísticas
    Esto es una aproximación ya que no tenemos la posición en los datos
    
    Args:
        player_data: Serie de pandas con los datos del jugador
        
    Returns:
        String con la posición estimada
    """
    ast = player_data.get('AST', 0)
    reb = player_data.get('REB', 0)
    pts = player_data.get('PTS', 0)
    
    # Lógica simple de inferencia
    if ast > 5:  # Muchas asistencias -> Guard
        return 'G'
    elif reb > 8:  # Muchos rebotes -> Center/Forward
        if reb > 10:
            return 'C'
        else:
            return 'F'
    elif pts > 20:  # Muchos puntos -> Forward
        return 'F'
    else:
        return 'G-F'  # Default


def create_radar_chart(percentiles_data):
    """
    Crea un gráfico de radar con los percentiles del jugador
    
    Args:
        percentiles_data: dict con los percentiles del jugador
        
    Returns:
        plotly figure
    """
    categories = ['FG%', '3P%', 'FT%']
    values = [
        percentiles_data['fg_pct_percentile'],
        percentiles_data['fg3_pct_percentile'],
        percentiles_data['ft_pct_percentile']
    ]
    
    # Cerrar el polígono
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(237, 28, 36, 0.3)',
        line=dict(color='rgb(237, 28, 36)', width=3),
        marker=dict(size=10, color='rgb(237, 28, 36)'),
        name='Percentiles'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='rgba(255, 255, 255, 0.8)', size=12),
                ticksuffix='%'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(color='white', size=14, family='Bebas Neue')
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=80, b=80),
        height=400
    )
    
    return fig
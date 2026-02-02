from dash import html

def create_dashboard_layout():
    """
    Layout para la página principal del dashboard
    """
    return html.Div(className='welcome-section', children=[
        html.H2('BIENVENIDO AL FUTURO DE LAS ESTADÍSTICAS NBA', className='welcome-title'),
        html.P(
            'Explora datos en tiempo real, análisis avanzados y visualizaciones interactivas '
            'de tus jugadores y equipos favoritos de la NBA.',
            className='welcome-description'
        ),
        
        # Grid de estadísticas destacadas
        html.Div(className='stats-grid', children=[
            html.Div(className='stat-card', children=[
                html.Div('🏀', className='stat-icon'),
                html.H3('30 EQUIPOS', className='stat-title'),
                html.P('Análisis completo de todas las franquicias de la NBA', className='stat-description')
            ]),
            html.Div(className='stat-card', children=[
                html.Div('⭐', className='stat-icon'),
                html.Div('450+ JUGADORES', className='stat-title'),
                html.P('Estadísticas detalladas de cada atleta activo', className='stat-description')
            ]),
            html.Div(className='stat-card', children=[
                html.Div('📊', className='stat-icon'),
                html.H3('TIEMPO REAL', className='stat-title'),
                html.P('Datos actualizados de partidos y rendimiento', className='stat-description')
            ]),
            html.Div(className='stat-card', children=[
                html.Div('🔥', className='stat-icon'),
                html.H3('ANALYTICS', className='stat-title'),
                html.P('Métricas avanzadas y predicciones basadas en IA', className='stat-description')
            ])
        ])
    ])
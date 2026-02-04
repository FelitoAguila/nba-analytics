from dash import html

def create_dashboard_layout():
    """
    Welcome layout
    Includes a description and cards with key features
    """
    return html.Div(className='welcome-section', children=[
        html.H2('WELCOME TO NBA ANALYTICS', className='welcome-title'),
        html.P(
            'This app provides interactive visualizations and data-driven analysis of NBA player and team performance,  '
            'sourced from real NBA data and updated every morning.',
            className='welcome-description'
        ),
        
        # Grid de estadísticas destacadas
        html.Div(className='stats-grid', children=[
            html.Div(className='stat-card', children=[
                html.H3('30 NBA TEAMS', className='stat-title'),
                html.P('Data on all current teams, including win-loss records and efficiency metrics for team performance analysis.', 
                       className='stat-description')
            ]),
            html.Div(className='stat-card', children=[
                html.Div('450+ ACTIVE PLAYERS', className='stat-title'),
                html.P('Detailed stats for every player, such as points per game, assists, and advanced metrics like PER, to explore individual contributions.', 
                       className='stat-description')
            ]),
            html.Div(className='stat-card', children=[
                html.H3('DAILY UPDATED', className='stat-title'),
                html.P('Integration with public NBA API ensures fresh data for timely analysis of ongoing seasons and player trends.', 
                       className='stat-description')
            ]),
            html.Div(className='stat-card', children=[
                html.H3('ADVANCED ANALYTICS', className='stat-title'),
                html.P('Interactive charts to uncover insights like shooting efficiency, defensive ratings, and predictive trends.', 
                       className='stat-description')
            ])
        ])
    ])
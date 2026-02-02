from dash import Input, Output, html, callback
import dash

def register_navigation_callbacks(app):
    """
    Registra los callbacks para la navegación entre páginas
    """
    
    @app.callback(
        Output('page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        """
        Cambia el contenido de la página según la URL
        """
        if pathname == '/players' or pathname == '/players/':
            from layouts.players_layout import create_players_layout
            return create_players_layout()
        elif pathname == '/teams' or pathname == '/teams/':
            from layouts.teams_layout import create_teams_layout
            return create_teams_layout()
        elif pathname == '/games' or pathname == '/games/':
            from layouts.games_layout import create_games_layout
            return create_games_layout()
        elif pathname == '/analysis' or pathname == '/analysis/':
            from layouts.analysis_layout import create_analysis_layout
            return create_analysis_layout()
        else:  # pathname == '/' or pathname == '/dashboard'
            from layouts.dashboard_layout import create_dashboard_layout
            return create_dashboard_layout()
    
    @app.callback(
        Output('nav-dashboard', 'className'),
        Output('nav-players', 'className'),
        Output('nav-teams', 'className'),
        Output('nav-games', 'className'),
        Output('nav-analysis', 'className'),
        [Input('url', 'pathname')]
    )
    def update_active_nav(pathname):
        """
        Actualiza la clase 'active' del item de navegación según la página actual
        """
        base_class = 'nav-item'
        active_class = 'nav-item active'
        
        if pathname == '/players' or pathname == '/players/':
            return base_class, active_class, base_class, base_class, base_class
        elif pathname == '/teams' or pathname == '/teams/':
            return base_class, base_class, active_class, base_class, base_class
        elif pathname == '/games' or pathname == '/games/':
            return base_class, base_class, base_class, active_class, base_class
        elif pathname == '/analysis' or pathname == '/analysis/':
            return base_class, base_class, base_class, base_class, active_class
        else:  # Dashboard
            return active_class, base_class, base_class, base_class, base_class
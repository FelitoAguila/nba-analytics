import pandas as pd
from nba_api.stats.endpoints import leagueleaders
from pandas_gbq import to_gbq
import functions_framework

@functions_framework.http
def run_nba_update(request):
    try:
        # Tu lógica original
        leaders = leagueleaders.LeagueLeaders(
            season='2025-26',
            season_type_all_star='Regular Season',
            per_mode48='Totals',
            stat_category_abbreviation='PTS',
            scope='S',
            league_id='00'
        )
        
        df = leaders.get_data_frames()[0]
        
        # Carga a BigQuery
        to_gbq(
            dataframe=df,
            destination_table="leagueleaders.season_25_26",
            project_id="nba-stats-485814",
            if_exists="replace"
        )
        return "Tabla actualizada exitosamente", 200
    except Exception as e:
        return f"Error: {str(e)}", 500
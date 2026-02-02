from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

class BigQueryDB:
    """
    Clase para manejar la conexión y consultas a BigQuery
    """
    
    def __init__(self, credentials_path='config/service-account.json', project_id=None):
        """
        Inicializa la conexión a BigQuery
        
        Args:
            credentials_path: Ruta al archivo JSON de credenciales
            project_id: ID del proyecto de GCP (opcional, se toma del JSON si no se provee)
        """
        # Cargar credenciales
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        
        # Obtener project_id del archivo de credenciales si no se provee
        if project_id is None:
            import json
            with open(credentials_path) as f:
                creds_json = json.load(f)
                project_id = creds_json.get('project_id')
        
        # Crear cliente de BigQuery
        self.client = bigquery.Client(
            credentials=self.credentials,
            project=project_id
        )
        
        self.project_id = project_id
    
    def query(self, sql):
        """
        Ejecuta una consulta SQL y retorna un DataFrame de pandas
        
        Args:
            sql: Consulta SQL
            
        Returns:
            pandas.DataFrame con los resultados
        """
        try:
            query_job = self.client.query(sql)
            return query_job.to_dataframe()
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            return pd.DataFrame()
    
    def get_player_by_name(self, player_name, dataset_id, table_id):
        """
        Busca jugadores por nombre (búsqueda parcial)
        
        Args:
            player_name: Nombre del jugador a buscar
            dataset_id: ID del dataset en BigQuery
            table_id: ID de la tabla en BigQuery
            
        Returns:
            pandas.DataFrame con los jugadores encontrados
        """
        sql = f"""
        SELECT *
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        WHERE UPPER(PLAYER) LIKE UPPER('%{player_name}%')
        ORDER BY PTS DESC
        LIMIT 20
        """
        return self.query(sql)
    
    def get_all_players(self, dataset_id, table_id, limit=50):
        """
        Obtiene todos los jugadores (limitado)
        
        Args:
            dataset_id: ID del dataset en BigQuery
            table_id: ID de la tabla en BigQuery
            limit: Número máximo de jugadores a retornar
            
        Returns:
            pandas.DataFrame con los jugadores
        """
        sql = f"""
        SELECT *
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        ORDER BY PTS DESC
        LIMIT {limit}
        """
        return self.query(sql)
    
    def filter_players(self, dataset_id, table_id, position=None, team=None, 
                      sort_by='PTS', sort_order='DESC', limit=50):
        """
        Filtra jugadores según criterios
        
        Args:
            dataset_id: ID del dataset en BigQuery
            table_id: ID de la tabla en BigQuery
            position: Posición del jugador (opcional)
            team: Equipo del jugador (opcional)
            sort_by: Campo por el cual ordenar
            sort_order: ASC o DESC
            limit: Número máximo de jugadores
            
        Returns:
            pandas.DataFrame con los jugadores filtrados
        """
        where_clauses = []
        
        if position and position != 'all':
            where_clauses.append(f"POSITION = '{position}'")
        
        if team and team != 'all':
            where_clauses.append(f"TEAM = '{team}'")
        
        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)
        
        sql = f"""
        SELECT *
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        {where_sql}
        ORDER BY {sort_by} {sort_order}
        LIMIT {limit}
        """
        return self.query(sql)
    
    def get_player_headshot_url(self, player_id):
        """
        Genera la URL de la imagen del jugador desde NBA.com
        
        Args:
            player_id: ID del jugador
            
        Returns:
            URL de la imagen
        """
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    
    def get_player_percentiles(self, player_id, dataset_id, table_id):
        """
        Calcula los percentiles de FG_PCT, FG3_PCT, FT_PCT para un jugador
        
        Args:
            player_id: ID del jugador
            dataset_id: ID del dataset en BigQuery
            table_id: ID de la tabla en BigQuery
            
        Returns:
            dict con los percentiles del jugador
        """
        sql = f"""
        WITH player_stats AS (
            SELECT 
                PLAYER_ID,
                PLAYER,
                FG_PCT,
                FG3_PCT,
                FT_PCT
            FROM `{self.project_id}.{dataset_id}.{table_id}`
            WHERE PLAYER_ID = {player_id}
        ),
        percentiles AS (
            SELECT
                PLAYER_ID,
                PLAYER,
                FG_PCT,
                FG3_PCT,
                FT_PCT,
                PERCENT_RANK() OVER (ORDER BY FG_PCT) * 100 AS FG_PCT_PERCENTILE,
                PERCENT_RANK() OVER (ORDER BY FG3_PCT) * 100 AS FG3_PCT_PERCENTILE,
                PERCENT_RANK() OVER (ORDER BY FT_PCT) * 100 AS FT_PCT_PERCENTILE
            FROM `{self.project_id}.{dataset_id}.{table_id}`
        )
        SELECT *
        FROM percentiles
        WHERE PLAYER_ID = {player_id}
        """
        
        df = self.query(sql)
        
        if df.empty:
            return None
        
        return {
            'player_name': df.iloc[0]['PLAYER'],
            'fg_pct': round(df.iloc[0]['FG_PCT'] * 100, 1) if df.iloc[0]['FG_PCT'] else 0,
            'fg3_pct': round(df.iloc[0]['FG3_PCT'] * 100, 1) if df.iloc[0]['FG3_PCT'] else 0,
            'ft_pct': round(df.iloc[0]['FT_PCT'] * 100, 1) if df.iloc[0]['FT_PCT'] else 0,
            'fg_pct_percentile': round(df.iloc[0]['FG_PCT_PERCENTILE'], 1),
            'fg3_pct_percentile': round(df.iloc[0]['FG3_PCT_PERCENTILE'], 1),
            'ft_pct_percentile': round(df.iloc[0]['FT_PCT_PERCENTILE'], 1)
        }
    
    def get_player_full_stats(self, player_id, dataset_id, table_id):
        """
        Obtiene todas las estadísticas de un jugador específico
        
        Args:
            player_id: ID del jugador
            dataset_id: ID del dataset en BigQuery
            table_id: ID de la tabla en BigQuery
            
        Returns:
            pandas.DataFrame con las estadísticas del jugador
        """
        sql = f"""
        SELECT *
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        WHERE PLAYER_ID = {player_id}
        """
        return self.query(sql)

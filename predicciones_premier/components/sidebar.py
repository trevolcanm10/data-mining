# components/sidebar.py
import streamlit as st
from utils.predictor import PremierLeaguePredictor

def show_sidebar():
    """Sidebar con equipos y configuración"""
    with st.sidebar:
        # Logo
        st.image("https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg", 
                 width=150)
        
        st.title("⚙️ Configuración")
        st.markdown("---")
        
        # Cargar equipos (una sola vez)
        if 'all_teams' not in st.session_state:
            try:
                predictor = PremierLeaguePredictor()
                # Obtener equipos únicos de los datos
                df = predictor.historical_df
                home_teams = df['team_home'].unique()
                away_teams = df['team_away'].unique()
                all_teams = sorted(set(list(home_teams) + list(away_teams)))
                st.session_state.all_teams = all_teams
            except:
                st.session_state.all_teams = [
                    "Manchester City", "Arsenal", "Liverpool", "Chelsea", "Tottenham",
                    "Manchester United", "Newcastle United", "West Ham", "Aston Villa"
                ]
        
        # Mostrar info
        st.subheader(f" Equipos disponibles: {len(st.session_state.all_teams)}")
        st.markdown("---")
        st.info("""
        **Cómo funciona:**
        1. Selecciona 2 equipos
        2. Click en PRE DECIR
        3. IA analiza datos históricos
        4. Recibe predicción + análisis
        
        **Datos usados:**
        - xG (Goles esperados)
        - Deep completions
        - NP-xG (sin penales)
        - Últimos 20 partidos
        """)
        
        # Info de versión
        st.markdown("---")
        st.caption("v1.0 • Python 3.12 • Actualizado hoy")
# components/sidebar.py
"""
Módulo de la barra lateral para la aplicación de predicciones de la Premier League.
Maneja la carga inicial de datos y la interfaz de usuario lateral.
"""
import streamlit as st
from utils.predictor import PremierLeaguePredictor


def show_sidebar():
    """Sidebar con equipos y configuración"""
    with st.sidebar:
        # Logo
        st.image(
            "https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg",
            width=150,
        )

        st.markdown("---")

        # Cargar equipos (una sola vez)
        if "all_teams" not in st.session_state:
            try:
                predictor = PremierLeaguePredictor()
                # Obtener equipos únicos de los datos
                df = predictor.historical_df
                if df is not None and not df.empty:
                    home_teams = df["team_home"].unique()
                    away_teams = df["team_away"].unique()
                    all_teams = sorted(set(list(home_teams) + list(away_teams)))
                    st.session_state.all_teams = all_teams
                else:
                    raise ValueError("La tabla de datos está vacía")
            except (ValueError, AttributeError, KeyError) as e:
                st.warning(f"Cargando equipos por defecto. (Motivo: {e})")
                st.session_state.all_teams = [
                    "Manchester City",
                    "Arsenal",
                    "Liverpool",
                    "Chelsea",
                    "Tottenham",
                    "Manchester United",
                    "Newcastle United",
                    "West Ham",
                    "Aston Villa",
                ]

        # Mostrar info
        st.subheader(f" Equipos disponibles: {len(st.session_state.all_teams)}")
        st.markdown("---")
        st.info(
            """
        **Cómo funciona:**
        1. Selecciona 2 equipos
        2. Click en PREDICCIÓN
        3. IA analiza datos históricos
        4. Recibe predicción + análisis
        
        **Datos usados:**
        - xG (Goles esperados)
        - Deep completions
        - NP-xG (sin penales)
        - Últimos 20 partidos
        """
        )

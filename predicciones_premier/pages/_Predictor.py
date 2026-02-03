# pages/_Predictor.py
import streamlit as st
import pandas as pd
import time

# Importar tu predictor
from utils.predictor import PremierLeaguePredictor
from components.prediction_card import show_prediction_card
from components.ads import show_bet365_ad

# Inicializar predictor (caché con session_state)
if 'predictor' not in st.session_state:
    st.session_state.predictor = PremierLeaguePredictor()

predictor = st.session_state.predictor

# Título de página
st.title("Predicción de Partidos")

# Obtener equipos del sidebar (ya cargados)
if 'all_teams' in st.session_state:
    premier_teams = st.session_state.all_teams
else:
    premier_teams = [
        "Manchester City", "Arsenal", "Liverpool", "Chelsea", "Tottenham",
        "Manchester United", "Newcastle United", "West Ham", "Aston Villa",
        "Brighton", "Brentford", "Crystal Palace", "Everton", "Fulham",
        "Nottingham Forest", "Wolverhampton Wanderers", "Bournemouth"
    ]

# UI para selección
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    home_team = st.selectbox(
        "Equipo Local",
        premier_teams,
        index=0,
        key="predictor_home"
    )

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)

with col3:
    away_team = st.selectbox(
        "Equipo Visitante",
        premier_teams,
        index=1,
        key="predictor_away"
    )

# Botón de predicción
if st.button("PRE DECIR PARTIDO", type="primary", use_container_width=True):
    if home_team == away_team:
        st.error("Selecciona equipos diferentes")
    else:
        with st.spinner("Analizando con IA y datos estadísticos..."):
            # Barra de progreso
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
            
            # Obtener predicción
            prediction = predictor.predict_match(home_team, away_team)
            
            # Análisis Gemini
            gemini_analysis = predictor.get_gemini_analysis(
                home_team, away_team, prediction
            )
        
        # Mostrar resultados
        st.success("¡Predicción completada!")
        
        # Card de predicción
        show_prediction_card(prediction, home_team, away_team)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Local gana", f"{prediction['probabilities']['home']}%")
        with col2:
            st.metric("Empate", f"{prediction['probabilities']['draw']}%")
        with col3:
            st.metric("Visitante gana", f"{prediction['probabilities']['away']}%")
        
        # Gráfico simple
        chart_data = pd.DataFrame({
            'Resultado': ['Local', 'Empate', 'Visitante'],
            'Probabilidad (%)': [
                prediction['probabilities']['home'],
                prediction['probabilities']['draw'],
                prediction['probabilities']['away']
            ]
        })
        
        st.bar_chart(chart_data.set_index('Resultado'))
        
        # Análisis IA
        with st.expander("ANÁLISIS DETALLADO DE IA", expanded=True):
            st.write(gemini_analysis)
            
            # Recomendaciones
            st.markdown("---")
            st.subheader("Recomendaciones de apuesta")
            
            if prediction['prediction'] == 'home' and prediction['confidence'] > 60:
                st.info("""
                **Apuesta sugerida:** Victoria local  
                **Tipo:** 1X2 o Handicap -0.5  
                **Riesgo:** Bajo-Medio
                """)
            else:
                st.info("""
                **Apuesta sugerida:** Doble oportunidad  
                **Tipo:** 1X o X2 (más seguro)  
                **Riesgo:** Bajo
                """)
        
        # Publicidad
        show_bet365_ad()
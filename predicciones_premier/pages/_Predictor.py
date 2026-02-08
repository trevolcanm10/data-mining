# pages/_Predictor.py
import streamlit as st
import pandas as pd
import time


# Importar tu predictor
from config import setup_page
from utils.predictor import PremierLeaguePredictor
from components.prediction_card import show_prediction_card
from components.ads import show_bet365_ad

setup_page()
# Inicializar predictor (caché con session_state)
if "predictor" not in st.session_state:
    st.session_state.predictor = PremierLeaguePredictor()

predictor = st.session_state.predictor

# Título de página
st.title("Predicción de Partidos")

# Obtener equipos del sidebar (ya cargados)
if "all_teams" in st.session_state and len(st.session_state.all_teams) > 1:
    premier_teams = st.session_state.all_teams
else:
    premier_teams = [
        "Manchester City",
        "Arsenal",
        "Liverpool",
        "Chelsea",
        "Tottenham",
        "Manchester United",
        "Newcastle United",
        "West Ham",
        "Aston Villa",
        "Brighton",
        "Brentford",
        "Crystal Palace",
        "Everton",
        "Fulham",
        "Nottingham Forest",
        "Wolverhampton Wanderers",
        "Bournemouth",
    ]

# UI para selección
col1, col2, col3 = st.columns([2, 1, 2])
home_default = st.session_state.get("predict_home", premier_teams[0])
away_default = st.session_state.get("predict_away", premier_teams[1])

with col1:
    st.markdown('<label style="color:#00ff99;font-weight:bold;">Equipo Local</label>', unsafe_allow_html=True)
    home_team = st.selectbox(
        "Equipo Local",
        premier_teams,
        index=premier_teams.index(home_default),
        key="predictor_home",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)

with col3:
    st.markdown('<label style="color:#00ff99;font-weight:bold;">Equipo Visitante</label>', unsafe_allow_html=True)
    away_team = st.selectbox(
        "Equipo Visitante",
        premier_teams,
        index=premier_teams.index(away_default),
        key="predictor_away",
        label_visibility="collapsed"
    )


# Funcion para correr la predicción
def run_prediction(home_team, away_team):

    with st.spinner("Analizando con IA y datos estadísticos..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)

        prediction = predictor.predict_match(home_team, away_team)

        gemini_analysis = predictor.get_gemini_analysis(
            home_team, away_team, prediction
        )

    st.success("¡Predicción completada!")

    show_prediction_card(prediction, home_team, away_team)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<h3 style="color:#00ff99;">Local gana: {prediction["probabilities"]["home"]}%</h3>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<h3 style="color:#ffdd00;">Empate: {prediction["probabilities"]["draw"]}%</h3>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<h3 style="color:#ff5555;">Visitante gana: {prediction["probabilities"]["away"]}%</h3>',
            unsafe_allow_html=True,
        )

    chart_data = pd.DataFrame(
        {
            "Resultado": ["Local", "Empate", "Visitante"],
            "Probabilidad (%)": [
                prediction["probabilities"]["home"],
                prediction["probabilities"]["draw"],
                prediction["probabilities"]["away"],
            ],
        }
    )

    # Orden de los graficos
    chart_data["Resultado"] = pd.Categorical(
        chart_data["Resultado"],
        categories=["Local", "Empate", "Visitante"],
        ordered=True,
    )
    chart_data = chart_data.sort_values("Resultado")
    st.bar_chart(chart_data.set_index("Resultado"))

    with st.expander("ANÁLISIS DETALLADO DE IA", expanded=True):
        st.markdown('<div style="background:rgba(0,255,153,0.1);padding:10px;border-radius:12px;">', unsafe_allow_html=True)
        st.write(gemini_analysis)
        st.markdown('</div>', unsafe_allow_html=True)

    show_bet365_ad()


# Botón de predicción
if "predict_home" in st.session_state and "predict_away" in st.session_state:

    home_team = st.session_state.predict_home
    away_team = st.session_state.predict_away

    st.success(f"Partido cargado automáticamente: {home_team} vs {away_team}")

    # Ejecutar predicción automáticamente
    run_prediction(home_team, away_team)

    # Limpiar para que no se repita siempre
    del st.session_state["predict_home"]
    del st.session_state["predict_away"]
    st.stop()


if st.button("PRE DECIR PARTIDO", type="primary", use_container_width=True):
    if home_team == away_team:
        st.markdown(
            '<div class="st-error" style="color:#ff5555;font-weight:bold;">Selecciona equipos diferentes</div>',
            unsafe_allow_html=True,
        )
    else:
        run_prediction(home_team, away_team)

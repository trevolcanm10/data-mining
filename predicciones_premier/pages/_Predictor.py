# pages/_Predictor.py
import streamlit as st
import pandas as pd
import time

# Importar tu predictor
from utils.predictor import PremierLeaguePredictor
from components.prediction_card import show_prediction_card
from components.ads import show_bet365_ad

# Inicializar predictor (caché con session_state)
if "predictor" not in st.session_state:
    st.session_state.predictor = PremierLeaguePredictor()

predictor = st.session_state.predictor

# Título de página
st.title("Predicción de Partidos")

# Obtener equipos del sidebar (ya cargados)
if "all_teams" in st.session_state:
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
    home_team = st.selectbox(
        "Equipo Local", premier_teams, index=premier_teams.index(home_default), key="predictor_home"
    )

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>VS</h2>", unsafe_allow_html=True)

with col3:
    away_team = st.selectbox(
        "Equipo Visitante",
        premier_teams,
        index=premier_teams.index(away_default),
        key="predictor_away",
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
        st.metric("Local gana", f"{prediction['probabilities']['home']}%")
    with col2:
        st.metric("Empate", f"{prediction['probabilities']['draw']}%")
    with col3:
        st.metric("Visitante gana", f"{prediction['probabilities']['away']}%")

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

    #Orden de los graficos
    chart_data["Resultado"] = pd.Categorical(
        chart_data["Resultado"],
        categories=["Local", "Empate", "Visitante"],
        ordered=True,
    )
    chart_data = chart_data.sort_values("Resultado")
    st.bar_chart(chart_data.set_index("Resultado"))

    with st.expander("ANÁLISIS DETALLADO DE IA", expanded=True):
        st.write(gemini_analysis)

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
        st.error("Selecciona equipos diferentes")
    else:
        run_prediction(home_team, away_team)

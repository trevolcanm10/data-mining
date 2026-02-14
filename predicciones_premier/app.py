"""
Aplicación principal de Predicciones Premier League.
Este módulo carga la interfaz de Streamlit y coordina la lógica de predicción.
"""
import streamlit as st
from components.sidebar import show_sidebar
from components.header import show_header
from components.footer import show_footer
# from components.prediction_card import show_prediction_card
from config import setup_page
# Cargar Font Awesome
# 🔹 TEST TEMPORAL: mostrar si la API Key de Gemini se lee correctamente
st.write("API Key leída:", st.secrets.get("GOOGLE_AI_API_KEY"))
st.markdown(
    '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/'
    'css/all.min.css" rel="stylesheet">',
    unsafe_allow_html=True,
)
# Configurar página
st.set_page_config(
    page_title="Predictor Premier League GRATIS",
    page_icon="⚽",
    layout="wide",
)
# Aplicando CSS Global
setup_page()
# Llamaremos al header
show_header()
# Llamamos al Sidebar
show_sidebar()
st.markdown('<h1><i class="fa-solid fa-trophy"></i> Predictor Premier League</h1>', unsafe_allow_html=True)
st.image(
    "https://cdn.resfu.com/media/img_news/creatividad-del-analisis-del-inicio-de-"
    "la-premier-league-2025-26--besoccer.jpg?size=1000x&lossy=1",
    caption="Análisis profesional de la Premier League",
    use_container_width=True,
)
# Sección: Equipos destacados
st.markdown('<h3><i class="fa-solid fa-fire"></i> Equipos Destacados</h3>', unsafe_allow_html=True)

team_images = {
    "Manchester City": (
        "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/"
        "Manchester_City_FC_badge.svg/1200px-Manchester_City_FC_badge.svg.png"
    ),
    "Arsenal": (
        "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/"
        "Arsenal_FC.svg/1200px-Arsenal_FC.svg.png"
    ),
    "Liverpool": (
        "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/"
        "Liverpool_FC.svg/1200px-Liverpool_FC.svg.png"
    ),
    "Chelsea": (
        "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/"
        "Chelsea_FC.svg/1200px-Chelsea_FC.svg.png"
    ),
}
# Mostrar logos de equipos en grid
for team, img_url in team_images.items():
    st.markdown(
        f"""
    <div class="team-row">
        <img src="{img_url}">
        <span>{team}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )
# Botones de navegación
if st.button("Predictor", use_container_width=True):
    st.switch_page("pages/_Predictor.py")
if st.button("Fixtures", use_container_width=True):
    st.switch_page("pages/_Fixtures.py")

if st.button(" Estadísticas", use_container_width=True):
    st.switch_page("pages/_Stats.py")
st.markdown('<div class="stInfo"><i class="fa-solid fa-lightbulb"></i> <b>Tip:</b> Usa los botones o el menú de Streamlit</div>', unsafe_allow_html=True)
show_footer()

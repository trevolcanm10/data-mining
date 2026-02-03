
import streamlit as st
from components.sidebar import show_sidebar
from components.header import show_header
from config import setup_page
# Configurar página
st.set_page_config(
    page_title="Predictor Premier League GRATIS",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)


#Aplicando CSS Global
setup_page()
#Llamaremos al header
show_header()
#Llamamos al Sidebar
show_sidebar()

st.title("Premier League Predictor")
st.write("Usa el menú lateral para navegar.")

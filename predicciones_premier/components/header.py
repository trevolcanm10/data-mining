# components/header.py
import streamlit as st


def show_header():
    """Mostrar header principal"""
    st.markdown(
        """    
    <div class ="header-container">
        <img src="https://cdn.worldvectorlogo.com/logos/premier-league-1.svg" width="180">
        <p class="sub-header">
            IA + Estadísticas Avanzadas • 100% GRATIS • Sin Registro
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

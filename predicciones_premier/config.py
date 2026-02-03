# config.py - Configuración global
import streamlit as st

def setup_page():
    """Configura CSS global"""
    st.markdown("""
    <style>
        .main-header {
            font-size: 3.2rem;
            color: #FF4B4B;
            text-align: center;
            margin-bottom: 0.5rem;
            font-weight: 800;
        }
        .sub-header {
            text-align: center;
            color: #666;
            margin-bottom: 2.5rem;
            font-size: 1.3rem;
        }
        .stButton > button {
            font-weight: bold;
            font-size: 1.1rem;
        }
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 2px solid #eee;
        }
    </style>
    """, unsafe_allow_html=True)
# config.py - Configuración global
import streamlit as st

def setup_page():
    """Configura CSS global"""
    st.markdown("""
    <style>
        .main-header {
            margin: 0 ;
            font-size: 28px;
        }
        
        img{
            max-width: 100%;
            height: auto;
            opacity : 0.5;
            transition: opacity 0.4s ease;
        }
        
        img:hover{
            opacity: 1;
        }
        
        .logo{
            border-radius: 0%;
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
            
        .team-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .team-row img {
            width: 50px;
            height: 50px;
        }
        .team-row span {
            font-weight: bold;
            font-size: 16px;
        }    
        
        div.stButton > button {
            background-color: #1E90FF;  /* Azul */
            color: white;               /* Texto blanco */
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;         /* Bordes redondeados */
            padding: 10px 0px;
        }
        
        div.stButton > button:hover {
            background-color: #104E8B;  /* Azul oscuro al pasar el mouse */
        }

    </style>
    """, unsafe_allow_html=True)
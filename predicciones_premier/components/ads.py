# components/ads.py
import streamlit as st

def show_bet365_ad():
    """Muestra anuncio de Bet365"""
    st.markdown("---")
    
    html = """
    <div style='
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 6px solid #00AD69;
        margin: 1.5rem 0;
    '>
        <h4 style='color: #333; margin-bottom: 0.8rem;'>¿Listo para apostar con ventaja?</h4>
        <p style='color: #555; margin-bottom: 1rem;'>
            Usa nuestro <strong>bono exclusivo</strong> de €30 en Bet365 y apuesta con tu predicción:
        </p>
        <a href="https://www.bet365.com" target="_blank" style="text-decoration: none;">
            <button style='
                background: linear-gradient(135deg, #00AD69 0%, #007E46 100%);
                color: white;
                padding: 14px 28px;
                border: none;
                border-radius: 10px;
                font-size: 1.1rem;
                font-weight: bold;
                cursor: pointer;
                width: 100%;
                transition: transform 0.2s;
            ' onmouseover="this.style.transform='scale(1.02)'" 
            onmouseout="this.style.transform='scale(1)'">
                OBTENER BONO €30 GRATIS
            </button>
        </a>
        <p style='
            font-size: 0.85rem;
            color: #666;
            margin-top: 0.8rem;
            text-align: center;
        '>
            *Solo nuevos clientes. Apuesta mínima €10. Condiciones aplican.
        </p>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)
# components/prediction_card.py
import streamlit as st


def show_prediction_card(prediction, home_team, away_team):
    """Muestra card bonita con resultado"""

    # Determinar color según confianza
    if prediction["confidence"] > 70:
        bg_color = "linear-gradient(135deg, #00b09b 0%, #96c93d 100%)"
    elif prediction["confidence"] > 50:
        bg_color = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    else:
        bg_color = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"

    # Mapear resultado a texto
    result_text = {
        "home": f" {home_team} GANA",
        "draw": " EMPATE",
        "away": f" {away_team} GANA",
    }

    html = f"""
    <div style='
        background: {bg_color};
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    '>
        <h2 style='color: white; margin-bottom: 1rem;'> PREDICCIÓN FINAL</h2>
        <div style='font-size: 1.8rem; font-weight: bold; margin-bottom: 1rem;'>
            {home_team.upper()} <span style='opacity: 0.8;'>VS</span> {away_team.upper()}
        </div>
        <div style='font-size: 2.2rem; margin: 1rem 0; font-weight: 900;'>
            {result_text[prediction['prediction']]}
        </div>
        <div style='
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            font-size: 1.3rem;
            margin-top: 0.5rem;
        '>
            Confianza: <strong>{prediction['confidence']}%</strong>
        </div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

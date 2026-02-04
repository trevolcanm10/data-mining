# components/footer.py
import streamlit as st


def show_footer():
    """Mostrar footer legal"""
    st.markdown("---")
    st.markdown(
        """
    <div class="footer">
        <p>⚠️ Solo mayores de 18 años. Juego responsable.</p>
        <p>📊 Predicciones basadas en análisis estadístico. No garantizamos aciertos.</p>
        <p>🔒 No almacenamos datos personales. 100% anónimo.</p>
        <p>📧 Contacto: predictorpremier@email.com | 📱 TikTok: @PredictorPremier</p>
        <p>© 2024 Predictor Premier League. Proyecto educativo.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

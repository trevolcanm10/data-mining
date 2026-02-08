# pages/_Fixtures.py
import streamlit as st
import pandas as pd
import time
# Importar tu predictor
from config import setup_page
from datetime import datetime
from utils.predictor import PremierLeaguePredictor
setup_page()
# Título de página
st.title("Próximos Partidos")

# Inicializar predictor
if 'predictor' not in st.session_state:
    st.session_state.predictor = PremierLeaguePredictor()

predictor = st.session_state.predictor

# Filtros
st.markdown("### Filtros")
col1, col2, col3 = st.columns(3)

# Asegurar que all_teams exista antes de usarlo
if "all_teams" not in st.session_state:
    st.session_state.all_teams = []


with col1:
    days_ahead = st.slider("Días a mostrar", 1, 60, 14, help="Muestra partidos hasta X días en el futuro")

with col2:
    show_all = st.checkbox("Mostrar todos", True, help="Mostrar partidos ya programados")

with col3:
    team_filter = st.selectbox(
        "Filtrar por equipo",
        ["Todos"] + st.session_state.all_teams,
        index=0
    )

# Botón para actualizar
if st.button(" Actualizar Partidos", type="secondary"):
    with st.spinner("Buscando partidos próximos..."):
        fixtures_df = predictor.fetch_fixtures(days_ahead=days_ahead)
        st.session_state.fixtures_cache = fixtures_df
        st.success(f"{len(fixtures_df)} partidos encontrados")
        st.rerun()

# Obtener fixtures
if 'fixtures_cache' not in st.session_state:
    with st.spinner("Cargando partidos..."):
        fixtures_df = predictor.fetch_fixtures(days_ahead=days_ahead)
        st.session_state.fixtures_cache = fixtures_df
else:
    fixtures_df = st.session_state.fixtures_cache

# Guardar lista real de equipos
st.session_state.all_teams = sorted(
    set(fixtures_df["home_team"]).union(set(fixtures_df["away_team"]))
)

# Aplicar filtros
if not fixtures_df.empty:
    # Convertir fecha
    fixtures_df["date"] = pd.to_datetime(fixtures_df["date"], errors="coerce")
    fixtures_df = fixtures_df.dropna(subset=["date"])
    # Filtrar solo partidos programados si show_all está desactivado
    if not show_all:
        fixtures_df = fixtures_df[fixtures_df["status"] == "SCHEDULED"]

    # Filtrar por equipo si se seleccionó
    if team_filter != "Todos":
        fixtures_df = fixtures_df[
            (fixtures_df['home_team'].str.contains(team_filter, case=False, na=False)) |
            (fixtures_df['away_team'].str.contains(team_filter, case=False, na=False))
        ]

    # Ordenar por fecha
    fixtures_df = fixtures_df.sort_values('date')

    # Formatear fecha bonita
    fixtures_df['fecha_formateada'] = fixtures_df['date'].dt.strftime('%a %d %b %Y')
    fixtures_df['hora'] = fixtures_df['date'].dt.strftime('%H:%M')

    # Mostrar estadísticas
    st.markdown(f"### {len(fixtures_df)} Partidos Encontrados")

    if len(fixtures_df) > 0:
        # Mostrar como cards
        for idx, row in fixtures_df.iterrows():
            with st.container():
                # Crear card para cada partido
                col1, col2, col3, col4 = st.columns([3, 2, 3, 2])

                with col1:
                    st.markdown(f"**{row['home_team']}**")

                with col2:
                    st.markdown(f"**VS**")
                    st.caption(f"{row['fecha_formateada']}")
                    st.caption(f"{row['hora']}")

                with col3:
                    st.markdown(f"**{row['away_team']}**")

                with col4:
                    # Botón para predecir este partido
                    if st.button(
                        "🔮 Predecir",
                        key=f"predict_{row['home_team']}_{row['away_team']}_{row['date']}",
                        use_container_width=True,
                    ):
                        st.session_state.predict_home = row['home_team']
                        st.session_state.predict_away = row['away_team']
                        st.switch_page("pages/_Predictor.py")

                # Separador
                st.markdown("---")
    else:
        st.warning(f"No hay partidos para {team_filter} en los próximos {days_ahead} días")
else:
    st.error("No se pudieron cargar los partidos. Verifica tu conexión o API key.")

# Sección de partidos destacados
st.markdown("### 🌟 Partidos Destacados")

if not fixtures_df.empty:
    # Seleccionar algunos partidos interesantes
    highlight_matches = fixtures_df.head(5)

    for idx, row in highlight_matches.iterrows():
        with st.expander(f"{row['home_team']} vs {row['away_team']} - {row['fecha_formateada']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**🏠 {row['home_team']}**")
                # Aquí podrías añadir estadísticas del equipo local
                st.caption(" Estadísticas detalladas próximamente...")

            with col2:
                st.markdown(f"**✈️ {row['away_team']}**")
                # Estadísticas visitante
                st.caption(" Estadísticas detalladas próximamente...")

            # Botón para predecir
            if st.button(f"🔮 Predecir este partido", key=f"highlight_{idx}"):
                st.session_state.predict_home = row['home_team']
                st.session_state.predict_away = row['away_team']
                st.switch_page("pages/_Predictor.py")

# Información adicional
st.markdown("")
st.info("""
**ℹ️ Información:**
- Los partidos se actualizan automáticamente cada 24 horas
- Datos proporcionados por Football-Data.org API
- Los horarios están en UTC (GMT+0)
- Para partidos de hoy/tomorrow, se mostrarán cuando estén programados
""")

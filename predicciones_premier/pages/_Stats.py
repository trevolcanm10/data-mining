# pages/_Stats.py
"""
Módulo de estadísticas detalladas de la Premier League.
Presenta análisis visuales, xG y métricas de rendimiento de los equipos.
"""
# ==============================
# 1️⃣ Standard library imports
# ==============================
import datetime
# ==============================
# 2️⃣ Third-party imports
# ==============================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# ==============================
# 3️⃣ Local imports
# ==============================
# Importar tu predictor
from config import (
    setup_page,
    PRIMARY_COLOR,
    TEAM_LOGOS,
)
from utils.predictor import PremierLeaguePredictor
setup_page()
# Título de página
st.title("Estadísticas y Análisis")

# Inicializar predictor
if "predictor" not in st.session_state:
    st.session_state.predictor = PremierLeaguePredictor()

predictor = st.session_state.predictor

# Verificar datos
if predictor.historical_df is None or predictor.historical_df.empty:
    st.error("No hay datos históricos cargados. Verifica el archivo matches.csv")
    st.stop()

df = predictor.historical_df

# Sidebar para filtros
with st.sidebar:
    st.header("🔧 Filtros")

    # Seleccionar equipo
    teams = sorted(set(list(df["team_home"].unique()) + list(df["team_away"].unique())))
    selected_team = st.selectbox("Seleccionar equipo", ["Todos"] + teams)

    # Rango de fechas
    if "date_home" in df.columns:
        df["date_home"] = pd.to_datetime(df["date_home"])
        min_date = df["date_home"].min().date()
        max_date = datetime.date(2026, 12, 31)

        date_range = st.date_input(
            "Rango de fechas",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[
                (df["date_home"].dt.date >= start_date)
                & (df["date_home"].dt.date <= end_date)
            ]

    # Métricas a mostrar
    st.markdown("---")
    st.subheader("📈 Métricas")
    show_xg = st.checkbox("xG (Goles esperados)", True)
    show_deep = st.checkbox("Deep Completions", True)
    show_ppda = st.checkbox("PPDA (Presión)", True)
    show_results = st.checkbox("Resultados", True)

# Pestañas principales
tab1, tab2, tab3, tab4 = st.tabs(
    [" Resumen", " Gráficos", " Ranking", " Análisis"]
)

with tab1:
    st.markdown(
        "<h2 style='color:#00ff99; font-family:'Courier New', monospace;'>Resumen General</h2>",
        unsafe_allow_html=True,
    )
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)

    # Función para renderizar cada tarjeta

    def render_card(title, value, icon_html):
        """
            Renderiza una tarjeta visual en Streamlit con un título, un valor y un ícono.

        Args:
            title (str): Nombre de la métrica mostrada.
            value (str | int | float): Valor principal de la tarjeta.
            icon_html (str): Código HTML del ícono (FontAwesome).
        """
        st.markdown(
            f"""
        <div style="
            border:1px solid #00ff99;
            border-radius:10px;
            padding:15px;
            text-align:center;
            min-height:120px;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
        ">
            <div style="font-size:28px; margin-bottom:8px;">{icon_html}</div>
            <div style="font-size:16px; font-weight:bold; color:#00ff99;">{title}</div>
            <div style="
                font-size:22px;
                font-weight:bold;
                color:white;
                margin-top:5px;
            ">
                {value}
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Iconos Font Awesome (requieren internet)
    fa_calendar = '<i class="fas fa-calendar-alt"></i>'
    fa_ball = '<i class="fas fa-futbol"></i>'
    fa_home = '<i class="fas fa-home"></i>'
    fa_users = '<i class="fas fa-users"></i>'

    # Calcular métricas
    total_matches = len(df)
    if total_matches > 0:
        avg_goals = (df["scored_home"].sum() + df["scored_away"].sum()) / total_matches
        home_wins = len(df[df["result_home"] == "w"])
        home_win_rate = f"{(home_wins / total_matches) * 100:.1f}%"
        btts_matches = len(df[(df["scored_home"] > 0) & (df["scored_away"] > 0)])
        btts_rate = f"{(btts_matches / total_matches) * 100:.1f}%"
    else:
        avg_goals = 0
        home_win_rate = "N/A"
        btts_rate = "N/A"
    # Renderizar tarjetas
    with col1:
        render_card("Partidos Analizados", total_matches, fa_calendar)
    with col2:
        render_card("Goles/Promedio", round(avg_goals, 2), fa_ball)

    with col3:
        render_card("Victorias Local", home_win_rate, fa_home)
    with col4:
        render_card("Ambos Anotan", btts_rate, fa_users)
    # Estadísticas por equipo si se seleccionó
    if selected_team != "Todos":
        st.markdown(
            f"""
        <h3 style="
            display:flex; 
            align-items:center; 
            gap:10px; 
            color:{PRIMARY_COLOR}; 
            font-family:'Courier New', monospace;
        ">
            <i class="fas fa-chart-bar"></i> Estadísticas de {selected_team}
        </h3>
        """,
            unsafe_allow_html=True,
        )

        # Filtrar partidos del equipo
        team_matches = df[
            (df["team_home"] == selected_team) | (df["team_away"] == selected_team)
        ]

        if not team_matches.empty:
            # Calcular métricas
            home_games = team_matches[team_matches["team_home"] == selected_team]
            away_games = team_matches[team_matches["team_away"] == selected_team]

            col1, col2, col3 = st.columns(3)

            with col1:
                wins = len(
                    team_matches[
                        (
                            (team_matches["team_home"] == selected_team)
                            & (team_matches["result_home"] == "w")
                        )
                        | (
                            (team_matches["team_away"] == selected_team)
                            & (team_matches["result_home"] == "l")
                        )
                    ]
                )
                st.markdown(
                    f"""
                        <div style="
                            border:2px solid {PRIMARY_COLOR};
                            border-radius:12px;
                            padding:15px;
                            text-align:center;
                        ">
                            <i class="fas fa-trophy" style="color:{PRIMARY_COLOR}; font-size:1.5rem;"></i>
                            <h4 style="margin:5px 0; color:{PRIMARY_COLOR};">Victorias</h4>
                            <span style="font-size:1.2rem; font-weight:bold; color:white;">{wins}</span>
                        </div>
                        """,
                            unsafe_allow_html=True,
                )

            with col2:
                avg_xg_home = (
                    home_games["xG_home"].mean() if not home_games.empty else 0
                )
                avg_xg_away = (
                    away_games["xG_away"].mean() if not away_games.empty else 0
                )
                avg_xg = np.mean([avg_xg_home, avg_xg_away])
                st.markdown(
                    f"""
                <div style="
                    border:2px solid {PRIMARY_COLOR};
                    border-radius:12px;
                    padding:15px;
                    text-align:center;
                ">
                    <i class="fas fa-bolt" style="color:{PRIMARY_COLOR}; font-size:1.5rem;"></i>
                    <h4 style="margin:5px 0; color:{PRIMARY_COLOR};">xG Promedio</h4>
                    <span style="font-size:1.2rem; font-weight:bold; color:white;">{round(avg_xg,2)}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with col3:
                goals_scored = (
                    home_games["scored_home"].sum() if not home_games.empty else 0
                ) + (away_games["scored_away"].sum() if not away_games.empty else 0)
                st.markdown(
                    f"""
                <div style="
                    border:2px solid {PRIMARY_COLOR};
                    border-radius:12px;
                    padding:15px;
                    text-align:center;
                ">
                    <i class="fas fa-futbol" style="color:{PRIMARY_COLOR}; font-size:1.5rem;"></i>
                    <h4 style="margin:5px 0; color:{PRIMARY_COLOR};">Goles Totales</h4>
                    <span style="font-size:1.2rem; font-weight:bold; color:white;">{goals_scored}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Últimos 5 partidos
            st.subheader("Últimos 5 Partidos")
            recent_matches = team_matches.sort_values(
                "date_home", ascending=False
            ).head(5)

            for _, match in recent_matches.iterrows():
                home_flag = match["team_home"] == selected_team
                opponent = match["team_away"] if home_flag else match["team_home"]
                team_score = match["scored_home"] if home_flag else match["scored_away"]
                opponent_score = match["scored_away"] if home_flag else match["scored_home"]

                # Resultado con colores y texto
                if (home_flag and match["result_home"] == "w") or (not home_flag and match["result_home"] == "l"):
                    result_color = "#00ff99"  # verde neón
                    result_text = "Victoria"
                elif match["result_home"] == "d":
                    result_color = "#ffdd00"  # amarillo
                    result_text = "Empate"
                else:
                    result_color = "#ff5555"  # rojo
                    result_text = "Derrota"

                # Logos con tamaño estándar y glow
                team_logo = TEAM_LOGOS.get(selected_team, "")
                opponent_logo = TEAM_LOGOS.get(opponent, "")
                logo_style = (
                    "width:50px; height:50px; object-fit:contain; border-radius:50%;"
                    "box-shadow:0 0 10px rgba(0,255,153,0.6);"
                )
                opponent_logo_style = logo_style.replace("0,255,153", "255,221,0")  # amarillo glow

                # Tarjeta de partido
                match_html = f"""
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    padding:10px 15px;
                    margin-bottom:12px;
                    background: rgba(0,0,0,0.3);
                    border:2px solid {result_color};
                    border-radius:12px;
                    box-shadow:0 0 12px {result_color};
                ">
                    <div style="text-align:center;">
                        <img src="{team_logo}" style="{logo_style}">
                        <div style="color:#00ff99; font-weight:bold; font-size:0.9rem;">{selected_team}</div>
                    </div>
                    <div style="text-align:center; font-weight:bold; color:{result_color}; font-size:1rem;">
                        {team_score} - {opponent_score}<br>
                        <span style="font-size:0.75rem; color:#fff;">
                            ({match.get('xG_home',0):.1f}-{match.get('xG_away',0):.1f} xG)
                        </span>
                    </div>
                    <div style="text-align:center;">
                        <img src="{opponent_logo}" style="{opponent_logo_style}">
                        <div style="color:#fff; font-weight:bold; font-size:0.9rem;">{opponent}</div>
                    </div>
                    <div style="color:{result_color}; font-weight:bold; font-size:0.9rem;">
                        {result_text}
                    </div>
                </div>
                """
                st.markdown(match_html, unsafe_allow_html=True)


with tab2:
    st.markdown(
        '<h1 style="font-size:24px; background-color:None box-shadown:None color:#F54927;">Gráficos y Visualizaciones</h1>',
        unsafe_allow_html=True,
    )

    # 1. Distribución de resultados
    if show_results:
        st.markdown(
            '<h2 style="font-size:24px; color:#00bcd4;">Distribución de Resultados</h2>',
            unsafe_allow_html=True,
        )

        results = df["result_home"].value_counts()
        result_labels = {
            "w": "Victoria Local",
            "d": "Empate",
            "l": "Victoria Visitante",
        }

        fig = px.pie(
            values=results.values,
            names=[result_labels.get(r, r) for r in results.index],
            title="Resultados de Partidos",
            color_discrete_sequence=["#00ff99", "#ffdd00", "#ff5555"],
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)
        fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05,0.05,0.05])

    # 2. xG por equipo (Top 10)
    if show_xg:
        st.markdown(
            '<h2 style="font-size:24px; color:#00bcd4;">xG por Equipo-Top 10</h2>',
            unsafe_allow_html=True,
        )

        # Calcular xG promedio por equipo como local y visitante
        home_xg = df.groupby("team_home")["xG_home"].mean().reset_index()
        home_xg.columns = ["team", "xg_home"]

        away_xg = df.groupby("team_away")["xG_away"].mean().reset_index()
        away_xg.columns = ["team", "xg_away"]

        # Combinar
        team_xg = pd.merge(home_xg, away_xg, on="team", how="outer").fillna(0)
        team_xg["xg_total"] = (team_xg["xg_home"] + team_xg["xg_away"]) / 2

        # Top 10
        top_10 = team_xg.sort_values("xg_total", ascending=False).head(10)

        fig = px.bar(
            top_10,
            x="team",
            y="xg_total",
            title="xG Promedio por Equipo",
            labels={"team": "Equipo", "xg_total": "xG Promedio"},
            color="xg_total",
            color_continuous_scale="Viridis",
            text_auto=".2f",
        )
        st.plotly_chart(fig, use_container_width=True)
        fig.update_layout(
            title={
                "text": "xG Promedio por Equipo (Top 10)",
                "x": 0.5,
                "xanchor": "center",
            },
            xaxis_tickangle=-45,
            font=dict(size=14),
        )

    # 3. Tendencia temporal
    st.markdown(
        '<h2 style="font-size:24px; color:#00bcd4;">Tendencia de Goles por Mes</h2>',
        unsafe_allow_html=True,
    )

    if "date_home" in df.columns:
        df["month"] = df["date_home"].dt.to_period("M").astype(str)

        monthly_stats = (
            df.groupby("month")
            .agg({"scored_home": "sum", "scored_away": "sum"})
            .reset_index()
        )

        monthly_stats["total_goals"] = (
            monthly_stats["scored_home"] + monthly_stats["scored_away"]
        )

        fig = px.line(
            monthly_stats,
            x="month",
            y="total_goals",
            title="Goles Totales por Mes",
            markers=True,
        )
        st.plotly_chart(fig, use_container_width=True)
        fig.update_traces(
            mode="lines+markers", fill="tozeroy", line=dict(color="#00bcd4", width=3)
        )
        fig.update_layout(xaxis_tickangle=-45, yaxis_title="Total Goles", font=dict(size=14))


with tab3:
    st.markdown(
        '<h1 style="font-size:28px; font-weight:bold; background-color:None color:#F54927;">Ranking de Equipos</h1>',
        unsafe_allow_html=True,
    )
    # Calcular ranking basado en múltiples métricas
    teams_list = teams
    rankings = []
    for team in teams_list:
        # Filtrar partidos del equipo
        team_df = df[(df["team_home"] == team) | (df["team_away"] == team)]

        if len(team_df) > 0:
            # Calcular métricas
            wins = len(
                team_df[
                    ((team_df["team_home"] == team) & (team_df["result_home"] == "w"))
                    | ((team_df["team_away"] == team) & (team_df["result_home"] == "l"))
                ]
            )

            draws = len(
                team_df[
                    ((team_df["team_home"] == team) & (team_df["result_home"] == "d"))
                    | ((team_df["team_away"] == team) & (team_df["result_home"] == "d"))
                ]
            )

            losses = len(team_df) - wins - draws

            # xG promedio
            home_xg = (
                team_df[team_df["team_home"] == team]["xG_home"].mean()
                if not team_df[team_df["team_home"] == team].empty
                else 0
            )
            away_xg = (
                team_df[team_df["team_away"] == team]["xG_away"].mean()
                if not team_df[team_df["team_away"] == team].empty
                else 0
            )
            avg_xg = np.mean([home_xg, away_xg])

            # Puntos (3 por victoria, 1 por empate)
            points = (wins * 3) + draws

            rankings.append(
                {
                    "Equipo": team,
                    "PJ": len(team_df),
                    "V": wins,
                    "E": draws,
                    "D": losses,
                    "Puntos": points,
                    "xG Avg": round(avg_xg, 2),
                    "PG %": round((wins / len(team_df)) * 100, 1),
                }
            )

    # Crear DataFrame y ordenar
    rankings_df = pd.DataFrame(rankings)
    if not rankings_df.empty:
        rankings_df = rankings_df.sort_values("Puntos", ascending=False).reset_index(
            drop=True
        )
        rankings_df.index = rankings_df.index + 1  # Para que empiece en 1

    # Mostrar tabla
    st.dataframe(
        rankings_df,
        use_container_width=True,
        column_config={
            "PG %": st.column_config.ProgressColumn(
                "PG %",
                help="Porcentaje de victorias",
                format="%.1f%%",
                min_value=0,
                max_value=100,
            )
        },
    )

    # Exportar opción
    csv = rankings_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar Ranking CSV",
        data=csv,
        file_name="ranking_premier_league.csv",
        mime="text/csv",
    )

with tab4:
    st.header("Análisis Avanzado")

    st.subheader(" Correlaciones entre Métricas")

    # Seleccionar métricas para análisis
    metrics_options = [
        "xG_home",
        "xGA_home",
        "deep_home",
        "npxG_home",
        "scored_home",
        "ppda_home",
        "ppda_allowed_home",
    ]

    selected_x = st.selectbox("Variable X", metrics_options, index=0)
    selected_y = st.selectbox("Variable Y", metrics_options, index=1)

    if selected_x in df.columns and selected_y in df.columns:
        # Filtrar valores válidos
        valid_data = df[[selected_x, selected_y]].copy()

        def to_float(series_or_df):
            # Si accidentalmente es DataFrame de 1 columna, extraer la Serie
            if isinstance(series_or_df, pd.DataFrame):
                series_or_df = series_or_df.iloc[:, 0]
            # Convertir a numérico, NaN si no se puede
            return pd.to_numeric(series_or_df, errors="coerce")

        # Convertir columnas a float
        series_x = to_float(valid_data[selected_x])
        series_y = to_float(valid_data[selected_y])
        
        # Eliminar filas donde haya NaN en cualquiera de las dos Series
        mask = series_x.notna() & series_y.notna()
        series_x = series_x[mask]
        series_y = series_y[mask]

        if series_x.empty or series_y.empty:
            st.warning("No hay datos suficientes para calcular correlación.")
        elif len(series_x) <= 10:
            st.info("Se requieren más de 10 registros para mostrar la correlación.")
        else:
            # Calcular correlación seguro
            correlation = series_x.corr(series_y)
            st.write(
                f"Correlación entre {selected_x} y {selected_y}: **{correlation:.3f}**"
            )
            col1, col2 = st.columns([2, 1])
            with col1:
                # Scatter plot
                fig = px.scatter(
                    x=series_x,
                    y=series_y,
                    trendline="ols",
                    title=f"Correlación: {correlation:.2f}",
                    labels={ "x": selected_x, "y": selected_y },
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.metric("Coeficiente Correlación", f"{correlation:.3f}")

                if correlation > 0.7:
                    st.success("Fuerte correlación positiva")
                elif correlation < -0.7:
                    st.success("Fuerte correlación negativa")
                elif abs(correlation) > 0.3:
                    st.info("Correlación moderada")
                else:
                    st.warning("Correlación débil")

        # Análisis de outliers
        st.subheader("Valores Atípicos (Outliers)")

        metric_for_outliers = st.selectbox(
            "Métrica para análisis", metrics_options, index=2
        )

        if metric_for_outliers in df.columns:
            # Calcular estadísticas
            mean_val = df[metric_for_outliers].mean()
            std_val = df[metric_for_outliers].std()

            # Identificar outliers (3 desviaciones estándar)
            outliers = df[abs(df[metric_for_outliers] - mean_val) > (3 * std_val)]

            st.write(f"**{len(outliers)} valores atípicos encontrados**")

            if not outliers.empty:
                st.dataframe(
                    outliers[["team_home", "team_away", metric_for_outliers]].head(10)
                )

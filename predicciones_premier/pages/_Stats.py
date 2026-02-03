# pages/_Stats.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Importar tu predictor
from utils.predictor import PremierLeaguePredictor

# Título de página
st.title("📊 Estadísticas y Análisis")

# Inicializar predictor
if 'predictor' not in st.session_state:
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
    teams = sorted(set(list(df['team_home'].unique()) + list(df['team_away'].unique())))
    selected_team = st.selectbox("Seleccionar equipo", ["Todos"] + teams)
    
    # Rango de fechas
    if 'date_home' in df.columns:
        df['date_home'] = pd.to_datetime(df['date_home'])
        min_date = df['date_home'].min().date()
        max_date = df['date_home'].max().date()
        
        date_range = st.date_input(
            "Rango de fechas",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df['date_home'].dt.date >= start_date) & 
                   (df['date_home'].dt.date <= end_date)]
    
    # Métricas a mostrar
    st.markdown("---")
    st.subheader("📈 Métricas")
    show_xg = st.checkbox("xG (Goles esperados)", True)
    show_deep = st.checkbox("Deep Completions", True)
    show_ppda = st.checkbox("PPDA (Presión)", True)
    show_results = st.checkbox("Resultados", True)

# Pestañas principales
tab1, tab2, tab3, tab4 = st.tabs(["📋 Resumen", "📈 Gráficos", "🏆 Ranking", "🔍 Análisis"])

with tab1:
    st.header("Resumen General")
    
    # Métricas generales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_matches = len(df)
        st.metric("Partidos Analizados", total_matches)
    
    with col2:
        avg_goals = (df['scored_home'].sum() + df['scored_away'].sum()) / total_matches
        st.metric("Goles/Promedio", round(avg_goals, 2))
    
    with col3:
        home_wins = len(df[df['result_home'] == 'w'])
        home_win_rate = (home_wins / total_matches) * 100
        st.metric("Victorias Local", f"{home_win_rate:.1f}%")
    
    with col4:
        btts_matches = len(df[(df['scored_home'] > 0) & (df['scored_away'] > 0)])
        btts_rate = (btts_matches / total_matches) * 100
        st.metric("Ambos Anotan", f"{btts_rate:.1f}%")
    
    # Estadísticas por equipo si se seleccionó
    if selected_team != "Todos":
        st.subheader(f"Estadísticas de {selected_team}")
        
        # Filtrar partidos del equipo
        team_matches = df[(df['team_home'] == selected_team) | (df['team_away'] == selected_team)]
        
        if not team_matches.empty:
            # Calcular métricas
            home_games = team_matches[team_matches['team_home'] == selected_team]
            away_games = team_matches[team_matches['team_away'] == selected_team]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                wins = len(team_matches[
                    ((team_matches['team_home'] == selected_team) & (team_matches['result_home'] == 'w')) |
                    ((team_matches['team_away'] == selected_team) & (team_matches['result_home'] == 'l'))
                ])
                st.metric("Victorias", wins)
            
            with col2:
                avg_xg_home = home_games['xG_home'].mean() if not home_games.empty else 0
                avg_xg_away = away_games['xG_away'].mean() if not away_games.empty else 0
                avg_xg = np.mean([avg_xg_home, avg_xg_away])
                st.metric("xG Promedio", round(avg_xg, 2))
            
            with col3:
                goals_scored = (home_games['scored_home'].sum() if not home_games.empty else 0) + \
                              (away_games['scored_away'].sum() if not away_games.empty else 0)
                st.metric("Goles Totales", goals_scored)
            
            # Últimos 5 partidos
            st.subheader("Últimos 5 Partidos")
            recent_matches = team_matches.sort_values('date_home', ascending=False).head(5)
            
            for _, match in recent_matches.iterrows():
                if match['team_home'] == selected_team:
                    result = "✅" if match['result_home'] == 'w' else "❌" if match['result_home'] == 'l' else "➖"
                    opponent = match['team_away']
                    score = f"{match['scored_home']}-{match['scored_away']}"
                else:
                    result = "✅" if match['result_home'] == 'l' else "❌" if match['result_home'] == 'w' else "➖"
                    opponent = match['team_home']
                    score = f"{match['scored_away']}-{match['scored_home']}"
                
                st.write(f"{result} vs {opponent}: {score} (xG: {match.get('xG_home', 0):.1f}-{match.get('xG_away', 0):.1f})")

with tab2:
    st.header("Gráficos y Visualizaciones")
    
    # 1. Distribución de resultados
    if show_results:
        st.subheader("Distribución de Resultados")
        
        results = df['result_home'].value_counts()
        result_labels = {'w': 'Victoria Local', 'd': 'Empate', 'l': 'Victoria Visitante'}
        
        fig = px.pie(
            values=results.values,
            names=[result_labels.get(r, r) for r in results.index],
            title="Resultados de Partidos",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 2. xG por equipo (Top 10)
    if show_xg:
        st.subheader("xG por Equipo (Top 10)")
        
        # Calcular xG promedio por equipo como local y visitante
        home_xg = df.groupby('team_home')['xG_home'].mean().reset_index()
        home_xg.columns = ['team', 'xg_home']
        
        away_xg = df.groupby('team_away')['xG_away'].mean().reset_index()
        away_xg.columns = ['team', 'xg_away']
        
        # Combinar
        team_xg = pd.merge(home_xg, away_xg, on='team', how='outer').fillna(0)
        team_xg['xg_total'] = (team_xg['xg_home'] + team_xg['xg_away']) / 2
        
        # Top 10
        top_10 = team_xg.sort_values('xg_total', ascending=False).head(10)
        
        fig = px.bar(
            top_10,
            x='team',
            y='xg_total',
            title="xG Promedio por Equipo",
            labels={'team': 'Equipo', 'xg_total': 'xG Promedio'},
            color='xg_total',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 3. Tendencia temporal
    st.subheader("Tendencia de Goles por Mes")
    
    if 'date_home' in df.columns:
        df['month'] = df['date_home'].dt.to_period('M').astype(str)
        
        monthly_stats = df.groupby('month').agg({
            'scored_home': 'sum',
            'scored_away': 'sum'
        }).reset_index()
        
        monthly_stats['total_goals'] = monthly_stats['scored_home'] + monthly_stats['scored_away']
        
        fig = px.line(
            monthly_stats,
            x='month',
            y='total_goals',
            title="Goles Totales por Mes",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("Ranking de Equipos")
    
    # Calcular ranking basado en múltiples métricas
    teams_list = teams
    
    rankings = []
    for team in teams_list:
        # Filtrar partidos del equipo
        team_df = df[(df['team_home'] == team) | (df['team_away'] == team)]
        
        if len(team_df) > 0:
            # Calcular métricas
            wins = len(team_df[
                ((team_df['team_home'] == team) & (team_df['result_home'] == 'w')) |
                ((team_df['team_away'] == team) & (team_df['result_home'] == 'l'))
            ])
            
            draws = len(team_df[
                ((team_df['team_home'] == team) & (team_df['result_home'] == 'd')) |
                ((team_df['team_away'] == team) & (team_df['result_home'] == 'd'))
            ])
            
            losses = len(team_df) - wins - draws
            
            # xG promedio
            home_xg = team_df[team_df['team_home'] == team]['xG_home'].mean() if not team_df[team_df['team_home'] == team].empty else 0
            away_xg = team_df[team_df['team_away'] == team]['xG_away'].mean() if not team_df[team_df['team_away'] == team].empty else 0
            avg_xg = np.mean([home_xg, away_xg])
            
            # Puntos (3 por victoria, 1 por empate)
            points = (wins * 3) + draws
            
            rankings.append({
                'Equipo': team,
                'PJ': len(team_df),
                'V': wins,
                'E': draws,
                'D': losses,
                'Puntos': points,
                'xG Avg': round(avg_xg, 2),
                'PG %': round((wins / len(team_df)) * 100, 1)
            })
    
    # Crear DataFrame y ordenar
    rankings_df = pd.DataFrame(rankings)
    rankings_df = rankings_df.sort_values('Puntos', ascending=False).reset_index(drop=True)
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
        }
    )
    
    # Exportar opción
    csv = rankings_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Ranking CSV",
        data=csv,
        file_name="ranking_premier_league.csv",
        mime="text/csv"
    )

with tab4:
    st.header("Análisis Avanzado")
    
    st.subheader(" Correlaciones entre Métricas")
    
    # Seleccionar métricas para análisis
    metrics_options = ['xG_home', 'xGA_home', 'deep_home', 'npxG_home', 
                      'scored_home', 'ppda_home', 'ppda_allowed_home']
    
    selected_x = st.selectbox("Variable X", metrics_options, index=0)
    selected_y = st.selectbox("Variable Y", metrics_options, index=1)
    
    if selected_x in df.columns and selected_y in df.columns:
        # Filtrar valores válidos
        valid_data = df[[selected_x, selected_y]].dropna()
        
        if len(valid_data) > 10:
            # Calcular correlación
            correlation = valid_data[selected_x].corr(valid_data[selected_y])
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Scatter plot
                fig = px.scatter(
                    valid_data,
                    x=selected_x,
                    y=selected_y,
                    trendline="ols",
                    title=f"Correlación: {correlation:.2f}",
                    labels={selected_x: selected_x, selected_y: selected_y}
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
        
        metric_for_outliers = st.selectbox("Métrica para análisis", metrics_options, index=2)
        
        if metric_for_outliers in df.columns:
            # Calcular estadísticas
            mean_val = df[metric_for_outliers].mean()
            std_val = df[metric_for_outliers].std()
            
            # Identificar outliers (3 desviaciones estándar)
            outliers = df[abs(df[metric_for_outliers] - mean_val) > (3 * std_val)]
            
            st.write(f"**{len(outliers)} valores atípicos encontrados**")
            
            if not outliers.empty:
                st.dataframe(outliers[['team_home', 'team_away', metric_for_outliers]].head(10))

# Información final
st.markdown("---")
st.info("""
**Acerca de las métricas:**
- **xG (Expected Goals):** Probabilidad de que un tiro resulte gol
- **npxG (Non-Penalty xG):** xG excluyendo penales
- **Deep Completions:** Pases completados cerca del área rival
- **PPDA:** Pases permitidos por acción defensiva (mide presión)
- **xGA:** Goles esperados en contra
""")
"""
Módulo de predicción y análisis de la Premier League.
Contiene la lógica de cálculo de probabilidades, integración con la API de IA
y gestión de datos históricos mediante tablas.
"""
# Lógica de predicción
from datetime import datetime, timedelta
import warnings
import os
import pandas as pd
import numpy as np
import ast
import pickle
import requests
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV


# from sklearn.linear_model import LogisticRegression

warnings.filterwarnings("ignore")


class PremierLeaguePredictor:
    """
    Clase encargada de gestionar los datos históricos, calcular probabilidades
    de victoria y generar análisis predictivos para los partidos de la Premier League.
    """
    def __init__(self):
        self.fixtures_df = None
        self.historical_df = None
        self.team_stats_home = None
        self.team_stats_away = None
        self.le = None
        self.model = None
        self.features = []
        self.team_mapping = self._load_team_mapping()

        self.load_historical_data()
        self.build_team_stats(n_last=10)
        self.train_model()

        # ---------- CACHE DE GEMINI ----------
        self.cache_file = "data/historical_cache.pkl"
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "rb") as f:
                    self.gemini_cache = pickle.load(f)
            except:
                print("Cache corrupto, reiniciando...")
                self.gemini_cache = {}
        else:
            self.gemini_cache = {}

    def save_cache(self):
        with open(self.cache_file, "wb") as f:
            pickle.dump(self.gemini_cache, f)

    def _load_team_mapping(self):
        "Mapeo de nombres API vs Understat"
        return {
            "Brighton & Hove Albion FC": "Brighton",
            "Crystal Palace FC": "Crystal Palace",
            "Leeds United FC": "Leeds",
            "Leicester City FC": "Leicester City",
            "Liverpool FC": "Liverpool",
            "Manchester City FC": "Manchester City",
            "Manchester United FC": "Manchester United",
            "Newcastle United FC": "Newcastle United",
            "Nottingham Forest FC": "Nottingham Forest",
            "Tottenham Hotspur FC": "Tottenham",
            "West Ham United FC": "West Ham",
            "Wolverhampton Wanderers FC": "Wolverhampton Wanderers",
            "AFC Bournemouth": "Bournemouth",
            "Aston Villa FC": "Aston Villa",
            "Burnley FC": "Burnley",
            "Chelsea FC": "Chelsea",
            "Everton FC": "Everton",
            "Fulham FC": "Fulham",
            "Sunderland AFC": "Sunderland",
            "Brentford FC": "Brentford",
            "Arsenal FC": "Arsenal",
            "Manchester United": "Manchester United",  # por si acaso
            "Manchester City": "Manchester City",
            "Arsenal": "Arsenal",
            "Liverpool": "Liverpool",
            "Chelsea": "Chelsea",
            "Tottenham Hotspur": "Tottenham",
            "Newcastle United": "Newcastle United",
            "West Ham United": "West Ham",
            "Aston Villa": "Aston Villa",
            "Brighton": "Brighton",
            "Brentford": "Brentford",
            "Crystal Palace": "Crystal Palace",
            "Everton": "Everton",
            "Fulham": "Fulham",
            "Nottingham Forest": "Nottingham Forest",
            "Wolverhampton Wanderers": "Wolverhampton Wanderers",
            "Bournemouth": "Bournemouth",
            "Leeds": "Leeds",
            "Leicester City": "Leicester City",
            "Southampton": "Southampton",
            "Burnley": "Burnley",
            "Sheffield United": "Sheffield United",
            "Luton Town": "Luton Town",
        }

    def load_historical_data(self, path=None):
        #  Directorio donde está predictor.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        #  Ruta real al dataset dentro del proyecto
        dataset_path = os.path.join(
            base_dir, "..", "data", "matches.csv"
        )
        dataset_path = os.path.abspath(dataset_path)

        #  Leer dataset
        self.historical_df = pd.read_csv(dataset_path)

    def build_team_stats(self, n_last=10):
        """
        Procesa los datos históricos para calcular y consolidar las
        métricas de rendimiento por equipo.
        """
        df = self.historical_df.copy()

        # Asegurar que la fecha sea datetime
        df["date_home"] = pd.to_datetime(df["date_home"], errors="coerce")

        # Ordenar por fecha (más antiguos → más recientes)
        df = df.sort_values("date_home")

        # ===============================
        # ÚLTIMOS N PARTIDOS COMO LOCAL
        # ===============================
        df_home_recent = df.groupby("team_home").tail(n_last)

        self.team_stats_home = df_home_recent.groupby("team_home").agg(
            {
                "xG_home": "mean",
                "deep_home": "mean",
                "npxG_home": "mean",
                "npxGA_home": "mean",
                "xGA_home": "mean",
                "deep_allowed_home": "mean",
                "pts_home": "mean",
                "xpts_home": "mean",
            }
        )

        # ===============================
        # ÚLTIMOS N PARTIDOS COMO VISITANTE
        # ===============================
        df_away_recent = df.groupby("team_away").tail(n_last)

        self.team_stats_away = df_away_recent.groupby("team_away").agg(
            {
                "xG_away": "mean",
                "deep_away": "mean",
                "npxG_away": "mean",
                "npxGA_away": "mean",
                "xGA_away": "mean",
                "deep_allowed_away": "mean",
                "pts_away": "mean",
            }
        )

    def fetch_fixtures(self, days_ahead=30):
        "Obtener partidos futuros"
        # from dotenv import load_dotenv
        # load_dotenv()
        import os
        import requests
        # 1️⃣ Intento usar Streamlit secrets si estamos en Streamlit
        API_KEY = None
        try:
            import streamlit as st
            try:
                API_KEY = st.secrets.get("FOOTBALL_DATA_API_KEY", None)
            except st.errors.StreamlitSecretNotFoundError:
                API_KEY = None
        except ModuleNotFoundError:
            API_KEY = None
        # 2️⃣ Si no está, intento variable de entorno local (con dotenv)
        if API_KEY is None:
            try:
                from dotenv import load_dotenv
                load_dotenv()  # Carga .env si existe
            except ImportError:
                pass
            API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", None)
        # 3️⃣ Error claro si no hay ninguna clave
        if API_KEY is None:
            raise ValueError(
                "No se encontró FOOTBALL_DATA_API_KEY ni en Streamlit secrets ni en variable de entorno local."
            )

        url = "https://api.football-data.org/v4/competitions/PL/matches"
        headers = {"X-Auth-Token": API_KEY}

        # Fechas dinámicas
        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")

        params = {"dateFrom": date_from, "dateTo": date_to}

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            data = response.json()

            fixtures = []

            for match in data.get("matches", []):
                fixtures.append(
                    {
                        "date": match["utcDate"],
                        "home_team": match["homeTeam"]["name"],
                        "away_team": match["awayTeam"]["name"],
                        "status": match["status"],
                        "matchday": match.get("matchday", 0),
                    }
                )

            self.fixtures_df = pd.DataFrame(fixtures)
            # Aplicación de mapeo
            self.fixtures_df["home_team"] = (
                self.fixtures_df["home_team"]
                .map(self.team_mapping)
                .fillna(self.fixtures_df["home_team"])
            )
            self.fixtures_df["away_team"] = (
                self.fixtures_df["away_team"]
                .map(self.team_mapping)
                .fillna(self.fixtures_df["away_team"])
            )

            return self.fixtures_df

        except (requests.exceptions.RequestException, KeyError, ValueError) as e:

            print(f"Error fetching fixtures: {e}")
            # Datos de ejemplo si falla
            return pd.DataFrame(
                {
                    "home_team": ["Manchester City", "Arsenal", "Liverpool"],
                    "away_team": ["Chelsea", "Tottenham", "Manchester United"],
                    "date": [datetime.now().strftime("%Y-%m-%d")] * 3,
                }
            )

    def parse_ppda(self, x):
        """
        Convierte valores tipo "{'att': 247, 'def': 20}"
        en un número real PPDA = att/def
        """
        try:
            d = ast.literal_eval(str(x))  # convierte texto → dict real
            return d["att"] / d["def"]
        except:
            return np.nan

    def prepare_features(self, home_team, away_team):
        """
        Extrae y organiza las métricas estadísticas de ambos equipos para
        generar el vector de características necesario para la predicción.
        """

        if home_team not in self.team_stats_home.index:
            raise ValueError(f"Equipo local sin datos: {home_team}")

        if away_team not in self.team_stats_away.index:
            raise ValueError(f"Equipo visitante sin datos:{away_team}")

        df = self.historical_df

        # Últimos partidos del local en casa
        home_games = df[df["team_home"] == home_team].tail(5)
        # Últimos partidos del visitante fuera
        away_games = df[df["team_away"] == away_team].tail(5)

        # ===============================
        # PROMEDIOS REALES
        # ===============================
        scored_home = home_games["scored_home"].mean()
        missed_home = home_games["missed_home"].mean()

        scored_away = away_games["scored_away"].mean()
        missed_away = away_games["missed_away"].mean()

        wins_home = home_games["wins_home"].mean()
        wins_away = away_games["wins_away"].mean()

        loses_home = home_games["loses_home"].mean()
        loses_away = away_games["loses_away"].mean()

        draws_home = home_games["draws_home"].mean()
        draws_away = away_games["draws_away"].mean()

        ppda_allowed_home = home_games["ppda_allowed_home"].apply(self.parse_ppda).mean()
        ppda_allowed_away = away_games["ppda_allowed_away"].apply(self.parse_ppda).mean()
        ppda_home = home_games["ppda_home"].apply(self.parse_ppda).mean()
        ppda_away = away_games["ppda_away"].apply(self.parse_ppda).mean()

        # ===============================
        # BASE xG
        # ===============================
        xG_home = home_games["xG_home"].mean()
        xGA_home = home_games["xGA_home"].mean()

        xG_away = away_games["xG_away"].mean()
        xGA_away = away_games["xGA_away"].mean()

        # ===============================
        # FEATURES DIFERENCIALES
        # ===============================
        goal_diff = scored_home - scored_away
        goals_total = scored_home + scored_away
        form_home = home_games["pts_home"].mean()
        form_away = away_games["pts_away"].mean()
        form_diff = form_home - form_away
        draw_rate = (draws_home + draws_away) / 2

        ppda_diff = ppda_home - ppda_away

        league_avg_ppda = df["ppda_home"].apply(self.parse_ppda).mean()
        league_avg_scored = df["scored_home"].mean()
        league_avg_missed = df["missed_home"].mean()

        if np.isnan(ppda_home):
            ppda_home = league_avg_ppda
        if np.isnan(ppda_away):
            ppda_away = league_avg_ppda
        if np.isnan(scored_home):
            scored_home = league_avg_scored
        if np.isnan(missed_home):
            missed_home = league_avg_missed

        if np.isnan(scored_away):
            scored_away = league_avg_scored
        if np.isnan(missed_away):
            missed_away = league_avg_missed

        attack_strength_home = scored_home - missed_home
        attack_strength_away = scored_away - missed_away

        # ===============================
        # FEATURE VECTOR FINAL
        # ===============================
        features = {
            "xG_home": xG_home,
            "xGA_home": xGA_home,
            "xG_away": xG_away,
            "xGA_away": xGA_away,
            "scored_home": scored_home,
            "scored_away": scored_away,
            "missed_home": missed_home,
            "missed_away": missed_away,
            "wins_home": wins_home,
            "wins_away": wins_away,
            "draws_home": draws_home,
            "draws_away": draws_away,
            "loses_home": loses_home,
            "loses_away": loses_away,
            "pts_home": home_games["pts_home"].mean(),
            "pts_away": away_games["pts_away"].mean(),
            "ppda_home": ppda_home,
            "ppda_away": ppda_away,
            "ppda_allowed_home": ppda_allowed_home,
            "ppda_allowed_away": ppda_allowed_away,
            "goal_diff": goal_diff,
            "goals_total": goals_total,
            "form_diff": form_diff,
            "draw_rate": draw_rate,
            "ppda_diff": ppda_diff,
            "attack_strength_home": attack_strength_home,
            "attack_strength_away": attack_strength_away,
        }

        df_feat = pd.DataFrame([features])
        # Reordenar igual que entrenamiento
        df_feat = df_feat.reindex(columns=self.features, fill_value=0)
        return df_feat.fillna(0), home_games, away_games

    def predict_match(self, home_team, away_team):
        """
        Preddicción principal - Falta adaptación del colab
        """
        # Preparación de los features
        features_df, _, _ = self.prepare_features(home_team, away_team)
        probs = self.model.predict_proba(features_df)[0]
        # ===============================
        # AJUSTES BOOKMAKER
        # ===============================
        # 1. Suavizar hacia promedio Premier League
        probs = self._shrink_to_league_avg(probs, alpha=0.22)
        # 2. Limitar extremos (clamp)
        probs = self._clamp_probs(probs, min_p=0.10, max_p=0.70)
        # 3. Reducir empate inflado
        probs = self._reduce_draw_bias(probs, max_draw=0.38)

        # Convertir array a diccionario con etiquetas reales
        probs_dict = dict(zip(self.le.classes_, probs))

        label = self.le.inverse_transform([np.argmax(probs)])[0]
        mapping = {"w": "home", "d": "draw", "l": "away"}

        return {
            "prediction": mapping[label],
            "confidence": round(np.max(probs) * 100, 2),
            "probabilities": {
                "home": round(probs_dict["w"] * 100, 2),
                "draw": round(probs_dict["d"] * 100, 2),
                "away": round(probs_dict["l"] * 100, 2),
            },
        }

    def build_match_summary(self, home_team, away_team, prediction_result, n_last=5):
        """
        Construye un resumen tipo Colab para que Gemini analice con contexto real.
        """

        # Promedios generales
        home_stats = self.team_stats_home.loc[home_team]
        away_stats = self.team_stats_away.loc[away_team]

        # Últimos partidos del local
        home_hist = (
            self.historical_df[
                (self.historical_df["team_home"] == home_team)
                | (self.historical_df["team_away"] == home_team)
            ]
            .sort_values("date_home", ascending=False)
            .head(n_last)
        )

        # Últimos partidos del visitante
        away_hist = (
            self.historical_df[
                (self.historical_df["team_home"] == away_team)
                | (self.historical_df["team_away"] == away_team)
            ]
            .sort_values("date_home", ascending=False)
            .head(n_last)
        )

        summary = f"""
        PARTIDO: {home_team} vs {away_team}

        ════════════════════════════
        PROMEDIOS DEL LOCAL
        ════════════════════════════
        - xG: {home_stats['xG_home']:.2f}
        - xGA: {home_stats['xGA_home']:.2f}
        - Deep completions: {home_stats['deep_home']:.2f}
        - Deep allowed: {home_stats['deep_allowed_home']:.2f}

        ════════════════════════════
        PROMEDIOS DEL VISITANTE
        ════════════════════════════
        - xG: {away_stats['xG_away']:.2f}
        - xGA: {away_stats['xGA_away']:.2f}
        - Deep completions: {away_stats['deep_away']:.2f}
        - Deep allowed: {away_stats['deep_allowed_away']:.2f}

        ════════════════════════════
        ÚLTIMOS {n_last} PARTIDOS LOCAL
        ════════════════════════════
        {home_hist[['team_home','team_away','scored_home','scored_away','xG_home','xG_away']].to_string(index=False)}

        ════════════════════════════
        ÚLTIMOS {n_last} PARTIDOS VISITANTE
        ════════════════════════════
        {away_hist[['team_home','team_away','scored_home','scored_away','xG_home','xG_away']].to_string(index=False)}

        ════════════════════════════
        PROBABILIDADES CALCULADAS
        ════════════════════════════
        - Local gana: {prediction_result['probabilities']['home']}%
        - Empate: {prediction_result['probabilities']['draw']}%
        - Visitante gana: {prediction_result['probabilities']['away']}%
        """

        return summary

    def train_model(self):
        # Columnas a usar (escaladas después)
        """
        Entrena el modelo usando Gradient Boosting.
        """

        df = self.historical_df.copy()

        # ===============================
        # 1. CONVERTIR PPDA A FLOAT
        # ===============================
        ppda_cols = ["ppda_home", "ppda_away", "ppda_allowed_home", "ppda_allowed_away"]

        for col in ppda_cols:
            df[col] = df[col].apply(self.parse_ppda)

        # ===============================
        # FEATURES PRINCIPALES
        # ===============================
        features = [
            # xG base
            "xG_home",
            "xGA_home",
            "xG_away",
            "xGA_away",
            # Goles reales (MUY importante)
            "scored_home",
            "scored_away",
            "missed_home",
            "missed_away",
            # Forma histórica
            "wins_home",
            "wins_away",
            "draws_home",
            "draws_away",
            "loses_home",
            "loses_away",
            # Puntos
            "pts_home",
            "pts_away",
            # Presión
            "ppda_home",
            "ppda_away",
            "ppda_allowed_home",
            "ppda_allowed_away",
        ]

        # ===============================
        # FEATURES DIFERENCIALES CLAVE
        # ===============================

        df["goal_diff"] = df["scored_home"] - df["scored_away"]
        df["goals_total"] = df["scored_home"] + df["scored_away"]

        df["form_diff"] = df["pts_home"] - df["pts_away"]
        df["draw_rate"] = (df["draws_home"] + df["draws_away"]) / 2

        df["ppda_diff"] = df["ppda_home"] - df["ppda_away"]

        df["attack_strength_home"] = df["scored_home"] - df["missed_home"]
        df["attack_strength_away"] = df["scored_away"] - df["missed_away"]

        features += [
            "goal_diff",
            "goals_total",
            "form_diff",
            "draw_rate",
            "ppda_diff",
            "attack_strength_home",
            "attack_strength_away",
        ]

        self.features = features

        # ===============================
        # VALIDACIÓN DE COLUMNAS
        # ===============================
        missing = [col for col in self.features if col not in df.columns]
        if missing:
            raise ValueError(f"Faltan columnas en el CSV: {missing}")

        # ===============================
        # MATRIZ X e Y
        # ===============================
        X = df[self.features]
        X = X.fillna(X.mean(numeric_only=True))
        X = X.fillna(0)

        y = df['result_home']  # 'w', 'd', 'l'

        if len(np.unique(y)) < 3:
            raise ValueError("Dataset incompleto: faltan clases w/d/l")

        # ===============================
        # LABEL ENCODER
        # ===============================
        self.le = LabelEncoder()
        y_encoded = self.le.fit_transform(y)
        # ===============================
        # MODELO: GRADIENT BOOSTING
        # ===============================
        base_model = HistGradientBoostingClassifier(
            max_iter=150,
            learning_rate=0.1,
            max_depth=3,
            min_samples_leaf=20,
            random_state=42,
        )

        weights = {"w": 1.0, "l": 1.0, "d": 0.75}
        sample_weights = y.map(weights)
        # Entrenar
        self.model = CalibratedClassifierCV(base_model, cv=3)
        self.model.fit(X, y_encoded, sample_weight=sample_weights)
    # ==========================================================
    # HEURÍSTICAS PARA PROBABILIDADES REALISTAS (BOOKMAKER STYLE)
    # ==========================================================

    def _shrink_to_league_avg(self, probs, alpha=0.22):
        """
        Evita extremos tipo 99%-1%-0%
        Mezcla predicción con distribución promedio de Premier League.
        """

        # Promedio real aproximado Premier:
        # Orden según LabelEncoder: ['d','l','w']
        league_avg = np.array([0.25, 0.30, 0.45])

        # Mezcla suavizada
        probs = (1 - alpha) * probs + alpha * league_avg

        return probs / probs.sum()

    def _clamp_probs(self, probs, min_p=0.08, max_p=0.78):
        """
        Limita probabilidades extremas como hacen las casas de apuestas.
        Evita resultados tipo 99%-1%.
        """
        probs = np.clip(probs, min_p, max_p)
        return probs / probs.sum()

    def _reduce_draw_bias(self, probs, max_draw=0.42):
        """
        Reduce empates exagerados.
        Si el modelo da draw demasiado alto, lo recorta.
        """
        probs_dict = dict(zip(self.le.classes_, probs))

        if probs_dict["d"] > max_draw:
            excess = probs_dict["d"] - max_draw
            probs_dict["d"] = max_draw
            probs_dict["w"] += excess / 2
            probs_dict["l"] += excess / 2

        new_probs = np.array([probs_dict["d"], probs_dict["l"], probs_dict["w"]])
        return new_probs / new_probs.sum()

    def get_gemini_analysis(self, home_team, away_team, prediction_result):
        # --- Cache por mes para que no sea eterno ---
        today = datetime.now().strftime("%Y-%m")
        confidence = prediction_result["confidence"]
        # --- Generar clave única ---
        key = f"{today}_{home_team}_vs_{away_team}_{confidence}"

        # --- Revisar cache ---
        if key in self.gemini_cache:
            return self.gemini_cache[key]
        # --- Límite máximo diario/local ---
        if len(self.gemini_cache) > 200:
            return "Límite diario alcanzado. Usa análisis estadístico local."
        # ===============================
        # 1️⃣ Obtener API key de Streamlit o local
        # ===============================
        api_key = None
        try:
            import streamlit as st
            try:
                api_key = st.secrets.get("GOOGLE_AI_API_KEY", None)
            except st.errors.StreamlitSecretNotFoundError:
                api_key = None
        except ModuleNotFoundError:
            api_key = None
        # Fallback a .env local
        if api_key is None:
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
            import os
            api_key = os.getenv("GOOGLE_AI_API_KEY", None)
        # ===============================
        # 2️⃣ Si no hay clave, usar fallback local
        # ===============================
        if not api_key:
            print(f"⚠️ Error ejecutando Gemini API: {e}")
            home_p = prediction_result["probabilities"]["home"]
            draw_p = prediction_result["probabilities"]["draw"]
            away_p = prediction_result["probabilities"]["away"]
            avg_goals = prediction_result.get("expected_goals", (home_p + away_p) / 2)
            fallback = (
                f"💡 Límite de peticiones alcanzado o API key no disponible. Fallback estadístico:\n"
                f"- Probabilidades: Local {home_p}%, Empate {draw_p}%, Visitante {away_p}%\n"
                f"- Escenario de goles: +1.5 probable, promedio esperado {avg_goals:.1f} goles.\n"
                f"- Recomendación: basarse en tendencias recientes y xG de equipos."
            )
            return fallback

        # ===============================
        # 3️⃣ Ejecutar API si hay clave
        # ===============================
        try:
            from google import genai

            client = genai.Client(api_key=api_key)

            resumen = self.build_match_summary(home_team, away_team, prediction_result)

            prompt = f"""
                    Eres un analista deportivo profesional. Tu objetivo principal es dar recomendaciones de apuestas
                    basadas en la cantidad de goles totales (por ejemplo: más de 1.5 goles, más de 2.5 goles), 
                    pero sin dejar de lado las apuestas tradicionales de resultado (local, empate, visitante) y otras métricas
                    como corners o tendencias de juego.

                    📌 Usa las estadísticas reales de cada equipo disponibles en este resumen y prioriza escenarios
                    de goles que tengan alta probabilidad según el historial de los equipos, pero sé conservador
                    y coherente.

                    RESUMEN DISPONIBLE:
                    {resumen}

                    Devuelve en formato estricto:

                    1. ANÁLISIS GENERAL
                    2. 📌 APUESTA GOLES (total esperado, +1.5, +2.5, etc.)
                    3. 📌 APUESTA ESTRUCTURA (resultado seguro: local/empate/visitante)
                    4. ⚽ APUESTA DINÁMICA (goles por tiempo, corners, tendencias)
                    5. JUSTIFICACIÓN TÉCNICA (xG, defensa, tendencias, forma reciente)
                    6. MÉTRICA CLAVE (escenario esperado de goles y resultado)

                    Sé claro y evita jerga técnica compleja: explica xG, xGA o Deep completions en términos de goles o defensa.
                    """

            response = client.models.generate_content(
                        model="gemini-2.5-flash", contents=prompt
                    )
            self.gemini_cache[key] = response.text
            self.save_cache()
            return response.text
        except Exception as e:
            print(f"⚠️ Error ejecutando Gemini API: {e}")
            # --- fallback local en caso de fallo API ---
            home_p = prediction_result["probabilities"]["home"]
            draw_p = prediction_result["probabilities"]["draw"]
            away_p = prediction_result["probabilities"]["away"]
            avg_goals = prediction_result.get("expected_goals", (home_p + away_p) / 2)
            fallback = (
                f"💡 Límite de peticiones alcanzado o error API. Fallback estadístico:\n"
                f"- Probabilidades: Local {home_p}%, Empate {draw_p}%, Visitante {away_p}%\n"
                f"- Escenario de goles: +1.5 probable, promedio esperado {avg_goals:.1f} goles.\n"
                f"- Recomendación: basarse en tendencias recientes y xG de equipos."
            )
            return fallback

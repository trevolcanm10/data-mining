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
import requests
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder, StandardScaler

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
        self.team_mapping = self._load_team_mapping()
        

        self.load_historical_data()
        self.build_team_stats()

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

    def load_historical_data(self, path="data/matches.csv"):
        """
        Carga el conjunto de datos históricos desde un archivo CSV
        para el entrenamiento y análisis del modelo.
        """
        self.historical_df = pd.read_csv(path)

    def build_team_stats(self):
        """
        Procesa los datos históricos para calcular y consolidar las
        métricas de rendimiento por equipo.
        """
        df = self.historical_df.copy()

        self.team_stats_home = df.groupby("team_home").agg(
            {
                "xG_home": "mean",
                "deep_home": "mean",
                "npxG_home": "mean",
                "xGA_home": "mean",
                "deep_allowed_home": "mean",
            }
        )

        self.team_stats_away = df.groupby("team_away").agg(
            {
                "xG_away": "mean",
                "deep_away": "mean",
                "npxG_away": "mean",
                "xGA_away": "mean",
                "deep_allowed_away": "mean",
            }
        )

    def fetch_fixtures(self, days_ahead=30):
        "Obtener partidos futuros"
        from dotenv import load_dotenv

        load_dotenv()
        API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
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

    def prepare_features(self, home_team, away_team):
        """
        Extrae y organiza las métricas estadísticas de ambos equipos para
        generar el vector de características necesario para la predicción.
        """

        if home_team not in self.team_stats_home.index:
            raise ValueError(f"Equipo local sin datos: {home_team}")

        if away_team not in self.team_stats_away.index:
            raise ValueError(f"Equipo visitante sin datos:{away_team}")

        home = self.team_stats_home.loc[home_team]
        away = self.team_stats_away.loc[away_team]

        features = {
            "home_xg": home["xG_home"],
            "home_deep": home["deep_home"],
            "home_np_diff": home["npxG_home"],
            "home_xga": home["xGA_home"],
            "home_deep_allowed": home["deep_allowed_home"],
            "away_xg": away["xG_away"],
            "away_deep": away["deep_away"],
            "away_np_diff": away["npxG_away"],
            "away_xga": away["xGA_away"],
            "away_deep_allowed": away["deep_allowed_away"],
        }

        return pd.DataFrame([features])

    def predict_match(self, home_team, away_team):
        """
        Preddicción principal - Falta adaptación del colab
        """
        try:
            # Preparación de los features
            features_df = self.prepare_features(home_team, away_team)
            # Heurística simple - revisión del colab para modificación
            home_score = (
                features_df["home_xg"].iloc[0]
                + features_df["home_deep"].iloc[0]
                + features_df["home_np_diff"].iloc[0]
                + (1 - features_df["home_xga"].iloc[0])
                + (1 - features_df["home_deep_allowed"].iloc[0])
            )

            away_score = (
                features_df["away_xg"].iloc[0]
                + features_df["away_deep"].iloc[0]
                + features_df["away_np_diff"].iloc[0]
                + (1 - features_df["away_xga"].iloc[0])
                + (1 - features_df["away_deep_allowed"].iloc[0])
            )

            draw_raw = np.exp(-np.abs(home_score - away_score))

            total = home_score + away_score + draw_raw

            prob_home = home_score / total
            prob_draw = draw_raw / total
            prob_away = away_score / total

            probs = [prob_home, prob_draw, prob_away]
            max_idx = np.argmax(probs)
            outcomes = ["home", "draw", "away"]

            result = {
                "prediction": outcomes[max_idx],
                "confidence": round(probs[max_idx] * 100, 1),
                "probabilities": {
                    "home": round(prob_home * 100, 1),
                    "draw": round(prob_draw * 100, 1),
                    "away": round(prob_away * 100, 1),
                },
                "metrics": {
                    "home_score": round(home_score, 2),
                    "away_score": round(away_score, 2),
                    "advantage": "home" if home_score > away_score else "away",
                },
            }
            return result

        except (KeyError, IndexError, ValueError, TypeError) as e:

            print(f"Error in prediction: {e}")
            return {
                "prediction": "draw",
                "confidence": 50.0,
                "probabilities": {"home": 40, "draw": 35, "away": 25},
                "metrics": {"error": str(e)},
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

    def get_gemini_analysis(self, home_team, away_team, prediction_result):
        try:
            from google import genai
            from dotenv import load_dotenv
            # import os

            load_dotenv()

            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if not api_key:
                return "Análisis no disponible - Configura API key"

            client = genai.Client(api_key=api_key)

            resumen = self.build_match_summary(home_team, away_team, prediction_result)

            prompt = f"""
            Eres un analista deportivo profesional.
            Explica el partido de forma clara para cualquier aficionado que incursiona en las apuestas,
            trata de no usar términos técnicos como xG, xGA o Deep completions, por el contrario traduce
            estos terminos para que el usuario pueda comprenderte 

            📌 RESUMEN DISPONIBLE:
            {resumen}

            Devuelve en formato estricto:

            1. ANÁLISIS GENERAL
            2. 📌 APUESTA ESTRUCTURA (segura)
            3. ⚽ APUESTA DINÁMICA (goles/corners)
            4. JUSTIFICACIÓN TÉCNICA (xG, defensa, tendencias)
            5. MÉTRICA CLAVE (escenario esperado)

            Sé conservador y coherente.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=prompt
            )

            return response.text

        except (ImportError, AttributeError, RuntimeError) as e:
            return f"Análisis IA temporalmente no disponible. Error: {str(e)}"

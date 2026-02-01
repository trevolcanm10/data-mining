#Lógica de predicción
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime,timedelta
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder #Convertir etiquetas categóricas en números
import warnings

warnings.filterwarnings('ignore')

class PremierLeaguePredictor:
    def __init__(self):
        self.fixtures_df = None
        self.historical_df = None
        self.team_stats_home = None
        self.team_stats_away =None
        self.team_mapping = self._load_team_mapping()
        self.model = None
        self.le = None
        
        self.load_historical_data()
        self.build_team_stats()
    
    
    def _load_team_mapping(self):
        "Mapeo de nombres API vs Understat"
        return {
            'Brighton & Hove Albion FC': 'Brighton',
            'Crystal Palace FC': 'Crystal Palace',
            'Leeds United FC': 'Leeds',
            'Leicester City FC': 'Leicester City',
            'Liverpool FC': 'Liverpool',
            'Manchester City FC': 'Manchester City',
            'Manchester United FC': 'Manchester United',
            'Newcastle United FC': 'Newcastle United',
            'Nottingham Forest FC': 'Nottingham Forest',
            'Tottenham Hotspur FC': 'Tottenham',
            'West Ham United FC': 'West Ham',
            'Wolverhampton Wanderers FC': 'Wolverhampton Wanderers',
            'AFC Bournemouth': 'Bournemouth',
            'Aston Villa FC': 'Aston Villa',
            'Burnley FC': 'Burnley',
            'Chelsea FC': 'Chelsea',
            'Everton FC': 'Everton',
            'Fulham FC': 'Fulham',
            'Sunderland AFC': 'Sunderland',
            'Brentford FC': 'Brentford',
            'Arsenal FC': 'Arsenal',
            'Manchester United': 'Manchester United',  # por si acaso
            'Manchester City': 'Manchester City',
            'Arsenal': 'Arsenal',
            'Liverpool': 'Liverpool',
            'Chelsea': 'Chelsea',
            'Tottenham Hotspur': 'Tottenham',
            'Newcastle United': 'Newcastle United',
            'West Ham United': 'West Ham',
            'Aston Villa': 'Aston Villa',
            'Brighton': 'Brighton',
            'Brentford': 'Brentford',
            'Crystal Palace': 'Crystal Palace',
            'Everton': 'Everton',
            'Fulham': 'Fulham',
            'Nottingham Forest': 'Nottingham Forest',
            'Wolverhampton Wanderers': 'Wolverhampton Wanderers',
            'Bournemouth': 'Bournemouth',
            'Leeds': 'Leeds',
            'Leicester City': 'Leicester City',
            'Southampton': 'Southampton',
            'Burnley': 'Burnley',
            'Sheffield United': 'Sheffield United',
            'Luton Town': 'Luton Town'
        }
    
    def load_historical_data(self,path="data/matches.csv"):
        self.historical_df = pd.read_csv(path)
        
    def build_team_stats(self):
        df = self.historical_df.copy()
        
        self.team_stats_home = df.groupby("team_home").agg({
            "xG_home": "mean",
            "deep_home": "mean",
            "npxG_home": "mean",
            "xGA_home": "mean",
            "deep_allowed_home": "mean"
        })
        
        
        self.team_stats_away =df.groupby("team_away").agg({
            
            "xG_away": "mean",
            "deep_away": "mean",
            "npxG_away": "mean",
            "xGA_away": "mean",
            "deep_allowed_away": "mean"
            
        })
        
    def fetch_fixtures(self,days_ahead=30):
        "Obtener partidos futuros"
        from dotenv import load_dotenv
        load_dotenv()
        API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
        url = "https://api.football-data.org/v4/competitions/PL/matches"
        
        headers = {"X-Auth-Token": API_KEY}
        
        #Fechas dinámicas
        date_from = datetime.now().strftime('%Y-%m-%d')
        date_to = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
        
        params = {"dateFrom": date_from, "dateTo": date_to}
        
        try:
            response = requests.get(url,headers=headers,params=params)
            data = response.json()
            
            fixtures = []
            
            for match in data.get("matches",[]):
                fixtures.append({
                    
                    "date": match["utcDate"],
                    "home_team": match["homeTeam"]["name"],
                    "away_team": match["awayTeam"]["name"],
                    "status": match["status"],
                    "matchday": match.get("matchday", 0) 
                })
                
            self.fixtures_df = pd.DataFrame(fixtures)
            #Aplicación de mapeo
            self.fixtures_df['home_team'] = self.fixtures_df['home_team'].map(self.team_mapping).fillna(self.fixtures_df['home_team'])
            self.fixtures_df['away_team'] = self.fixtures_df['away_team'].map(self.team_mapping).fillna(self.fixtures_df['away_team'])
            
            return self.fixtures_df

        except Exception as e:
            
            print(f"Error fetching fixtures: {e}")
            #Datos de ejemplo si falla
            return pd.DataFrame({
                'home_team': ['Manchester City', 'Arsenal', 'Liverpool'],
                'away_team': ['Chelsea', 'Tottenham', 'Manchester United'],
                'date': [datetime.now().strftime('%Y-%m-%d')]*3
            })
            
    def prepare_features(self,home_team,away_team):
         # Features base (simuladas, después pondrás las reales)
        
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
    
    
    def predict_match(self,home_team,away_team):
        """
        Preddicción principal - Falta adaptación del colab
        """
        try:
            #Preparación de los features
            features_df =self.prepare_features(home_team,away_team)
            #Heurística simple - revisión del colab para modificación
            home_score = (
                features_df['home_xg'].iloc[0] + 
                features_df['home_deep'].iloc[0] +
                features_df['home_np_diff'].iloc[0] + 
                (1 - features_df['home_xga'].iloc[0]) +
                (1 - features_df['home_deep_allowed'].iloc[0])
            )
            
            away_score = (
                features_df['away_xg'].iloc[0] +
                features_df['away_deep'].iloc[0] +
                features_df['away_np_diff'].iloc[0] +
                (1 - features_df['away_xga'].iloc[0]) +
                (1 - features_df['away_deep_allowed'].iloc[0])
            )
            
            draw_raw = np.exp(-np.abs(home_score - away_score))
            
            total = home_score + away_score + draw_raw
            
            prob_home = home_score / total
            prob_draw = draw_raw / total
            prob_away = away_score / total
            
            probs = [prob_home,prob_draw,prob_away]
            max_idx = np.argmax(probs)
            outcomes = ['home','draw','away']
            
            result = {
                'prediction': outcomes[max_idx],
                'confidence': round(probs[max_idx] * 100, 1),
                'probabilities': {
                    'home': round(prob_home * 100, 1),
                    'draw': round(prob_draw * 100, 1),
                    'away': round(prob_away * 100, 1)
                },
                'metrics': {
                    'home_score': round(home_score, 2),
                    'away_score': round(away_score, 2),
                    'advantage': 'home' if home_score > away_score else 'away'
                }
            }
            return result

        except Exception as e:
            
            print(f"Error in prediction: {e}")
            return{
                'prediction': 'draw',
                'confidence': 50.0,
                'probabilities': {'home': 40, 'draw': 35, 'away': 25},
                'metrics': {'error': str(e)}
            }
            
            
    def get_gemini_analysis(self, home_team, away_team, prediction_result):
        try:
            from google import genai
            from dotenv import load_dotenv
            import os
            load_dotenv()
            
            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if not api_key:
                return "Análisis no disponible - Configura API key"
            
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Analiza este partido de Premier League:
            
            {home_team} vs {away_team}
            
            Probabilidades calculadas:
            - Local gana: {prediction_result['probabilities']['home']}%
            - Empate: {prediction_result['probabilities']['draw']}%
            - Visitante gana: {prediction_result['probabilities']['away']}%
            
            Dime en 2-3 líneas:
            1. Qué esperar del partido
            2. Una apuesta interesante (ej: ambos marcan, over/under)
            3. Factor clave a observar
            
            Sé conciso y profesional.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            return response.text
            
        except Exception as e:
            return f"Análisis IA temporalmente no disponible. Error: {str(e)}"




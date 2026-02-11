from utils.predictor import PremierLeaguePredictor
import pandas as pd

print("\n TEST GENERAL DEL MODELO PREMIER LEAGUE\n")

predictor = PremierLeaguePredictor()

df = predictor.historical_df.sample(100)

draws = 0

for _, row in df.iterrows():
    res = predictor.predict_match(row["team_home"], row["team_away"])
    if res["prediction"] == "draw":
        draws += 1

print("Draw rate:", draws, "%")

matches = [
    ("Manchester City", "Chelsea"),
    ("Arsenal", "Tottenham"),
    ("Liverpool", "Manchester United"),
    ("Newcastle United", "Everton"),
    ("Brighton", "West Ham"),
]

results = []

print("===============================")
print("⚽ TEST DE PREDICCIONES")
print("===============================\n")

for home, away in matches:

    res = predictor.predict_match(home, away)

    probs = res["probabilities"]

    print(f"🏟️ {home} vs {away}")
    print(f"➡️ Predicción: {res['prediction']} ({res['confidence']}%)")

    print(
        f"   Probabilidades: "
        f"Home={probs['home']}% | "
        f"Draw={probs['draw']}% | "
        f"Away={probs['away']}%"
    )

    print("-" * 50)

    results.append(
        {
            "home": home,
            "away": away,
            "pred": res["prediction"],
            "home_win": probs["home"],
            "draw": probs["draw"],
            "away_win": probs["away"],
        }
    )


# ===============================
# 📊 RESUMEN FINAL
# ===============================

df = pd.DataFrame(results)

print("\n===============================")
print("📌 RESUMEN TABLA FINAL")
print("===============================\n")

print(df)

print("\n===============================")
print("📊 PROMEDIOS GENERALES")
print("===============================\n")

print("Home Win Avg:", round(df["home_win"].mean(), 2), "%")
print("Draw Avg:", round(df["draw"].mean(), 2), "%")
print("Away Win Avg:", round(df["away_win"].mean(), 2), "%")

print("\n✅ TEST TERMINADO\n")

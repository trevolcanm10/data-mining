from utils.predictor import PremierLeaguePredictor

predictor = PremierLeaguePredictor()

# 1️⃣ Probar predicción
result = predictor.predict_match("Manchester City", "Chelsea")
print("PREDICCIÓN:")
print(result)

# 2️⃣ Probar análisis IA
analysis = predictor.get_gemini_analysis(
    "Manchester City",
    "Chelsea",
    result
)

print("\nANÁLISIS IA:")
print(analysis)

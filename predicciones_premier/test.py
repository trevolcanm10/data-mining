from utils.predictor import PremierLeaguePredictor
import pandas as pd

# ===============================
# TEST PRINCIPAL DEL DATASET
# ===============================

print("\n🚀 Iniciando prueba del dataset...\n")

# Crear instancia del predictor (carga dataset automáticamente)
predictor = PremierLeaguePredictor()

df = predictor.historical_df

# ===============================
# 1. TOTAL PARTIDOS
# ===============================
print("📌 TOTAL partidos en dataset:", len(df))

# ===============================
# 2. RANGO DE FECHAS
# ===============================
df["date_home"] = pd.to_datetime(df["date_home"], errors="coerce")

print("\n📅 Rango de fechas:")
print("Desde:", df["date_home"].min())
print("Hasta:", df["date_home"].max())

# ===============================
# 3. PARTIDOS POR EQUIPO
# ===============================
print("\n🏠 Partidos como LOCAL (Top 10):")
print(df["team_home"].value_counts().head(10))

print("\n✈️ Partidos como VISITANTE (Top 10):")
print(df["team_away"].value_counts().head(10))

# ===============================
# 4. MÍNIMO PARTIDOS POR EQUIPO
# ===============================
min_home = df["team_home"].value_counts().min()
min_away = df["team_away"].value_counts().min()

print("\n⚠️ Mínimo partidos disponibles:")
print("Local:", min_home)
print("Visitante:", min_away)

# ===============================
# 5. ÚLTIMOS PARTIDOS REGISTRADOS
# ===============================
print("\n🔥 Últimos 10 partidos del dataset:")

print(
    df.sort_values("date_home", ascending=False).head(10)[
        ["date_home", "team_home", "team_away", "scored_home", "scored_away"]
    ]
)

print("\n✅ Prueba finalizada correctamente.\n")

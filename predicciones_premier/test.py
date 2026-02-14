import google.generativeai as genai

# 1️⃣ Configurar tu API key (opcional, solo para probar conectividad)
genai.configure(api_key="AIzaSyCguzK1g4Khd1-BVjfrU0OnLRcgLxq4fdk")

# 2️⃣ Listar todos los modelos disponibles
print("=== Modelos disponibles ===")
for m in genai.list_models():
    print(m.name, "-", getattr(m, "display_name", "sin display_name"))
    print("Métodos soportados:", getattr(m, "supported_generation_methods", []))
    print("---")

# 3️⃣ Listar las funciones del módulo para ver lo que realmente puedes usar
print("=== Funciones disponibles en google.generativeai ===")
print([f for f in dir(genai) if not f.startswith("_")])

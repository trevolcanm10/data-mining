from utils.cache_db import init_db, save_analysis, get_analysis


def main():
    print("\n🚀 Probando configuración de SQLite Cache...\n")

    # 1️⃣ Inicializar DB
    init_db()
    print("✅ Base de datos inicializada correctamente.")

    # 2️⃣ Crear clave de prueba
    key = "2026-02_ManchesterCity_vs_Arsenal"

    # 3️⃣ Guardar análisis falso
    fake_analysis = "🔥 Este es un análisis de prueba guardado en SQLite."

    save_analysis(key, fake_analysis)
    print("✅ Análisis guardado correctamente.")

    # 4️⃣ Recuperar análisis
    recovered = get_analysis(key)

    if recovered:
        print("\n✅ Caché funciona, análisis recuperado:\n")
        print("------------------------------------------------")
        print(recovered)
        print("------------------------------------------------")
    else:
        print("❌ Error: no se recuperó nada del caché.")


if __name__ == "__main__":
    main()

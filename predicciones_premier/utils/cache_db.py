"""
Conexión a la base datos y guardado del análisis
"""
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "..", "data", "gemini_cache.db")
# Crear carpeta si no existe
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

def init_db():
    """
    Conexión a la base de datos + creación de las tablas correspondientes
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS gemini_cache (
            key TEXT PRIMARY KEY,
            analysis TEXT,
            created_at TEXT
        )
    """
    )

    conn.commit()
    conn.close()


def get_analysis(key):
    """
    Traemos el análisis a través de la selección de la clave
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT analysis FROM gemini_cache WHERE key = ?", (key,))
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    return None


def save_analysis(key, analysis):
    """
    Guardamos el análisis generado por la API en la base de datos
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO gemini_cache (key, analysis, created_at)
        VALUES (?, ?, ?)
    """,
        (key, analysis, datetime.now().isoformat()),
    )

    conn.commit()
    conn.close()

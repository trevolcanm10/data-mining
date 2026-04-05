# config.py - Configuración global - Dark Cyberpunk / Sports Analytics Theme
import streamlit as st

# =========================
# COLORES PRINCIPALES
# =========================
PRIMARY_COLOR = "#00ff88"       # Verde neón principal
SECONDARY_COLOR = "#00d4ff"     # Cian neón
ACCENT_COLOR = "#ff00ff"        # Magenta neón
WARNING_COLOR = "#ffdd00"       # Amarillo neón
ERROR_COLOR = "#ff4757"         # Rojo neón
TEXT_COLOR = "#e0e0e0"          # Texto principal
TEXT_MUTED = "#8892b0"          # Texto secundario
BG_PRIMARY = "#0e1117"          # Fondo principal
BG_SECONDARY = "#1a1c24"       # Fondo secundario
BG_CARD = "rgba(255,255,255,0.03)"  # Fondo tarjetas
GLASS_BG = "rgba(15, 23, 42, 0.6)"  # Glassmorphism
GLASS_BORDER = "rgba(0, 255, 136, 0.15)"  # Borde glass
NEON_GLOW = "0 0 15px rgba(0, 255, 136, 0.3)"  # Glow verde
CYAN_GLOW = "0 0 15px rgba(0, 212, 255, 0.3)"  # Glow cian

# =========================
# ESTILOS DINÁMICOS PARA TARJETAS DE PREDICCIÓN
# =========================
PREDICTION_CARD_STYLE = f"""
    background: {GLASS_BG};
    border: 1px solid {GLASS_BORDER};
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: {NEON_GLOW};
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
"""

PREDICTION_CARD_TITLE_STYLE = f"""
    text-align: center;
    color: {PRIMARY_COLOR};
    font-family: 'Inter', 'Segoe UI', sans-serif;
    font-weight: 800;
    letter-spacing: -0.5px;
"""


def setup_page():
    """Configura CSS global - Dark Cyberpunk / Sports Analytics Theme"""
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* ============================================
           GLOBAL RESET & BASE
           ============================================ */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        :root {
            --neon-green: #00ff88;
            --neon-cyan: #00d4ff;
            --neon-magenta: #ff00ff;
            --neon-yellow: #ffdd00;
            --neon-red: #ff4757;
            --bg-primary: #0e1117;
            --bg-secondary: #1a1c24;
            --bg-card: rgba(255,255,255,0.03);
            --glass-bg: rgba(15, 23, 42, 0.6);
            --glass-border: rgba(0, 255, 136, 0.15);
            --text-primary: #e0e0e0;
            --text-muted: #8892b0;
        }

        .stApp {
            background: linear-gradient(160deg, #0e1117 0%, #131620 30%, #1a1c24 60%, #0e1117 100%) !important;
            color: var(--text-primary);
            font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
        }

        /* Hide default Streamlit header & footer */
        header[data-testid="stHeader"] {
            background: transparent !important;
            backdrop-filter: blur(10px);
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}

        /* ============================================
           SCROLLBAR CUSTOM
           ============================================ */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--neon-green), var(--neon-cyan));
            border-radius: 10px;
        }

        /* ============================================
           TYPOGRAPHY
           ============================================ */
        h1, .stTitle h1 {
            font-family: 'Inter', sans-serif !important;
            font-size: 2.2rem !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            text-align: center;
            margin-bottom: 8px;
            letter-spacing: -1px;
            background: linear-gradient(135deg, #00ff88, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        h2, h3, .stSubheader {
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            color: #ffffff !important;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }

        h2 { font-size: 1.6rem !important; }
        h3 { font-size: 1.3rem !important; }

        p, li, span, div {
            font-family: 'Inter', sans-serif;
        }

        /* ============================================
           MAIN CARD - Glassmorphism Container
           ============================================ */
        .main-card {
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(0, 255, 136, 0.12);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 24px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .main-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-green), var(--neon-cyan), transparent);
            opacity: 0.6;
        }

        .main-card:hover {
            border-color: rgba(0, 255, 136, 0.3);
            box-shadow: 0 8px 32px rgba(0, 255, 136, 0.08);
            transform: translateY(-2px);
        }

        /* ============================================
           PREDICTION HEADER
           ============================================ */
        .prediction-header {
            text-align: center;
            padding: 20px 0;
            position: relative;
        }

        .prediction-header h2 {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.8rem !important;
            font-weight: 900 !important;
            background: linear-gradient(135deg, #00ff88, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .prediction-header .subtitle {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 4px;
            font-weight: 400;
        }

        /* ============================================
           STAT BOX - Metric Cards
           ============================================ */
        .stat-box {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 136, 0.1);
            border-radius: 16px;
            padding: 20px 16px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .stat-box::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 40%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--neon-green), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .stat-box:hover {
            border-color: rgba(0, 255, 136, 0.3);
            box-shadow: 0 4px 20px rgba(0, 255, 136, 0.1);
            transform: translateY(-3px);
        }

        .stat-box:hover::after {
            opacity: 1;
        }

        .stat-box .stat-icon {
            font-size: 1.8rem;
            margin-bottom: 8px;
            display: block;
        }

        .stat-box .stat-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 6px;
        }

        .stat-box .stat-value {
            font-family: 'Inter', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            color: #ffffff;
            line-height: 1;
        }

        .stat-box .stat-value.green { color: var(--neon-green); text-shadow: 0 0 20px rgba(0,255,136,0.4); }
        .stat-box .stat-value.cyan { color: var(--neon-cyan); text-shadow: 0 0 20px rgba(0,212,255,0.4); }
        .stat-box .stat-value.yellow { color: var(--neon-yellow); text-shadow: 0 0 20px rgba(255,221,0,0.4); }
        .stat-box .stat-value.red { color: var(--neon-red); text-shadow: 0 0 20px rgba(255,71,87,0.4); }
        .stat-box .stat-value.magenta { color: var(--neon-magenta); text-shadow: 0 0 20px rgba(255,0,255,0.4); }

        /* ============================================
           PROBABILITY CARDS (Home/Draw/Away)
           ============================================ */
        .prob-container {
            display: flex;
            gap: 16px;
            justify-content: center;
            margin: 24px 0;
        }

        .prob-card {
            flex: 1;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.06);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .prob-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            border-radius: 3px 3px 0 0;
        }

        .prob-card.home::before { background: linear-gradient(90deg, #00ff88, #00cc6a); }
        .prob-card.draw::before { background: linear-gradient(90deg, #ffdd00, #ffaa00); }
        .prob-card.away::before { background: linear-gradient(90deg, #ff4757, #ff6b81); }

        .prob-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }

        .prob-card .prob-label {
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .prob-card.home .prob-label { color: var(--neon-green); }
        .prob-card.draw .prob-label { color: var(--neon-yellow); }
        .prob-card.away .prob-label { color: var(--neon-red); }

        .prob-card .prob-value {
            font-family: 'Inter', sans-serif;
            font-size: 2.8rem;
            font-weight: 900;
            line-height: 1;
            margin-bottom: 4px;
        }

        .prob-card.home .prob-value { color: var(--neon-green); text-shadow: 0 0 30px rgba(0,255,136,0.3); }
        .prob-card.draw .prob-value { color: var(--neon-yellow); text-shadow: 0 0 30px rgba(255,221,0,0.3); }
        .prob-card.away .prob-value { color: var(--neon-red); text-shadow: 0 0 30px rgba(255,71,87,0.3); }

        .prob-card .prob-percent {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        /* ============================================
           MATCH CARD (Fixtures)
           ============================================ */
        .match-card {
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 136, 0.08);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .match-card:hover {
            border-color: rgba(0, 255, 136, 0.25);
            box-shadow: 0 4px 20px rgba(0, 255, 136, 0.06);
            transform: translateX(4px);
        }

        .match-card .team-info {
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 120px;
        }

        .match-card .team-info img {
            width: 44px;
            height: 44px;
            object-fit: contain;
            margin-bottom: 6px;
            filter: drop-shadow(0 0 6px rgba(0,255,136,0.3));
        }

        .match-card .team-info .team-name {
            font-size: 0.8rem;
            font-weight: 700;
            color: #ffffff;
            text-align: center;
        }

        .match-card .match-meta {
            text-align: center;
            flex: 1;
        }

        .match-card .match-meta .vs-text {
            font-family: 'Inter', sans-serif;
            font-size: 1.2rem;
            font-weight: 900;
            color: var(--neon-cyan);
            text-shadow: 0 0 10px rgba(0,212,255,0.3);
        }

        .match-card .match-meta .match-date {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        .match-card .match-meta .match-time {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--neon-green);
        }

        /* ============================================
           AI CONSOLE - Hacker Style
           ============================================ */
        .ai-console {
            background: rgba(10, 14, 20, 0.9);
            border: 1px solid rgba(0, 255, 136, 0.2);
            border-radius: 16px;
            padding: 0;
            margin: 20px 0;
            overflow: hidden;
            position: relative;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
        }

        .ai-console::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            border-radius: 16px;
            padding: 1px;
            background: linear-gradient(135deg, var(--neon-green), var(--neon-cyan), var(--neon-magenta), var(--neon-green));
            background-size: 300% 300%;
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            animation: borderGlow 4s ease infinite;
            pointer-events: none;
        }

        @keyframes borderGlow {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .ai-console-header {
            background: rgba(0, 255, 136, 0.05);
            padding: 12px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(0, 255, 136, 0.1);
        }

        .ai-console-header .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }

        .ai-console-header .dot.red { background: #ff4757; box-shadow: 0 0 6px #ff4757; }
        .ai-console-header .dot.yellow { background: #ffdd00; box-shadow: 0 0 6px #ffdd00; }
        .ai-console-header .dot.green { background: #00ff88; box-shadow: 0 0 6px #00ff88; }

        .ai-console-header .console-title {
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--neon-green);
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-left: 8px;
        }

        .ai-console-body {
            padding: 20px 24px;
            color: var(--neon-green);
            font-size: 0.85rem;
            line-height: 1.8;
            max-height: 500px;
            overflow-y: auto;
        }

        .ai-console-body .ai-line {
            opacity: 0;
            animation: typeIn 0.3s ease forwards;
        }

        .ai-console-body .ai-line:nth-child(1) { animation-delay: 0.1s; }
        .ai-console-body .ai-line:nth-child(2) { animation-delay: 0.2s; }
        .ai-console-body .ai-line:nth-child(3) { animation-delay: 0.3s; }
        .ai-console-body .ai-line:nth-child(4) { animation-delay: 0.4s; }
        .ai-console-body .ai-line:nth-child(5) { animation-delay: 0.5s; }
        .ai-console-body .ai-line:nth-child(6) { animation-delay: 0.6s; }
        .ai-console-body .ai-line:nth-child(7) { animation-delay: 0.7s; }
        .ai-console-body .ai-line:nth-child(8) { animation-delay: 0.8s; }
        .ai-console-body .ai-line:nth-child(9) { animation-delay: 0.9s; }
        .ai-console-body .ai-line:nth-child(10) { animation-delay: 1.0s; }

        @keyframes typeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .ai-console-body .highlight-green { color: var(--neon-green); font-weight: 700; }
        .ai-console-body .highlight-cyan { color: var(--neon-cyan); font-weight: 700; }
        .ai-console-body .highlight-yellow { color: var(--neon-yellow); font-weight: 700; }
        .ai-console-body .highlight-red { color: var(--neon-red); font-weight: 700; }

        /* ============================================
           TEAM GRID (Home Page)
           ============================================ */
        .teams-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 16px;
            margin: 20px 0;
        }

        .team-card {
            background: rgba(15, 23, 42, 0.5);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(0, 255, 136, 0.08);
            border-radius: 16px;
            padding: 20px 12px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
        }

        .team-card:hover {
            border-color: rgba(0, 255, 136, 0.3);
            box-shadow: 0 8px 24px rgba(0, 255, 136, 0.1);
            transform: translateY(-6px);
        }

        .team-card img {
            width: 56px;
            height: 56px;
            object-fit: contain;
            margin-bottom: 10px;
            filter: drop-shadow(0 0 8px rgba(0,255,136,0.2));
            transition: all 0.3s ease;
        }

        .team-card:hover img {
            filter: drop-shadow(0 0 16px rgba(0,255,136,0.5));
            transform: scale(1.1);
        }

        .team-card .team-name {
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            font-weight: 700;
            color: #ffffff;
        }

        /* ============================================
           NAV BUTTONS (Home Page)
           ============================================ */
        .nav-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin: 24px 0;
        }

        .nav-btn {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 136, 0.1);
            border-radius: 16px;
            padding: 24px 16px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none !important;
        }

        .nav-btn:hover {
            border-color: var(--neon-green);
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.15);
            transform: translateY(-4px);
        }

        .nav-btn .nav-icon {
            font-size: 2rem;
            margin-bottom: 10px;
            display: block;
        }

        .nav-btn .nav-label {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            font-weight: 700;
            color: #ffffff;
        }

        .nav-btn .nav-desc {
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 4px;
        }

        /* ============================================
           HERO BANNER
           ============================================ */
        .hero-banner {
            position: relative;
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: 28px;
        }

        .hero-banner img {
            width: 100%;
            height: 280px;
            object-fit: cover;
            border-radius: 20px;
            filter: brightness(0.6);
        }

        .hero-banner .hero-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 30px;
            background: linear-gradient(transparent, rgba(14, 17, 23, 0.95));
        }

        .hero-banner .hero-overlay h2 {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.6rem !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            margin: 0 0 6px 0;
        }

        .hero-banner .hero-overlay p {
            color: var(--text-muted);
            font-size: 0.9rem;
            margin: 0;
        }

        /* ============================================
           BADGE / PILL
           ============================================ */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .badge.green {
            background: rgba(0, 255, 136, 0.1);
            color: var(--neon-green);
            border: 1px solid rgba(0, 255, 136, 0.2);
        }

        .badge.cyan {
            background: rgba(0, 212, 255, 0.1);
            color: var(--neon-cyan);
            border: 1px solid rgba(0, 212, 255, 0.2);
        }

        .badge.yellow {
            background: rgba(255, 221, 0, 0.1);
            color: var(--neon-yellow);
            border: 1px solid rgba(255, 221, 0, 0.2);
        }

        /* ============================================
           STREAMLIT OVERRIDES
           ============================================ */
        /* Main content area */
        main .block-container {
            padding: 2rem 3rem !important;
            max-width: 1200px;
        }

        /* Image styling */
        .stImage img {
            border-radius: 16px;
            transition: all 0.4s ease;
        }

        .stImage img:hover {
            box-shadow: 0 0 30px rgba(0,255,136,0.15);
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.1)) !important;
            color: var(--neon-green) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            border: 1px solid rgba(0, 255, 136, 0.2) !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            transition: all 0.3s ease !important;
            letter-spacing: 0.5px;
        }

        div.stButton > button:hover {
            background: linear-gradient(135deg, rgba(0,255,136,0.2), rgba(0,212,255,0.2)) !important;
            border-color: var(--neon-green) !important;
            box-shadow: 0 0 20px rgba(0, 255, 136, 0.2) !important;
            transform: translateY(-2px);
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #00ff88, #00d4ff) !important;
            color: #0e1117 !important;
            border: none !important;
            font-weight: 800 !important;
            font-size: 1rem !important;
            letter-spacing: 1px;
        }

        div.stButton > button[kind="primary"]:hover {
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.4) !important;
            transform: translateY(-2px);
        }

        /* Selectbox */
        div[data-baseweb="select"] {
            font-family: 'Inter', sans-serif;
        }

        div[data-baseweb="select"] > div {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(0, 255, 136, 0.15) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: rgba(0, 255, 136, 0.4) !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(15, 23, 42, 0.5) !important;
            border: 1px solid rgba(0, 255, 136, 0.1) !important;
            border-radius: 12px !important;
            color: var(--text-muted) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            border-color: rgba(0, 255, 136, 0.3) !important;
            color: #ffffff !important;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(0, 255, 136, 0.1) !important;
            border-color: var(--neon-green) !important;
            color: var(--neon-green) !important;
        }

        .stTabs [data-baseweb="tab-highlight"] {
            display: none;
        }

        .stTabs [data-baseweb="tab-border"] {
            display: none;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(15, 23, 42, 0.5) !important;
            border: 1px solid rgba(0, 255, 136, 0.1) !important;
            border-radius: 12px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            color: var(--neon-green) !important;
        }

        /* Dataframe */
        .stDataFrame {
            border-radius: 12px;
            overflow: hidden;
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--neon-green), var(--neon-cyan)) !important;
        }

        /* Slider */
        .stSlider > div > div > div > div {
            background: var(--neon-green) !important;
        }

        /* Checkbox */
        .stCheckbox label span {
            font-family: 'Inter', sans-serif !important;
        }

        /* Info/Warning/Error boxes */
        .stAlert {
            border-radius: 12px !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Spinner */
        .stSpinner > div {
            border-top-color: var(--neon-green) !important;
        }

        /* ============================================
           SIDEBAR - Professional Dark Theme
           ============================================ */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0a0e14 0%, #131620 50%, #0a0e14 100%) !important;
        }

        div[data-testid="stSidebarContent"] {
            background: transparent !important;
            padding: 20px 16px !important;
        }

        /* Sidebar logo */
        section[data-testid="stSidebar"] img {
            display: block;
            margin: 0 auto;
            opacity: 0.9;
            transition: all 0.4s ease;
            border-radius: 8px;
            filter: drop-shadow(0 0 8px rgba(0,255,136,0.2));
        }

        section[data-testid="stSidebar"] img:hover {
            opacity: 1;
            transform: scale(1.05);
            filter: drop-shadow(0 0 20px rgba(0,255,136,0.5));
        }

        /* Sidebar navigation */
        [data-testid="stSidebarNav"] {
            margin-top: 16px;
        }

        [data-testid="stSidebarNav"] li {
            font-family: 'Inter', sans-serif;
            width: 100%;
        }

        [data-testid="stSidebarNav"] a {
            width: 100% !important;
            display: flex !important;
            align-items: center;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted) !important;
            text-decoration: none !important;
            background: transparent;
            border-left: 3px solid transparent;
            transition: all 0.25s ease;
        }

        [data-testid="stSidebarNav"] a:hover {
            background: rgba(0, 255, 136, 0.06);
            border-left: 3px solid var(--neon-green);
            color: #ffffff !important;
            transform: translateX(4px);
        }

        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(0, 255, 136, 0.1);
            border-left: 3px solid var(--neon-green);
            color: var(--neon-green) !important;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.08);
        }

        /* Sidebar custom boxes */
        .sidebar-title {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--neon-green);
            text-align: center;
            margin-bottom: 16px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .sidebar-box {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 255, 136, 0.08);
            transition: all 0.3s ease;
        }

        .sidebar-box:hover {
            background: rgba(0, 255, 136, 0.04);
            border-color: rgba(0, 255, 136, 0.15);
        }

        .sidebar-box h3 {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
        }

        .sidebar-box ol, .sidebar-box ul {
            padding-left: 18px;
            color: var(--text-muted);
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
        }

        .sidebar-box li {
            margin-bottom: 6px;
            line-height: 1.5;
        }

        .sidebar-box b {
            color: var(--neon-green);
        }

        /* ============================================
           HEADER CONTAINER
           ============================================ */
        .header-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
            padding: 24px 0 8px 0;
        }

        .header-container img {
            max-width: 80px;
            height: auto;
            border-radius: 8px;
            transition: all 0.4s ease;
            filter: drop-shadow(0 0 10px rgba(0,255,136,0.2));
        }

        .header-container img:hover {
            transform: scale(1.08);
            filter: drop-shadow(0 0 20px rgba(0,255,136,0.5));
        }

        .header-container .sub-header {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-muted);
            text-align: center;
            margin-top: 10px;
        }

        .header-container .sub-header.gradient {
            background: linear-gradient(90deg, var(--neon-green), var(--neon-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        }

        /* ============================================
           FOOTER
           ============================================ */
        .footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.8rem;
            margin-top: 3rem;
            padding: 24px 20px;
            border-top: 1px solid rgba(0, 255, 136, 0.08);
            font-family: 'Inter', sans-serif;
            background: rgba(10, 14, 20, 0.5);
            border-radius: 16px;
        }

        .footer:hover {
            background: rgba(0, 255, 136, 0.02);
        }

        .footer p {
            margin: 4px 0;
            line-height: 1.5;
        }

        .footer p span, .footer p i {
            font-weight: 600;
            color: var(--neon-green);
        }

        /* ============================================
           DIVIDER
           ============================================ */
        .cyber-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0,255,136,0.3), rgba(0,212,255,0.3), transparent);
            margin: 24px 0;
            border: none;
        }

        /* ============================================
           LOADING ANIMATION
           ============================================ */
        .pulse-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--neon-green);
            animation: pulse 1.5s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.3; transform: scale(0.8); }
            50% { opacity: 1; transform: scale(1.2); }
        }

        /* ============================================
           RESPONSIVE
           ============================================ */
        @media (max-width: 768px) {
            .prob-container { flex-direction: column; }
            .nav-grid { grid-template-columns: 1fr; }
            .teams-grid { grid-template-columns: repeat(2, 1fr); }
            main .block-container { padding: 1rem 1rem !important; }
        }

    </style>
    """,
        unsafe_allow_html=True,
    )

# Definir imágenes globales
IMAGES = {
    "premier_banner": "https://streamcoimg-a.akamaihd.net/cms/2025/8/0197d555-1250-4742-61d2-ef25bd273b0f.jpg?resize=1440px:*&quality=85",
    "vs_icon": "https://cdn-icons-png.flaticon.com/512/32/32328.png",
    "home_icon": "https://cdn-icons-png.flaticon.com/512/53/53254.png",
    "away_icon": "https://cdn-icons-png.flaticon.com/512/53/53254.png",
}

TEAM_LOGOS = {
    "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "Chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Tottenham": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",
    "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
    "Manchester United": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "Newcastle United": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    "Everton": "https://upload.wikimedia.org/wikipedia/en/7/7c/Everton_FC_logo.svg",
    "Brighton": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
    "West Ham": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    "Aston Villa": "https://cdn.worldvectorlogo.com/logos/aston-villa.svg",
    "Leeds": "https://upload.wikimedia.org/wikipedia/en/thumb/5/54/Leeds_United_F.C._logo.svg/1280px-Leeds_United_F.C._logo.svg.png",
    "Southampton": "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg",
    "Wolverhampton Wanderers": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
    "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/sco/thumb/d/d2/Nottingham_Forest_logo.svg/1280px-Nottingham_Forest_logo.svg.png",
    "Bournemouth": "https://upload.wikimedia.org/wikipedia/sco/thumb/e/e5/AFC_Bournemouth_%282013%29.svg/960px-AFC_Bournemouth_%282013%29.svg.png",
    "Fulham": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Fulham_FC_%28shield%29.svg/330px-Fulham_FC_%28shield%29.svg.png",
    "Brentford": "https://upload.wikimedia.org/wikipedia/uk/thumb/d/d0/Brentford_Logo.svg/960px-Brentford_Logo.svg.png",
    "Crystal Palace": "https://upload.wikimedia.org/wikipedia/sco/thumb/0/0c/Crystal_Palace_FC_logo.svg/500px-Crystal_Palace_FC_logo.svg.png",
    "Sunderland": "https://upload.wikimedia.org/wikipedia/sco/thumb/7/77/Logo_Sunderland.svg/3840px-Logo_Sunderland.svg.png",
    "Burnley": "https://upload.wikimedia.org/wikipedia/fr/thumb/0/02/Logo_Burnley_FC_2023.svg/1280px-Logo_Burnley_FC_2023.svg.png",
}

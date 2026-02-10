# config.py - Configuración global
import streamlit as st

def setup_page():
    """Configura CSS global"""
    st.markdown(
        """
    <style>
        .stApp {
            background: linear-gradient(180deg, #0f0c29, #302b63, #24243e);
            color: #fff;
        }

        /* =========================
        Contenedor principal (contenido)
        ========================= */
        main {
            padding: 20px 40px;
            background: transparent;  /* para que se vea el body/stApp */
        }
        
        h1, .stTitle h1 {
            font-family: "Courier New", monospace;
            font-size: 32px;
            font-weight: 800;
            color: #00ff99;             /* verde neón */
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 0 0 6px #00ff99;
        }
        
        /* Subtítulos */
        h2, h3, .stSubheader {
            font-family: "Courier New", monospace;
            font-weight: 700;
            color: #fff;
            margin-bottom: 12px;
        }
        /* Imagen principal */
        .stImage img {
            background: transparent !important;
            box-shadow: none !important;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,255,153,0.3);
            transition: all 0.4s ease-in-out;
        }
        
        .stImage img:hover {
            transform: scale(1.03);
            box-shadow: 0 0 30px rgba(0,255,153,0.6);
        }
        
        /* Grid de logos de equipos */
        .team-row {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            margin: 10px 20px;
            transition: all 0.3s ease-in-out;
        }

        .team-row img {
            width: 80px;
            height: 80px;
            object-fit: contain;
            border-radius: 8px;
            filter: drop-shadow(0 0 8px #00ff99);
            transition: all 0.3s ease-in-out;
        }

        .team-row img:hover {
            transform: scale(1.1);
            filter: drop-shadow(0 0 15px #00ff99);
        }
        
        .team-row span {
            margin-top: 6px;
            font-family: "Courier New", monospace;
            font-weight: 700;
            color: #00ff99;
            text-align: center;
        }

        
        /* Botones principales */
        div.stButton > button {
            background-color: #0f172a;    /* Azul principal */
            color: #00ff99;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px 0;
            margin: 8px 0;
            transition: all 0.3s ease-in-out;
        }
        
        div.stButton > button:hover {
            background-color: #0f172a;
            color: #00ff99;
            transform: translateY(-2px);
            box-shadow: 0 0 12px rgba(0,255,153,0.7);
            border-color: #00ff99;
        }

        .stInfo {
            background: rgba(0,255,150,0.1);
            border-left: 4px solid #00ff99;
            color: #00ff99;
            padding: 12px;
            border-radius: 10px;
            font-family: "Courier New", monospace;
        }

        .logo{
            border-radius: 0%;
        }
        .sub-header {
            text-align: center;
            color: #666;
            margin-bottom: 2.5rem;
            font-size: 1.3rem;
        }
        .stButton > button {
            font-weight: bold;
            font-size: 1.1rem;
        }
        .footer {
            text-align: center;
            color: #888;
            font-size: 0.9rem;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 2px solid #eee;
        }
            
        .team-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .team-row img {
            width: 50px;
            height: 50px;
            object-fit: contain;
            border-radius: 8px;
            transition: all 0.3s ease-in-out;
        }
        
        .team-row img:hover {
            transform: scale(1.1);
            filter: none;
        }
        .team-row span {
            font-weight: bold;
            font-size: 16px;
        }    
        

        section[data-testid="stSidebar"] img {
            display: block;
            margin: 0 auto; 
            opacity: 0.85;
            transition: all 0.4s ease;
            border-radius: 8px; 
            filter: brightness(1) drop-shadow(0 0 0px #00ff99);
        }

        section[data-testid="stSidebar"] img:hover {
            opacity: 1;
            transform: scale(1.05);
            filter: brightness(1.3) drop-shadow(0 0 15px #00ff99);
            box-shadow: 0 0 20px rgba(0, 255, 153, 0.6);
            animation: glow 1s ease-in-out infinite alternate;
        }
        
        @keyframes glow {
            from { filter: brightness(1.3) drop-shadow(0 0 10px #00ff99); }
            to { filter: brightness(1.5) drop-shadow(0 0 20px #00ff99); }
        }
        /* ===============================
        MENÚ MULTIPAGE STREAMLIT FIX
        ================================ */

        /* Contenedor */
        [data-testid="stSidebarNav"] {
            margin-top: 20px;
        }

        /* Cada item */
        [data-testid="stSidebarNav"] li {
            font-family: "Lucida Console", "Courier New", monospace;
            width: 100%;
        }


        /* Activo */
        /* Todos normales */
        [data-testid="stSidebarNav"] a {
            width: 100% !important;
            display: flex !important;
            align-items: center;

            padding: 12px 14px;
            border-radius: 14px;

            font-size: 16px;
            font-weight: 700;

            color: white !important;
            text-decoration: none !important;

            background: rgba(255,255,255,0.05);
            border-left: 4px solid transparent;

            transition: all 0.25s ease-in-out;
        }


        /* Hover */
        [data-testid="stSidebarNav"] a:hover {
            background: rgba(0,255,150,0.15);
            border-left: 4px solid #00ff99;
            transform: translateX(6px)
        }

        /* Activo */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(0,255,150,0.30);
            border-left: 4px solid #00ff99;
        }

        div[data-testid="stSidebarContent"] {
            background: linear-gradient(180deg, #2b004f, #0f172a) !important;
        }

        
        div[data-testid="stSidebarContent"] {
            background: linear-gradient(180deg, #2b004f, #0f172a) !important;
        }

        /* ===========================
        Sidebar Box y Títulos
        =========================== */

        /* Título principal de sidebar */
        .sidebar-title {
            font-size: 20px;
            font-family: "Lucida Console", "Courier New", monospace;
            font-weight: 700;
            color: #00ff99;          /* Verde neon tipo PL */
            text-align: center;
            margin-bottom: 20px;
        }

        /* Caja principal que contiene el contenido */
        .sidebar-box {
            background: rgba(255, 255, 255, 0.05);  /* fondo oscuro semi-transparente */
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 25px;
            border-left: 4px solid #00ff99;
            transition: all 0.3s ease-in-out;
        }

        /* Hover efecto en toda la caja */
        .sidebar-box:hover {
            background: rgba(0, 255, 150, 0.1);
            transform: translateY(-2px);
        }

        /* Subtítulos dentro de la caja */
        .sidebar-box h3 {
            font-size: 16px;
            font-family: "Courier New", monospace;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 10px;
        }

        /* Listas ordenadas */
        .sidebar-box ol,
        .sidebar-box ul {
            padding-left: 20px;
            color: #ddd;
            font-family: "Courier New", monospace;
            font-size: 15px;
        }

        /* Elementos de la lista */
        .sidebar-box li {
            margin-bottom: 6px;
        }

        /* Negrita dentro de listas */
        .sidebar-box b {
            color: #00ff99;
        }

        /* Ajuste general del sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a, #1e293b);
            padding: 25px;
        }

        /* Para hacer que los links del sidebar y cajas se vean uniformes */
        [data-testid="stSidebarContent"] {
            padding-top: 20px;
        }


        /* Contenedor del header */
        .header-container {
            display: flex;
            flex-direction: column;
            align-items: center;       /* centra horizontalmente */
            justify-content: center;
            margin-bottom: 30px;
            padding: 20px 0;
        }

        

        /* Imagen del logo del header */
        .header-container img {
            max-width: 90px;
            height: auto;
            border-radius: 8px;
            transition: all 0.4s ease;
            filter: brightness(1) drop-shadow(0 0 0px #00ff99);
        }
        
        /* Hover en la imagen: glow + zoom */
        .header-container img:hover {
            transform: scale(1.08);
            filter: brightness(1.3) drop-shadow(0 0 15px #00ff99);
            box-shadow: 0 0 25px rgba(0, 255, 153, 0.6);
            animation: glowHeader 1s ease-in-out infinite alternate;
        }

        /* Animación glow */
        @keyframes glowHeader {
            from { filter: brightness(1.3) drop-shadow(0 0 10px #00ff99); }
            to   { filter: brightness(1.5) drop-shadow(0 0 20px #00ff99); }
        }

        .header-container .sub-header {
            font-family: "Courier New", monospace;
            font-size: 16px;
            font-weight: 600;
            color: #00ff99;                  /* verde neón para resaltar */
            text-align: center;
            margin-top: 10px;
            text-shadow: 0 0 5px #00ff99;    /* resplandor leve del texto */
        }
        
        .header-container .sub-header.gradient {
            background: linear-gradient(90deg, #00ff99, #00ccff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .footer {
            text-align: center;
            color: #ccc;                   /* gris claro para no competir con el verde neón */
            font-size: 0.9rem;
            margin-top: 3rem;
            padding: 20px 15px 40px 15px;
            border-top: 2px solid rgba(0,255,153,0.3); /* línea superior verde neón suave */
            font-family: "Courier New", monospace;
            background: rgba(15,23,42,0.8); /* fondo semi-transparente oscuro */
            border-radius: 12px;
            transition: all 0.3s ease-in-out;
        }
        
        /* Hover opcional para resaltar el footer */
        .footer:hover {
            background: rgba(0,255,150,0.08);
        }

        /* Párrafos del footer */
        .footer p {
            margin: 4px 0;
            line-height: 1.4;
        }
        
        .footer p span,
        .footer p i {
            font-weight: bold;
            color: #00ff99; /* verde neón */
            text-shadow: 0 0 4px #00ff99;
        }


    </style>
    """,
        unsafe_allow_html=True,
    )

# Definir imágenes globales
IMAGES = {
    "premier_banner": "https://m.media-amazon.com/images/M/MV5BMjA0ZGI1MDQtOGNmMi00MTkxLWFkNGUtOTJiYTVlOGVlNjhmXkEyXkFqcGc@._V1_.jpg",
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
    "Aston Villa": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg",
    "Leicester City": "https://upload.wikimedia.org/wikipedia/en/6/63/Leicester_City_Seal.svg",
    "Leeds United": "https://upload.wikimedia.org/wikipedia/en/0/0c/Leeds_United_F.C._logo.svg",
    "Southampton": "https://upload.wikimedia.org/wikipedia/en/c/c9/FC_Southampton.svg",
    "Wolverhampton Wanderers": "https://upload.wikimedia.org/wikipedia/en/f/fc/Wolverhampton_Wanderers.svg",
    "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/6/6b/Nottingham_Forest_logo.svg",
    "Bournemouth": "https://upload.wikimedia.org/wikipedia/en/5/5c/AFC_Bournemouth_logo.svg",
    "Fulham": "https://upload.wikimedia.org/wikipedia/en/e/e6/Fulham_FC_%28shield%29.svg",
    "Brentford": "https://upload.wikimedia.org/wikipedia/en/0/0b/Brentford_FC_crest.svg",
    "Crystal Palace": "https://upload.wikimedia.org/wikipedia/en/0/0c/Crystal_Palace_FC_logo.svg",
}

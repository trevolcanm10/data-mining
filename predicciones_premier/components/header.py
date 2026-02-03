# components/header.py
import streamlit as st
import streamlit.components.v1 as components
def show_header():
    """
    Muestra el header principal con título, subtítulo y navegación
    """
    # CSS para el header
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 900;
        letter-spacing: -1px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2.5rem;
        font-size: 1.3rem;
        font-weight: 400;
    }
    
    .tag-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    
    .tag {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #444;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .nav-tabs {
        display: flex;
        justify-content: center;
        gap: 0;
        margin-bottom: 2rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .nav-tab {
        padding: 12px 24px;
        background: none;
        border: none;
        color: #666;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border-bottom: 3px solid transparent;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .nav-tab:hover {
        color: #FF4B4B;
        background-color: rgba(255, 75, 75, 0.05);
    }
    
    .nav-tab.active {
        color: #FF4B4B;
        border-bottom: 3px solid #FF4B4B;
        font-weight: 700;
    }
    
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 2px;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .sub-header {
            font-size: 1.1rem;
        }
        
        .stats-bar {
            flex-direction: column;
            gap: 15px;
        }
        
        .nav-tabs {
            flex-wrap: wrap;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.markdown('<h1 class="main-header">⚽ PREDICTOR PREMIER LEAGUE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">IA + Estadísticas Avanzadas • 100% GRATIS • Sin Registro</p>', unsafe_allow_html=True)
    
    # Tags de características
    st.markdown("""
    <div class="tag-container">
        <div class="tag">🤖 IA Avanzada</div>
        <div class="tag">📊 xG + npxG</div>
        <div class="tag">🎯 67% Precisión</div>
        <div class="tag">⚡ Tiempo Real</div>
        <div class="tag">🔒 100% Gratis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de estadísticas (simuladas - puedes hacerlas dinámicas)
    show_stats_bar()
    
    # Navegación con tabs (alternativa a sidebar)
    show_navigation()

def show_stats_bar():
    """
    Muestra barra de estadísticas destacadas
    """
    # Estas podrían ser estadísticas reales de tu predictor
    stats = [
        {"value": "67%", "label": "Precisión"},
        {"value": "1,240", "label": "Partidos"},
        {"value": "+12.5%", "label": "Valor (EV)"},
        {"value": "24/7", "label": "Actualizado"}
    ]
    
    stats_html = '<div class="stats-bar">'
    for stat in stats:
        stats_html += f'''
        <div class="stat-item">
            <div class="stat-value">{stat['value']}</div>
            <div class="stat-label">{stat['label']}</div>
        </div>
        '''
    stats_html += '</div>'
    
    components.html(stats_html, height=140)

def show_navigation():
    """
    Muestra navegación horizontal (opcional, complementa sidebar)
    """
    # Obtener página actual
    query_params = st.query_params
    current_page = query_params.get("page", ["predict"])[0]
    
    nav_items = [
        {"icon": "🎯", "label": "Predictor", "page": "predict", "key": "predict"},
        {"icon": "📅", "label": "Próximos", "page": "fixtures", "key": "fixtures"},
        {"icon": "📊", "label": "Estadísticas", "page": "stats", "key": "stats"}
    ]
    
    # Crear HTML de navegación
    nav_html = '<div class="nav-tabs">'
    
    for item in nav_items:
        is_active = current_page == item["page"]
        active_class = "active" if is_active else ""
        
        # Crear link que cambia parámetro de URL
        nav_html += f'''
        <a href="?page={item['page']}" class="nav-tab {active_class}">
            {item['icon']} {item['label']}
        </a>
        '''
    
    nav_html += '</div>'
    
    components.html(nav_html, height=80)
    # Manejar cambio de página (opcional, Streamlit ya maneja las páginas automáticamente)
    # Esta es solo para mostrar navegación visual

def show_alert_banner():
    """
    Muestra banner de alerta/noticia importante
    """
    # Solo mostrar en ciertas condiciones
    import datetime
    
    today = datetime.datetime.now()
    
    # Ejemplo: Mostrar banner los fines de semana
    if today.weekday() >= 5:  # Sábado (5) o Domingo (6)
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            padding: 12px;
            border-radius: 10px;
            margin: 15px 0;
            text-align: center;
            color: #333;
            font-weight: 600;
            box-shadow: 0 3px 10px rgba(255, 165, 0, 0.2);
            border-left: 5px solid #FF8C00;
        '>
        🚨 FIN DE SEMANA ACTIVO - Más partidos disponibles para predicción
        </div>
        """, unsafe_allow_html=True)


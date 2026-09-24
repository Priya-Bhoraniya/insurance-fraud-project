import streamlit as st
from streamlit_option_menu import option_menu

def top_navbar(current_page):
    """
    Renders a stunning horizontal navbar at the top of the page,
    and completely hides the default Streamlit sidebar.
    """
    st.markdown("""
    <style>
        /* Hide the default sidebar and its toggle button */
        [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        /* Add some padding to the top */
        .block-container { padding-top: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)
    
    pages = [
        "Home", "Dashboard", "Prediction", "Performance", 
        "Designer", "Analytics", "Cases", "Health", "About", "Contact"
    ]
    page_files = {
        "Home": "app.py",
        "Dashboard": "pages/0_Executive_Dashboard.py",
        "Prediction": "pages/1_Fraud_Prediction.py",
        "Performance": "pages/2_Model_Performance.py",
        "Designer": "pages/5_Model_Designer.py",
        "Analytics": "pages/6_Insurance_Analytics.py",
        "Cases": "pages/7_Case_Management.py",
        "Health": "pages/8_System_Health.py",
        "About": "pages/3_About.py",
        "Contact": "pages/4_Contact.py"
    }
    
    try:
        default_idx = pages.index(current_page)
    except ValueError:
        default_idx = 0
        
    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=["house", "bar-chart", "shield-lock", "graph-up", "cpu", "pie-chart", "briefcase", "heart-pulse", "info-circle", "envelope"],
        menu_icon="cast",
        default_index=default_idx,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "5px !important", 
                "background-color": "rgba(10, 10, 15, 0.7)", 
                "border-radius": "20px", 
                "border": "1px solid rgba(255,255,255,0.1)", 
                "margin-bottom": "2rem", 
                "backdrop-filter": "blur(20px)",
                "box-shadow": "0 10px 30px rgba(0,0,0,0.5)"
            },
            "icon": {"color": "#00f2fe", "font-size": "18px"},
            "nav-link": {
                "font-family": "'Outfit', sans-serif", 
                "font-size": "15px", 
                "font-weight": "600",
                "text-align": "center", 
                "margin": "0px 5px", 
                "--hover-color": "rgba(255,255,255,0.1)", 
                "color": "#d1d1e0",
                "border-radius": "15px"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, rgba(245, 87, 108, 0.2), rgba(240, 147, 251, 0.2))", 
                "color": "#ffffff", 
                "border": "1px solid rgba(240, 147, 251, 0.5)",
                "box-shadow": "0 0 15px rgba(240, 147, 251, 0.3)"
            },
        }
    )
    
    if selected != current_page:
        st.switch_page(page_files[selected])


def inject_custom_css():
    """
    Injects a jaw-dropping, mind-blowing Neo-Glassmorphism CSS.
    Features: 
    - Animated flowing gradient background
    - Animated gradient text for headings
    - Spinning glowing borders on cards
    - Liquid shiny buttons with pulsing glow
    - 3D tilt effects on cards
    """
    custom_css = """
    <style>
        /* Import High-Tech Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@300;400;600;800&display=swap');

        /* Global Styling */
        html, body, [class*="css"], p, span, li, label, div {
            font-family: 'Inter', sans-serif;
        }

        /* --------------------------------------
           MIND-BLOWING ANIMATED BACKGROUND 
           -------------------------------------- */
        @keyframes liquidBg {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(-45deg, #050505, #130022, #001220, #1b0024, #050505);
            background-size: 400% 400%;
            animation: liquidBg 15s ease infinite;
            color: #FFFFFF !important;
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 10px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { 
            background: linear-gradient(180deg, #00f2fe, #4facfe, #f093fb, #f5576c); 
            border-radius: 10px; 
        }

        /* Hide Streamlit Elements */
        header[data-testid="stHeader"] { background-color: transparent !important; }
        footer { display: none !important; }

        /* --------------------------------------
           TYPOGRAPHY - ANIMATED GRADIENTS
           -------------------------------------- */
        @keyframes textGlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
        }

        h1 {
            font-weight: 800 !important;
            font-size: 3.5rem !important;
            background: linear-gradient(270deg, #00f2fe, #4facfe, #f093fb, #f5576c, #00f2fe);
            background-size: 200% 200%;
            animation: textGlow 5s ease infinite;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0px 5px 25px rgba(240, 147, 251, 0.4);
            margin-bottom: 2rem !important;
            text-align: center;
        }

        h2, h3 {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.2);
            letter-spacing: 1px;
        }

        p, span, li, label {
            color: #d1d1e0 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }

        /* --------------------------------------
           METRIC CARDS - SPINNING GLOW BORDERS
           -------------------------------------- */
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            font-family: 'Outfit', sans-serif !important;
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        
        div[data-testid="metric-container"] {
            background: rgba(20, 20, 30, 0.6) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            backdrop-filter: blur(15px) !important;
            position: relative;
            z-index: 1;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.05) !important;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        }
        
        /* The spinning gradient border effect */
        @keyframes spin { 100% { transform: rotate(360deg); } }
        
        div[data-testid="metric-container"]::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%; width: 200%; height: 200%;
            background: conic-gradient(from 0deg, transparent 0%, transparent 80%, #00f2fe 90%, #f093fb 100%);
            animation: spin 4s linear infinite;
            z-index: -2;
            opacity: 0;
            transition: opacity 0.4s ease;
        }
        div[data-testid="metric-container"]::after {
            content: '';
            position: absolute;
            inset: 2px;
            background: rgba(15, 15, 25, 0.9);
            border-radius: 18px;
            z-index: -1;
        }
        
        div[data-testid="metric-container"]:hover::before { opacity: 1; }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-5px) scale(1.02) !important;
            box-shadow: 0 20px 40px rgba(0, 242, 254, 0.2), 0 0 20px rgba(240, 147, 251, 0.2) !important;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem !important;
            color: #8b8b9b !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Inter', sans-serif !important;
        }

        /* --------------------------------------
           INPUTS - GLOWING NEON
           -------------------------------------- */
        .stNumberInput input, .stTextInput input, .stSelectbox select {
            background-color: rgba(10, 10, 20, 0.8) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            padding: 0.8rem 1rem !important;
            font-size: 1rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.5) !important;
        }
        .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
            border-color: #00f2fe !important;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.5), inset 0 2px 5px rgba(0,0,0,0.5) !important;
            background-color: rgba(20, 20, 40, 0.9) !important;
            outline: none !important;
        }

        /* --------------------------------------
           BUTTONS - LIQUID ENERGY
           -------------------------------------- */
        @keyframes pulseGlow {
            0% { box-shadow: 0 0 15px rgba(245, 87, 108, 0.4); }
            50% { box-shadow: 0 0 30px rgba(240, 147, 251, 0.8); }
            100% { box-shadow: 0 0 15px rgba(245, 87, 108, 0.4); }
        }

        div.stButton > button[kind="primary"] {
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 1rem 2.5rem !important;
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            font-family: 'Outfit', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            width: 100% !important;
            animation: pulseGlow 2s infinite;
        }
        div.stButton > button[kind="primary"]:hover {
            transform: scale(1.03) translateY(-3px);
            background: linear-gradient(45deg, #f5576c 0%, #f093fb 100%) !important;
            animation: none;
            box-shadow: 0 15px 40px rgba(240, 147, 251, 0.7) !important;
        }
        
        div.stButton > button:not([kind="primary"]) {
            background: rgba(30, 30, 45, 0.5) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 50px !important;
            padding: 0.8rem 2rem !important;
            font-weight: 600 !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:not([kind="primary"]):hover {
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4) !important;
            transform: translateY(-2px);
        }

        /* --------------------------------------
           DATAFRAMES - CYBER TABLES
           -------------------------------------- */
        [data-testid="stDataFrame"] {
            border-radius: 15px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            background: rgba(10, 10, 15, 0.6) !important;
            backdrop-filter: blur(15px) !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        }
        [data-testid="stDataFrame"] th {
            background: rgba(0, 242, 254, 0.1) !important;
            color: #00f2fe !important;
            font-weight: 700 !important;
            border-bottom: 1px solid rgba(0, 242, 254, 0.3) !important;
            padding: 1rem !important;
            font-family: 'Outfit', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        [data-testid="stDataFrame"] td {
            background-color: transparent !important;
            color: #e0e0e0 !important;
            border-bottom: 1px solid rgba(255,255,255,0.05) !important;
            padding: 0.8rem !important;
        }

        /* --------------------------------------
           ALERTS & EXPANDERS
           -------------------------------------- */
        .stAlert {
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            padding: 1.2rem !important;
            background: rgba(20, 20, 30, 0.6) !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3) !important;
        }
        .st-ae[data-baseweb="notification"] { border-left: 4px solid #f5576c !important; }
        .st-af[data-baseweb="notification"] { border-left: 4px solid #f093fb !important; }
        .st-ag[data-baseweb="notification"] { border-left: 4px solid #00f2fe !important; }

        .streamlit-expanderHeader {
            background: rgba(20, 20, 30, 0.6) !important;
            border-radius: 10px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 1rem 1.2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #FFFFFF !important;
            backdrop-filter: blur(10px) !important;
            transition: all 0.3s ease !important;
        }
        .streamlit-expanderHeader:hover {
            background: rgba(40, 40, 60, 0.8) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3) !important;
        }
        
        hr {
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin: 2.5rem 0 !important;
        }
        
        /* --------------------------------------
           PROGRESS BAR - LIQUID GRADIENT
           -------------------------------------- */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #00f2fe, #f093fb) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 15px rgba(240, 147, 251, 0.5) !important;
        }
        
        /* --------------------------------------
           ENTRANCE ANIMATIONS
           -------------------------------------- */
        .element-container {
            animation: zoomIn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
            opacity: 0;
            transform: scale(0.98);
        }
        @keyframes zoomIn {
            to { opacity: 1; transform: scale(1); }
        }
        .element-container:nth-child(1) { animation-delay: 0.1s; }
        .element-container:nth-child(2) { animation-delay: 0.15s; }
        .element-container:nth-child(3) { animation-delay: 0.2s; }
        .element-container:nth-child(4) { animation-delay: 0.25s; }
        .element-container:nth-child(5) { animation-delay: 0.3s; }
        .element-container:nth-child(6) { animation-delay: 0.35s; }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

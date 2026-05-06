import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');

        :root {
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --accent-color: #00D1FF;
            --accent-glow: rgba(0, 209, 255, 0.3);
            --text-main: #E2E8F0;
            --text-bright: #FFFFFF;
            --sidebar-bg: #05060B;
            --card-bg: rgba(255, 255, 255, 0.03);
        }

        .stApp {
            background: linear-gradient(135deg, #0F172A 0%, #020617 100%);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        /* --- CRITICAL READABILITY FIXES --- */
        /* Ensure all standard markdown text is bright white */
        .stMarkdown div, .stMarkdown p, .stMarkdown span, .stMarkdown label, .stMarkdown li {
            color: #FFFFFF !important;
        }
        
        /* Fix for Streamlit's new status and info components which might have dark text */
        [data-testid="stStatusWidget"], [data-testid="stAlert"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }
        [data-testid="stStatusWidget"] p, [data-testid="stAlert"] p {
            color: white !important;
        }

        /* Code and Preformatted text */
        code {
            color: #FF79C6 !important; /* Drac-style pink for contrast */
            background: rgba(0,0,0,0.3) !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
        }
        pre {
            background: rgba(0,0,0,0.4) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
        }

        h1, h2, h3, h4 {
            font-family: 'Outfit', sans-serif !important;
            color: var(--text-bright) !important;
            letter-spacing: -0.02em;
            font-weight: 700 !important;
        }

        /* --- COMPONENTS --- */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
            transition: all 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
        }

        .glass-card:hover {
            transform: translateY(-2px);
            border-color: var(--accent-color);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 15px 50px -5px var(--accent-glow);
        }

        .stButton>button {
            background: linear-gradient(90deg, #00D1FF 0%, #0077FF 100%);
            color: white !important;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 1.5rem;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px -5px var(--accent-glow);
            filter: brightness(1.1);
        }

        /* Chat interface adjustments */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.04) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            margin-bottom: 24px !important;
            color: white !important;
        }

        .stChatMessage p {
            color: #FFFFFF !important;
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
        }

        /* --- SIDEBAR & HEADER --- */
        [data-testid="stSidebar"] {
            background-color: var(--sidebar-bg) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        [data-testid="stSidebar"] h2 {
            font-size: 1.4rem !important;
            background: linear-gradient(90deg, #FFFFFF, var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Force Sidebar Toggle to be visible and glowing */
        [data-testid="stSidebarCollapseButton"] {
            color: var(--accent-color) !important;
            background: rgba(0, 209, 255, 0.1) !important;
            border: 1px solid var(--accent-glow) !important;
            border-radius: 50% !important;
            padding: 5px !important;
            box-shadow: 0 0 10px var(--accent-glow) !important;
            transition: all 0.3s ease;
        }
        [data-testid="stSidebarCollapseButton"]:hover {
            background: rgba(0, 209, 255, 0.2) !important;
            transform: scale(1.1);
        }

        /* --- VISUALIZATIONS --- */
        .timeline-container {
            border-left: 1px solid rgba(0, 209, 255, 0.3);
            margin-left: 20px;
            padding-left: 30px;
            position: relative;
        }
        .timeline-item {
            position: relative;
            margin-bottom: 2rem;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -36px;
            top: 15px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-color);
            box-shadow: 0 0 15px var(--accent-color);
            z-index: 2;
        }
        .source-tag {
            font-size: 0.6rem;
            padding: 3px 10px;
            border-radius: 4px;
            background: rgba(0, 209, 255, 0.1);
            color: var(--accent-color) !important;
            border: 1px solid var(--accent-glow);
            letter-spacing: 0.5px;
        }

        /* Voice Assistant Pulse */
        .voice-pulse {
            width: 90px;
            height: 90px;
            background: radial-gradient(circle, var(--accent-color) 0%, #0077FF 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 30px auto;
            animation: pulse 2s infinite;
            box-shadow: 0 0 0 0 rgba(0, 209, 255, 0.4);
            font-size: 2rem;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 209, 255, 0.4); }
            70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(0, 209, 255, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 209, 255, 0); }
        }

        /* Status Indicator */
        .neural-status {
            padding: 10px 15px;
            border-radius: 12px;
            background: rgba(0, 209, 255, 0.05);
            border: 1px solid rgba(0, 209, 255, 0.1);
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 10px 0;
        }
        .neural-dot {
            width: 6px;
            height: 6px;
            background: var(--accent-color);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent-color);
            animation: blink 1.5s infinite;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; filter: brightness(1.2); }
            50% { opacity: 0.4; filter: brightness(0.8); }
        }

        /* Hide UI cruft */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header { background-color: transparent !important; }
        
        .stTabs [data-baseweb="tab-list"] {
            padding: 10px 0;
        }
        .stTabs [data-baseweb="tab"] {
            color: #64748B !important;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            color: var(--accent-color) !important;
        }

        /* --- HUD ELEMENTS --- */
        .hud-container {
            position: relative;
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid var(--accent-glow);
            border-radius: 20px;
            padding: 40px;
            overflow: hidden;
            box-shadow: inset 0 0 50px rgba(0, 209, 255, 0.1);
        }
        .hud-scanline {
            width: 100%;
            height: 100px;
            z-index: 3;
            background: linear-gradient(0deg, rgba(0, 0, 0, 0) 0%, rgba(0, 209, 255, 0.05) 50%, rgba(0, 0, 0, 0) 100%);
            opacity: 0.1;
            position: absolute;
            bottom: 100%;
            animation: scanline 6s linear infinite;
        }
        @keyframes scanline {
            0% { bottom: 100%; }
            100% { bottom: -100px; }
        }
        .hud-corner {
            position: absolute;
            width: 30px;
            height: 30px;
            border-color: var(--accent-color);
            border-style: solid;
            opacity: 0.5;
        }
        .hud-tl { top: 15px; left: 15px; border-width: 3px 0 0 3px; }
        .hud-tr { top: 15px; right: 15px; border-width: 3px 3px 0 0; }
        .hud-bl { bottom: 15px; left: 15px; border-width: 0 0 3px 3px; }
        .hud-br { bottom: 15px; right: 15px; border-width: 0 3px 3px 0; }
        
        .hud-data-row {
            display: flex;
            justify-content: space-between;
            font-family: 'Courier New', monospace;
            font-size: 0.7rem;
            color: var(--accent-color);
            margin-bottom: 5px;
            opacity: 0.6;
        }

        .hud-response {
            background: rgba(0, 209, 255, 0.05);
            border-left: 3px solid var(--accent-color);
            padding: 15px;
            margin-top: 20px;
            animation: fadeIn 0.5s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Floating "Open Sidebar" prompt when collapsed */
        .collapsed-info {
            position: fixed;
            top: 10px;
            left: 50px;
            font-size: 0.7rem;
            color: var(--accent-color);
            opacity: 0.6;
            z-index: 1000;
        }
        </style>
    """, unsafe_allow_html=True)

import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');

        :root {
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --accent-color: #7B61FF;
            --accent-glow: rgba(123, 97, 255, 0.4);
            --text-main: #E0E0E0;
            --text-bright: #FFFFFF;
        }

        .stApp {
            background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            color: var(--text-bright) !important;
            letter-spacing: -0.02em;
        }

        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: fadeIn 0.8s ease-out;
        }

        .glass-card:hover {
            transform: translateY(-5px) scale(1.01);
            border-color: var(--accent-color);
            box-shadow: 0 12px 40px 0 var(--accent-glow);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stButton>button {
            background: linear-gradient(135deg, var(--accent-color) 0%, #4E31AA 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 0.7rem 2rem;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px var(--accent-glow);
            width: 100%;
        }

        .stButton>button:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 25px var(--accent-glow);
            color: white;
        }

        .memory-metadata {
            color: var(--accent-color);
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.5rem;
            display: block;
        }

        /* Chat interface adjustments */
        .stChatMessage {
            background: rgba(255, 255, 255, 0.07) !important;
            border-radius: 18px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            margin-bottom: 15px !important;
            color: #FFFFFF !important;
        }

        /* Ensure all text within chat is white and readable */
        .stChatMessage p, .stChatMessage span, .stChatMessage div {
            color: #FFFFFF !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 20, 0.95) !important;
            backdrop-filter: blur(25px);
            border-right: 1px solid var(--glass-border);
        }

        /* Better Sidebar Text */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #FFFFFF !important;
        }

        /* Refined Sidebar Toggle Visibility */
        button[kind="header"] {
            background-color: transparent !important;
            color: white !important;
        }

        /* Hide Streamlit Footer but keep Header for sidebar toggle */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Ensure the header is visible but transparent so the sidebar toggle shows */
        header {
            background-color: transparent !important;
        }

        /* Timeline / Action Logger Styling */
        .timeline-container {
            border-left: 2px solid var(--accent-color);
            margin-left: 20px;
            padding-left: 20px;
        }
        .timeline-item {
            position: relative;
            margin-bottom: 2rem;
        }
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -31px;
            top: 5px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--accent-color);
            box-shadow: 0 0 10px var(--accent-glow);
        }
        .source-tag {
            font-size: 0.65rem;
            padding: 2px 8px;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.1);
            margin-left: 10px;
            vertical-align: middle;
        }

        /* Voice Assistant Pulse */
        .voice-pulse {
            width: 80px;
            height: 80px;
            background: var(--accent-color);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px auto;
            animation: pulse 2s infinite;
            box-shadow: 0 0 0 0 rgba(123, 97, 255, 0.7);
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(123, 97, 255, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(123, 97, 255, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(123, 97, 255, 0); }
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0,0,0,0.1);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--glass-border);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-color);
        }
        </style>
    """, unsafe_allow_html=True)

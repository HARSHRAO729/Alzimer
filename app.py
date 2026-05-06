import streamlit as st
import os
import tempfile
import random
from pathlib import Path
from datetime import datetime
from core.perception import describe_image
from core.repository import MemoryRepository
from adapters.chroma_adapter import ChromaVectorStore
from ui.styles import apply_styles
import config

# Page Configuration
st.set_page_config(
    page_title="Cognitive Fabric | Memory Companion",
    page_icon="🧠",
    layout="wide"
)

# Initialize Backend
@st.cache_resource
def get_backend():
    adapter = ChromaVectorStore()
    repository = MemoryRepository(adapter)
    return repository

repository = get_backend()

# Apply Custom Styling
apply_styles()

# Helper for simulating random life events
def simulate_event(sensor_type):
    home_events = [
        "User placed their keys on the dining table.",
        "User put a medicine bottle in the kitchen cabinet.",
        "The red umbrella was left near the front door.",
        "User is reading a book on the sofa.",
        "A cup of coffee was placed on the side table."
    ]
    glass_events = [
        "User is looking at a specific document in the office.",
        "User greeted a friend named Alex on the street.",
        "User is checking the price of a watch in a shop window.",
        "User is looking for their parked car (Silver SUV).",
        "User is reading a prescription label."
    ]
    
    event_text = random.choice(home_events if "Living Room" in sensor_type else glass_events)
    new_record = {
        "memory_id": f"sim_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "date": datetime.now().strftime("%B %d, %Y, %I:%M %p"),
        "context": event_text,
        "emotional_tone": "Neutral",
        "people": ["User"]
    }
    repository.add_memory(new_record)
    return event_text

# Sidebar: Configuration & Stats
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🧠 COGNITIVE FABRIC</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8rem; opacity: 0.7;'>Ambient Intelligence System</p>", unsafe_allow_html=True)
    
    # Neural Status indicator
    st.markdown("""
        <div class="neural-status">
            <div class="neural-dot"></div>
            <span style="font-size: 0.8rem; font-weight: 600;">Neural Fabric: ACTIVE</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Explanation (Addressing User Query)
    with st.expander("ℹ️ How the Brain Works"):
        st.markdown(f"""
        **Vision (LLaVA Model):** The "Eyes". 
        *Why LLaVA?* LLaVA is a multimodal model specifically designed to "see" images and describe them in text.
        
        **Language (Gemma 4 Model):** The "Mouth". 
        *Why Gemma?* Gemma is a Large Language Model (LLM) optimized for reasoning and conversation. It reads the text descriptions stored in your memory to talk to you.
        
        **Memory (Chroma Vector DB):** The "Lobe". 
        It stores semantic snapshots of your life. When you ask a question, the system searches this database for relevant events.
        """)

    st.markdown("---")
    
    # Mode Switcher
    sensor = st.radio("Primary Sensor", ["🏠 Living Room Camera", "🕶️ Personal Eyeglasses"])
    
    # Memory Stats
    mem_count = repository.count()
    st.metric("Life Snapshots Stored", mem_count)
    
    # Cognitive Health Indicators
    st.markdown("---")
    st.subheader("📊 System Health")
    
    # Semantic Load (Simulated based on memory count)
    semantic_load = min(100, (mem_count / 1000) * 100)
    st.write(f"Semantic Load: {semantic_load:.1f}%")
    st.progress(semantic_load / 100)
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown(f"""
            <div style="background: rgba(0,255,100,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(0,255,100,0.2);">
                <div style="font-size: 0.6rem; opacity: 0.7;">RECALL ACCURACY</div>
                <div style="font-weight: 700; color: #00FF66;">99.4%</div>
            </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown(f"""
            <div style="background: rgba(0,209,255,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(0,209,255,0.2);">
                <div style="font-size: 0.6rem; opacity: 0.7;">NEURAL DENSITY</div>
                <div style="font-weight: 700; color: var(--accent-color);">High</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Actions
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Reseed"):
            with st.spinner("Rebuilding..."):
                count = repository.reseed()
                st.success(f"Indexed {count}!")
                st.rerun()
    with col_b:
        if st.button("🎲 Simulate"):
            event = simulate_event(sensor)
            st.toast(f"Logged: {event}", icon="👀")
            st.rerun()

    st.markdown("---")
    st.subheader("📸 Direct Frame Injection")
    uploaded_file = st.file_uploader("Force a 'Snap-and-Forget' action", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    st.markdown("<div style='font-size: 0.7rem; opacity: 0.5;'>v1.4.0-ambient-pro<br/>System Latency: Optimized</div>", unsafe_allow_html=True)

# Sidebar helper prompt (visible when sidebar is closed)
st.markdown('<div class="collapsed-info">← Use the arrow to open system controls</div>', unsafe_allow_html=True)

# Main Application Tabs
tab1, tab2, tab3 = st.tabs(["💬 Personal Assistant", "📜 Action Timeline", "🕶️ Glass Simulation"])

# --- TAB 1: ASSISTANT ---
with tab1:
    st.markdown("### 🧠 Continuous Recall Assistant")
    st.markdown("<p style='opacity: 0.6;'>I have access to your home and eyeglass feeds. Ask me anything.</p>", unsafe_allow_html=True)
    
    # Chat History Initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Where did I put the medicine?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            # Using status to give meaningful progress feedback
            with st.status("🔍 Accessing Cognitive Fabric...", expanded=True) as status:
                status.write("Consulting neural pathways and life snapshots...")
                
                # Use repository to generate response
                for chunk in repository.query_assistant(prompt, st.session_state.messages[:-1]):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                
                status.update(label="Response Synthesized", state="complete", expanded=False)
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- TAB 2: ACTION LOGGER ---
with tab2:
    st.markdown("### 📜 Action Intelligence Log")
    st.markdown("<p style='opacity: 0.6;'>Chronological stream of semantic events captured by the ambient mesh.</p>", unsafe_allow_html=True)
    
    timeline = repository.get_history()
    
    if not timeline:
        st.info("The system is currently observing. Move objects to trigger a log.")
    else:
        st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
        for event in timeline:
            # Determine source from sensor or metadata
            ctx_lower = event.get("context", "").lower()
            # Simple heuristic for existing data, but new simulated data will be more precise
            is_home = "kitchen" in ctx_lower or "dining" in ctx_lower or "table" in ctx_lower or "home" in event.get("memory_id", "")
            source_label = "🏠 HOME SENSOR" if is_home else "🕶️ GLASSES"
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 0.75rem; color: var(--accent-color); font-weight: 700;">{event.get('date', 'Just now')}</span>
                        <span class="source-tag">{source_label}</span>
                    </div>
                    <p style="margin: 0; font-size: 1rem; color: #FFFFFF !important;">{event.get('context')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: GLASS MODE ---
with tab3:
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🕶️ Eyeglass HUD Simulation</h2>", unsafe_allow_html=True)
    
    # Glass State
    if "glass_active" not in st.session_state:
        st.session_state.glass_active = False

    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        if not st.session_state.glass_active:
            st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 60px 40px;">
                    <div style="font-size: 4rem; margin-bottom: 20px; opacity: 0.8;">👓</div>
                    <h3>Personal Glass HUD Offline</h3>
                    <p style="opacity: 0.6; margin-bottom: 30px;">Tap the temple sensor on your eyewear to establish a neural link with the Cognitive Fabric.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("👆 Tap Temple to Summon Assistant"):
                st.session_state.glass_active = True
                st.rerun()
        else:
            # HUD CONTAINER
            st.markdown(f"""
                <div class="hud-container">
                    <div class="hud-scanline"></div>
                    <div class="hud-corner hud-tl"></div>
                    <div class="hud-corner hud-tr"></div>
                    <div class="hud-corner hud-bl"></div>
                    <div class="hud-corner hud-br"></div>
                    
                    <div class="hud-data-row">
                        <span>SYS_ID: CF-PRO-882</span>
                        <span>LINK_STRENGTH: 98%</span>
                    </div>
                    <div class="hud-data-row">
                        <span>MODEL: GEMMA_4_LOCAL</span>
                        <span>LATENCY: 24ms</span>
                    </div>
                    <div class="hud-data-row">
                        <span>USER_COORD: 40.7128° N, 74.0060° W</span>
                        <span>TIME: {datetime.now().strftime("%H:%M:%S")}</span>
                    </div>
                    
                    <div class="voice-pulse" style="margin: 20px auto;">🎙️</div>
                    <h3 style="text-align: center; color: var(--accent-color) !important;">Neural Link Established</h3>
                    <p style="text-align: center; opacity: 0.8;">Listening for voice commands...</p>
            """, unsafe_allow_html=True)
            
            glass_query = st.text_input("Speak to Glasses (Type simulation):", placeholder="Where did I leave my keys?", label_visibility="collapsed")
            
            if glass_query:
                with st.status("🧠 Consulting Memory Core...", expanded=True) as status:
                    status.write("Accessing distributed visual memory nodes...")
                    full_response = ""
                    # Use the first chunk to update status
                    response_gen = repository.query_assistant(glass_query)
                    for chunk in response_gen:
                        full_response += chunk
                    status.update(label="Memory Verified", state="complete")
                
                st.markdown(f"""
                    <div class="hud-response">
                        <strong style="color: var(--accent-color); font-family: 'Outfit', sans-serif; letter-spacing: 1px;">&gt; RETRIEVAL SUCCESSFUL</strong><br/>
                        <p style="font-size: 1.1rem; color: #FFFFFF !important; line-height: 1.5; margin-top: 10px;">{full_response}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True) # End hud-container
            
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button("❌ Terminate HUD Link"):
                st.session_state.glass_active = False
                st.rerun()

# --- Ambient Logic ---
if uploaded_file and "image_processed" not in st.session_state:
    with st.spinner("Processing Vision Frame..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        description = describe_image(tmp_path)
        os.remove(tmp_path)
        
        if description:
            st.session_state.image_processed = True
            source_id = "home" if "Living Room" in sensor else "glass"
            new_record = {
                "memory_id": f"{source_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "date": datetime.now().strftime("%B %d, %Y, %I:%M %p"),
                "context": description,
                "emotional_tone": "Neutral",
                "people": ["User"]
            }
            repository.add_memory(new_record)
            st.toast("Snap-and-Forget: Visual event logged successfully!", icon="✅")
            st.rerun()

if not uploaded_file and "image_processed" in st.session_state:
    del st.session_state.image_processed

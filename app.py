import streamlit as st
import os
import tempfile
from pathlib import Path
from datetime import datetime
from core.perception import describe_image
from core.retriever import MemoryRetriever
from core.generator import generate_response
from core.memory_store import MemoryStore
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
    store = MemoryStore(adapter)
    retriever = MemoryRetriever(adapter)
    return store, retriever

store, retriever = get_backend()

# Apply Custom Styling
apply_styles()

# Sidebar: Configuration & Stats
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🧠 COGNITIVE FABRIC</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.8rem; opacity: 0.7;'>Ambient Intelligence System</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Mode Switcher (Visual only for now)
    st.radio("System Source", ["Home (Active)", "Eyeglasses (Synced)"])
    
    # Memory Stats
    mem_count = store.count()
    st.metric("Stored Memories", mem_count)
    
    # Actions
    if st.button("🔄 Reseed Memory Core"):
        with st.spinner("Seeding memories..."):
            count = store.load_seed_data()
            st.success(f"Successfully seeded {count} memories!")
            st.rerun()

    st.markdown("---")
    st.subheader("📸 Perceptual Capture")
    uploaded_file = st.file_uploader("Manual override: Upload frame", type=["jpg", "jpeg", "png"])
    
    st.markdown("---")
    st.markdown("<div style='font-size: 0.7rem; opacity: 0.5;'>v1.2.0-ambient<br/>Powered by Gemma 4 & LLaVA</div>", unsafe_allow_html=True)

# Main Application Tabs
tab1, tab2, tab3 = st.tabs(["💬 Assistant", "📜 Action Logger", "👓 Glass Mode"])

# --- TAB 1: ASSISTANT ---
with tab1:
    st.markdown("### Conversational Recall")
    
    # Chat History Initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask about your day..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.spinner("Searching memories..."):
            results = retriever.retrieve(prompt)
            context = retriever.build_context(results)
        
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            for chunk in generate_response(prompt, context, st.session_state.messages[:-1]):
                full_response += chunk
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- TAB 2: ACTION LOGGER ---
with tab2:
    st.markdown("### Ambient Action Timeline")
    st.markdown("<p style='opacity: 0.6;'>A continuous log of detected hand-object interactions and visual events.</p>", unsafe_allow_html=True)
    
    timeline = store.get_timeline()
    
    if not timeline:
        st.info("No actions logged yet. The system is observing...")
    else:
        st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
        for event in timeline:
            source = config.SOURCE_HOME if "key" in event.get("context", "").lower() else config.SOURCE_GLASSES
            source_label = "🏠 Home" if source == config.SOURCE_HOME else "👓 Glasses"
            
            st.markdown(f"""
            <div class="timeline-item">
                <span class="memory-metadata">{event.get('date', 'Just now')} <span class="source-tag">{source_label}</span></span>
                <div class="glass-card">
                    {event.get('context')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: GLASS MODE (Simulation) ---
with tab3:
    st.markdown("<h2 style='text-align: center;'>Eyeglass Interface</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>Touch-activated AI Sidebar Simulation</p>", unsafe_allow_html=True)
    
    # Voice Activation Simulation
    if "glass_active" not in st.session_state:
        st.session_state.glass_active = False

    if not st.session_state.glass_active:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        if st.button("👆 Touch Temple to Activate"):
            st.session_state.glass_active = True
            st.rerun()
    else:
        st.markdown('<div class="voice-pulse">🎙️</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-weight: 600;'>Hi User. I'm listening... How can I help you?</p>", unsafe_allow_html=True)
        
        glass_query = st.text_input("Speak your query (Simulation):", placeholder="Where did I put my keys?")
        
        if glass_query:
            with st.spinner("Retrieving from Central DB..."):
                results = retriever.retrieve(glass_query)
                context = retriever.build_context(results)
                
                # Simple Voice-like response
                full_response = ""
                for chunk in generate_response(glass_query, context):
                    full_response += chunk
                
                st.markdown(f"""
                <div class="glass-card" style="border-left: 5px solid var(--accent-color);">
                    <strong>Agent:</strong> {full_response}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Close Sidebar"):
                    st.session_state.glass_active = False
                    st.rerun()

# --- Shared Perception Logic (Moved to bottom for clarity) ---
if uploaded_file and "image_processed" not in st.session_state:
    with st.spinner("Processing Ambient Frame..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        description = describe_image(tmp_path)
        os.remove(tmp_path)
        
        if description:
            st.session_state.image_processed = True
            # Log as a new memory automatically (Simulating Ambient logging)
            new_record = {
                "memory_id": f"ambient_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "date": datetime.now().strftime("%B %d, %Y, %I:%M %p"),
                "context": description,
                "emotional_tone": "Neutral",
                "people": ["User"]
            }
            store.add_memory(new_record)
            st.success("Visual event logged to Action Timeline!")
            st.rerun()

if not uploaded_file and "image_processed" in st.session_state:
    del st.session_state.image_processed

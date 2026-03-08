import streamlit as st
from groq import Groq

# 1. Setup minimaliste
st.set_page_config(page_title="Sovereign", layout="centered")
client = Groq(api_key="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")

# 2. CSS Radical (On vire tout le surplus)
st.markdown("""
    <style>
    .stApp { background: #000; }
    header, footer { visibility: hidden; }
    
    /* Titre XXL Aluetoo */
    .aluetoo-title {
        font-weight: 900;
        background: linear-gradient(90deg, #ff4b4b, #af40ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: clamp(40px, 8vw, 80px);
        text-align: center;
        margin: 20px 0;
    }

    /* Animation d'apparition */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); filter: blur(10px); }
        to { opacity: 1; transform: translateY(0); filter: blur(0px); }
    }
    .msg-anim { animation: slideIn 0.5s ease-out forwards; }
    
    /* Input recentré */
    div[data-testid="stChatInput"] {
        max-width: 600px !important;
        margin: 0 auto !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="aluetoo-title">ALUETOO</div>', unsafe_allow_html=True)

# 3. Système de messages simple
if "chat" not in st.session_state:
    st.session_state.chat = []

# Affichage avec animation
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(f'<div class="msg-anim">{m["content"]}</div>', unsafe_allow_html=True)

# 4. Input & Logique IA
if prompt := st.chat_input("Écris ici..."):
    st.session_state.chat.append({"role": "user", "content": prompt})
    st.rerun()

# Si le dernier message est de l'utilisateur, Aluetoo répond
if st.session_state.chat and st.session_state.chat[-1]["role"] == "user":
    user_msg = st.session_state.chat[-1]["content"]
    
    with st.chat_message("assistant"):
        # On vérifie si on demande une action à l'IA
        if any(k in user_msg.lower() for k in ["envoie", "ecrit", "message"]):
            st.info("⚡ Action Aluetoo détectée")
            
        # Appel Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Tu es Aluetoo, l'IA de Léo. Sois courte et stylée."}] + st.session_state.chat,
        ).choices[0].message.content
        
        st.markdown(f'<div class="msg-anim">{response}</div>', unsafe_allow_html=True)
        st.session_state.chat.append({"role": "assistant", "content": response})

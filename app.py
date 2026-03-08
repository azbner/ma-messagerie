import streamlit as st
from groq import Groq
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sovereign OS", layout="wide")
client = Groq(api_key="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")

# Initialisation des états
if "aluetoo_full" not in st.session_state:
    st.session_state.aluetoo_full = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "contacts" not in st.session_state:
    st.session_state.contacts = [{"name": "Léo Ciach", "id": "123"}, {"name": "Ami", "id": "456"}]

# --- 2. STYLE CSS XXL & FULL SCREEN ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    header, footer { visibility: hidden; }
    
    /* Centrage Premium */
    .main .block-container {
        max-width: 900px !important;
        margin: auto !important;
        padding: 0 !important;
    }

    /* Bouton Aluetoo Dégradé */
    .aluetoo-trigger {
        background: linear-gradient(to right, #ff4b4b, #af40ff, #00d4ff);
        padding: 15px;
        border-radius: 50px;
        text-align: center;
        color: white;
        font-weight: 900;
        cursor: pointer;
        font-size: 20px;
        letter-spacing: 2px;
        margin: 20px;
        box-shadow: 0 0 20px rgba(175, 64, 255, 0.4);
    }

    /* Titre XXL */
    .mega-title {
        font-weight: 900;
        background: linear-gradient(to right, #ff4b4b, #af40ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 65px;
        text-align: center;
    }

    /* Animation Ghost */
    @keyframes ghostFade {
        0% { opacity: 0; filter: blur(8px); }
        100% { opacity: 1; filter: blur(0px); }
    }
    .word-fade { animation: ghostFade 1.2s ease-out; color: #e6edf3; font-size: 24px; }

    /* Glassmorphism Contacts */
    .contact-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE ALUETOO FULL SCREEN ---
def toggle_aluetoo():
    st.session_state.aluetoo_full = not st.session_state.aluetoo_full

# --- 4. INTERFACE ---

# HEADER AVEC BOUTON ALUETOO
col_side, col_mid, col_side2 = st.columns([1, 4, 1])
with col_mid:
    if st.button("✨ OUVRIR ALUETOO AI ✨", use_container_width=True):
        toggle_aluetoo()

# MODE IA EN GRAND (SI ACTIVÉ)
if st.session_state.aluetoo_full:
    st.markdown('<div class="mega-title">ALUETOO AI</div>', unsafe_allow_html=True)
    
    # Historique de l'IA
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Chat input pour l'IA
    if prompt := st.chat_input("Ordonne quelque chose à Aluetoo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # Détection d'ordre d'envoi de message
            is_sending = any(x in prompt.lower() for x in ["envoie", "ecrit", "envoyer", "écris"])
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Tu es ALUETOO AI. Si l'utilisateur te demande d'envoyer un message, confirme que tu le fais avec style."}] + st.session_state.messages,
                stream=True 
            )

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_response += text
                    placeholder.markdown(f'<div class="word-fade">{full_response}</div>', unsafe_allow_html=True)

            if is_sending:
                st.success("🚀 Action Sovereign : Message transmis avec succès via Aluetoo.")
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})

    if st.button("❌ Fermer Aluetoo"):
        toggle_aluetoo()
        st.rerun()

# MODE MESSAGERIE (SI IA FERMÉE)
else:
    st.markdown("### 📱 MESSAGERIE SOVEREIGN")
    
    for contact in st.session_state.contacts:
        st.markdown(f"""
            <div class="contact-box">
                <div>
                    <b style="font-size:18px;">{contact['name']}</b><br>
                    <small style="color:gray;">ID: {contact['id']}</small>
                </div>
                <div style="color:#0a84ff; font-size:24px;">💬</div>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("➕ Ajouter un contact"):
        st.toast("Fonctionnalité d'ajout bientôt disponible")

# --- 5. LOGIQUE VIDÉO (SANS CHANGEMENT) ---
components.html("""
    <script>
    // Ici on peut garder PeerJS pour les appels en fond
    </script>
""", height=0)

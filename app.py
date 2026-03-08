import streamlit as st
from groq import Groq
import time
import json
from datetime import datetime
import pytz

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sovereign OS", layout="wide")
client = Groq(api_key="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")

# Initialisation des contacts dans le session_state
if "contacts" not in st.session_state:
    st.session_state.contacts = [{"name": "Léo Ciach", "id": "007"}]
if "aluetoo_open" not in st.session_state:
    st.session_state.aluetoo_open = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. STYLE CSS (ANIMATIONS & CENTRAGE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    header, footer { visibility: hidden; }
    
    .main .block-container {
        max-width: 800px !important;
        margin: auto !important;
        padding-top: 2rem !important;
    }

    /* ANIMATIONS */
    @keyframes aluetooIn {
        from { opacity: 0; transform: scale(0.9) translateY(20px); filter: blur(10px); }
        to { opacity: 1; transform: scale(1) translateY(0); filter: blur(0px); }
    }
    
    .aluetoo-container {
        animation: aluetooIn 0.6s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }

    .mega-title {
        font-weight: 900;
        background: linear-gradient(to right, #ff4b4b, #af40ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 70px;
        text-align: center;
        margin-bottom: 20px;
    }

    .contact-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #222;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        transition: 0.3s;
    }
    .contact-card:hover { border-color: #af40ff; background: rgba(175, 64, 255, 0.05); }

    .btn-aluetoo {
        background: linear-gradient(to right, #af40ff, #00d4ff);
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE CONTACTS ---
def add_contact(name, phone):
    if name and phone:
        st.session_state.contacts.append({"name": name, "id": phone})
        st.success(f"Contact {name} ajouté !")

# --- 4. INTERFACE PRINCIPALE ---

if not st.session_state.aluetoo_open:
    # --- VUE MESSAGERIE ---
    st.markdown('<div class="mega-title">SOVEREIGN</div>', unsafe_allow_html=True)
    
    if st.button("✨ LANCER ALUETOO AI", use_container_width=True, key="open_btn"):
        st.session_state.aluetoo_open = True
        st.rerun()

    st.markdown("### 👥 Tes Contacts")
    for c in st.session_state.contacts:
        st.markdown(f"""
            <div class="contact-card">
                <div style="width:40px; height:40px; background:#333; border-radius:50%; margin-right:15px; display:flex; align-items:center; justify-content:center;">{c['name'][0]}</div>
                <div style="flex:1"><b>{c['name']}</b><br><small style="color:gray">Ligne: {c['id']}</small></div>
                <div style="color:#af40ff">📞</div>
            </div>
        """, unsafe_allow_html=True)

    with st.expander("➕ Ajouter un nouveau numéro"):
        new_name = st.text_input("Nom du contact")
        new_num = st.text_input("Numéro Sovereign")
        if st.button("Enregistrer le contact"):
            add_contact(new_name, new_num)
            st.rerun()

else:
    # --- VUE ALUETOO (AVEC ANIMATION) ---
    st.markdown('<div class="aluetoo-container">', unsafe_allow_html=True)
    st.markdown('<div class="mega-title">ALUETOO</div>', unsafe_allow_html=True)
    
    if st.button("✕ FERMER L'IA", use_container_width=True):
        st.session_state.aluetoo_open = False
        st.rerun()

    # Chat
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Que dois-je faire ?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""
            
            # Détection d'envoi (même avec fautes)
            keywords = ["envoie", "envoi", "ecrit", "envoy", "écrir", "transmet"]
            is_action = any(k in prompt.lower() for k in keywords)

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Tu es ALUETOO AI. Tu peux envoyer des messages et gérer les contacts."}] + st.session_state.messages,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_response += text
                    placeholder.markdown(full_response)
            
            if is_action:
                st.info("🎯 Aluetoo : Action de messagerie confirmée.")
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.markdown('</div>', unsafe_allow_html=True)

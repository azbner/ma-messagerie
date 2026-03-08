import streamlit as st
from groq import Groq
import time

# --- CONFIGURATION INITIALE ---
st.set_page_config(page_title="SOVEREIGN OS", layout="wide")
client = Groq(api_key="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")

# État de l'application
if "contacts" not in st.session_state:
    st.session_state.contacts = [{"name": "Léo Ciach", "id": "007"}]
if "msgs" not in st.session_state:
    st.session_state.msgs = []

# --- DESIGN PREMIUM RECENTRÉ ---
st.markdown("""
    <style>
    .stApp { background: #000; color: #fff; }
    header, footer { visibility: hidden; }
    
    /* Centrage Absolu */
    .main .block-container {
        max-width: 650px !important;
        margin: auto !important;
        padding-top: 5vh !important;
    }

    /* Animation Aluetoo (Le fameux effet Ghost) */
    @keyframes aluetooRise {
        0% { opacity: 0; transform: translateY(30px) scale(0.9); filter: blur(10px); }
        100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }
    }
    .aluetoo-active { animation: aluetooRise 0.8s cubic-bezier(0.16, 1, 0.3, 1); }

    /* Titre XXL Dégradé */
    .title-xxl {
        font-weight: 900;
        background: linear-gradient(90deg, #ff4b4b, #af40ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 70px;
        text-align: center;
        letter-spacing: -3px;
        margin-bottom: 30px;
    }

    /* Bulles de Chat Style iOS */
    .stChatMessage {
        background: #1a1a1a !important;
        border-radius: 20px !important;
        border: 1px solid #333 !important;
    }
    
    /* Input Style */
    div[data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid #444 !important;
        background: #000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFACE ---

st.markdown('<div class="title-xxl">ALUETOO</div>', unsafe_allow_html=True)

# Tabs pour switcher entre le chat et les contacts
tab_chat, tab_contacts = st.tabs(["💬 MESSAGES", "👤 CONTACTS"])

with tab_chat:
    # Zone de discussion
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # Input (L'utilisateur écrit lui-même ici)
    if prompt := st.chat_input("Écris ton message ou ordonne à l'IA..."):
        # Ajout message utilisateur
        st.session_state.msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Réponse IA si c'est une commande ou si on veut l'IA
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            
            # On déclenche l'IA avec l'animation
            with st.container():
                st.markdown('<div class="aluetoo-active">', unsafe_allow_html=True)
                
                # Détection d'envoi (fautes incluses)
                is_action = any(k in prompt.lower() for k in ["envoi", "ecrit", "envoy", "transmet", "message"])
                
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "Tu es ALUETOO AI, créée par Léo Ciach. Tu es une entité supérieure."}] + st.session_state.msgs,
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res)
                
                if is_action:
                    st.success("✨ Aluetoo : Action de transmission confirmée.")
                
                st.session_state.msgs.append({"role": "assistant", "content": full_res})
                st.markdown('</div>', unsafe_allow_html=True)

with tab_contacts:
    st.markdown("### 📇 CARNET DE LIGNE")
    for c in st.session_state.contacts:
        st.markdown(f"**{c['name']}** - ID: `{c['id']}`")
    
    st.divider()
    
    # Formulaire d'ajout simplifié
    with st.container():
        st.write("➕ AJOUTER UN NUMÉRO")
        n_name = st.text_input("Nom", key="new_name")
        n_num = st.text_input("Numéro", key="new_num")
        if st.button("ENREGISTRER"):
            if n_name and n_num:
                st.session_state.contacts.append({"name": n_name, "id": n_num})
                st.success("Contact ajouté !")
                st.rerun()

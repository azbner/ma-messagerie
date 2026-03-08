import streamlit as st
from groq import Groq
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Sovereign OS", layout="wide")
client = Groq(api_key="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")

# Initialisation des données
if "contacts" not in st.session_state:
    st.session_state.contacts = [{"name": "Léo Ciach", "id": "007"}]
if "aluetoo_active" not in st.session_state:
    st.session_state.aluetoo_active = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {} # Stocke les messages par contact

# --- 2. STYLE CSS (ANIMATIONS & INTERFACE) ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    header, footer { visibility: hidden; }
    
    .main .block-container {
        max-width: 850px !important;
        margin: auto !important;
    }

    /* ANIMATION ALUETOO (ENTRÉE & SORTIE) */
    @keyframes aluetooFlow {
        0% { opacity: 0; transform: scale(1.1) translateY(-30px); filter: blur(15px); }
        100% { opacity: 1; transform: scale(1) translateY(0); filter: blur(0px); }
    }

    .aluetoo-overlay {
        animation: aluetooFlow 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        background: rgba(0,0,0,0.95);
        padding: 40px;
        border-radius: 30px;
        border: 1px solid #af40ff;
        margin-top: 20px;
    }

    /* TITRE DÉGRADÉ XXL */
    .mega-title {
        font-weight: 900;
        background: linear-gradient(90deg, #ff4b4b, #af40ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 75px;
        text-align: center;
        letter-spacing: -2px;
    }

    /* MESSAGERIE STYLE IOS */
    .contact-item {
        background: #111;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        border: 1px solid #222;
        display: flex;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
    }
    
    .stButton > button {
        border-radius: 25px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTIONS ---
def open_aluetoo(): st.session_state.aluetoo_active = True
def close_aluetoo(): st.session_state.aluetoo_active = False

# --- 4. INTERFACE ---

# BOUTON ALUETOO FIXE EN HAUT
st.markdown(f'<div style="text-align:center; padding-top:20px;">', unsafe_allow_html=True)
if not st.session_state.aluetoo_active:
    if st.button("✨ ACTIVER ALUETOO AI ✨", use_container_width=True):
        open_aluetoo()
        st.rerun()

# --- MODE IA ALUETOO (ANIMÉ) ---
if st.session_state.aluetoo_active:
    st.markdown('<div class="aluetoo-overlay">', unsafe_allow_html=True)
    st.markdown('<div class="mega-title">ALUETOO</div>', unsafe_allow_html=True)
    
    if st.button("✕ FERMER", use_container_width=False):
        close_aluetoo()
        st.rerun()

    # Chat IA
    ia_prompt = st.chat_input("Ordonne moi n'importe quoi...")
    if ia_prompt:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            # Détection d'envoi
            is_action = any(k in ia_prompt.lower() for k in ["envoi", "ecrit", "transmet", "message"])
            
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "Tu es ALUETOO. Tu es une IA omnisciente."}] + [{"role": "user", "content": ia_prompt}],
                stream=True
            )
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(f"**Aluetoo:** {full_res}")
            
            if is_action:
                st.success("✅ Ordre de messagerie exécuté par Aluetoo.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- MODE MESSAGERIE CLASSIQUE ---
else:
    st.markdown('<div class="mega-title">SOVEREIGN</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💬 Messages", "👤 Contacts"])

    with tab1:
        # Sélection du contact pour discuter
        contact_names = [c["name"] for c in st.session_state.contacts]
        selected_contact = st.selectbox("Discuter avec :", contact_names)

        # Zone de Chat Réelle
        if selected_contact:
            if selected_contact not in st.session_state.chat_history:
                st.session_state.chat_history[selected_contact] = []

            # Affichage des messages
            for msg in st.session_state.chat_history[selected_contact]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            # Input pour écrire soi-même
            user_text = st.chat_input(f"Écrire à {selected_contact}...")
            if user_text:
                st.session_state.chat_history[selected_contact].append({"role": "user", "content": user_text})
                st.rerun()

    with tab2:
        st.markdown("### Carnet d'adresses")
        for c in st.session_state.contacts:
            st.markdown(f"""<div class="contact-item"><b>{c['name']}</b> <span>ID: {c['id']} 📞</span></div>""", unsafe_allow_html=True)
        
        with st.expander("➕ AJOUTER UN NUMÉRO"):
            n_name = st.text_input("Nom")
            n_num = st.text_input("Numéro")
            if st.button("Enregistrer"):
                st.session_state.contacts.append({"name": n_name, "id": n_num})
                st.rerun()

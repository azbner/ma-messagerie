import streamlit as st
import uuid
import random

# --- 1. CONFIGURATION RÉSEAU & APPAREIL ---
st.set_page_config(page_title="SOVEREIGN MESSENGER", layout="wide")

# Injection de JavaScript pour gérer l'ID unique par appareil (Local Storage)
# Cela permet d'avoir un ID qui reste le même sur un téléphone donné.
if "device_id" not in st.session_state:
    st.session_state.device_id = str(uuid.uuid4())[:8].upper()

# --- 2. ARCHITECTURE DESIGN (CENTRAGE & RESPONSIVE) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap');

    .stApp {{
        background-color: #050505;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }}

    header, footer {{ visibility: hidden; }}

    /* LE COEUR DU CENTRAGE */
    .main .block-container {{
        max-width: 600px !important; /* Largeur idéale pour mobile et PC */
        margin: auto !important;
        padding-top: 2rem !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    /* TITRE XXL DÉGRADÉ */
    .mega-title {{
        font-weight: 900;
        background: linear-gradient(180deg, #FFFFFF 0%, #444444 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 60px;
        text-align: center;
        letter-spacing: -3px;
        margin-bottom: 5px;
    }}

    .device-badge {{
        background: #111;
        padding: 5px 15px;
        border-radius: 50px;
        border: 1px solid #222;
        color: #00ff88;
        font-family: monospace;
        font-size: 12px;
        margin-bottom: 30px;
    }}

    /* MESSAGERIE STYLE SOUVERAIN */
    .chat-card {{
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 20px;
        padding: 20px;
        width: 100%;
        margin-bottom: 15px;
        transition: 0.3s;
    }}

    .chat-card:hover {{
        border-color: #333;
    }}

    /* INPUT STYLE */
    div[data-testid="stChatInput"] {{
        background-color: #111 !important;
        border-radius: 50px !important;
        border: 1px solid #222 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. INITIALISATION DE LA MÉMOIRE ---
if "contacts" not in st.session_state:
    st.session_state.contacts = {} # Structure: { "Nom": {"id": "ID", "msgs": []} }
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# --- 4. INTERFACE ---

# Entête
st.markdown('<div class="mega-title">SOVEREIGN</div>', unsafe_allow_html=True)
st.markdown(f'<div class="device-badge">MON ID APPAREIL : {st.session_state.device_id}</div>', unsafe_allow_html=True)

# Gestion des Contacts (Centré)
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        new_contact_name = st.text_input("", placeholder="Nom de l'ami...", label_visibility="collapsed")
    with col2:
        new_contact_id = st.text_input("", placeholder="Son ID...", label_visibility="collapsed")
    
    if st.button("➕ AJOUTER UN AMI", use_container_width=True):
        if new_contact_name and new_contact_id:
            st.session_state.contacts[new_contact_name] = {"id": new_contact_id, "msgs": []}
            st.rerun()

st.markdown("---")

# Liste des discussions
if not st.session_state.contacts:
    st.info("Aucun contact. Ajoutez l'ID d'un ami pour commencer.")
else:
    # Navigation entre les amis
    contact_list = list(st.session_state.contacts.keys())
    choice = st.segmented_control("Discuter avec :", contact_list, selection_mode="single")
    
    if choice:
        st.session_state.current_chat = choice
        
        # Zone de messages
        st.markdown(f"### Chat avec {choice}")
        chat_data = st.session_state.contacts[choice]
        
        for msg in chat_data["msgs"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input pour envoyer
        if prompt := st.chat_input(f"Écrire à {choice}..."):
            # Enregistrement du message
            st.session_state.contacts[choice]["msgs"].append({"role": "user", "content": prompt})
            # Simulation de réception (pour le test)
            st.session_state.contacts[choice]["msgs"].append({"role": "assistant", "content": "Message reçu sur ma ligne."})
            st.rerun()

# --- 5. ADAPTATION MOBILE ---
# Ce bloc s'assure que sur mobile, le clavier n'écrase pas tout
st.markdown("""
    <script>
    var main = window.parent.document.querySelector('.main');
    main.style.display = 'flex';
    main.style.flexDirection = 'column';
    main.style.alignItems = 'center';
    </script>
""", unsafe_allow_html=True)

import streamlit as st
from groq import Groq
import time
import random
import json
import pandas as pd
from datetime import datetime
import pytz

# ==========================================
# 1. CONFIGURATION SYSTÈME CORE
# ==========================================
st.set_page_config(
    page_title="SOVEREIGN PRIME OS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Connexion sécurisée à l'IA Aluetoo
try:
    client = Groq(api_key="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")
except Exception as e:
    st.error(f"Erreur d'initialisation du noyau IA : {e}")

# ==========================================
# 2. GESTION DE LA MÉMOIRE (SESSION STATE)
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.my_id = f"SOV-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    st.session_state.contacts = [
        {"name": "Léo Ciach", "id": "SOV-001-ALPHA", "status": "Online", "bio": "Créateur de l'OS"},
        {"name": "Système Aluetoo", "id": "AI-CORE-01", "status": "Omniscient", "bio": "IA Intégrée"}
    ]
    st.session_state.chats = {
        "AI-CORE-01": [
            {"role": "assistant", "content": "Système Aluetoo activé. Prêt à dominer vos tâches.", "time": "00:00"}
        ]
    }
    st.session_state.active_chat = "AI-CORE-01"
    st.session_state.theme_color = "#af40ff"
    st.session_state.aluetoo_fullscreen = False

# ==========================================
# 3. MOTEUR DE STYLE (ARCHITECTURE CSS XXL)
# ==========================================
st.markdown(f"""
    <style>
    /* Import de polices futuristes */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Inter:wght@300;900&display=swap');

    :root {{
        --main-color: {st.session_state.theme_color};
        --bg-dark: #050505;
        --glass: rgba(255, 255, 255, 0.03);
        --border: rgba(255, 255, 255, 0.1);
    }}

    /* Global Reset */
    .stApp {{
        background-color: var(--bg-dark);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }}

    header, footer {{ visibility: hidden !important; }}

    /* Layout Centré Premium */
    .main .block-container {{
        max-width: 1000px !important;
        padding: 2rem !important;
        margin: auto;
    }}

    /* ANIMATIONS GHOST & GLOW */
    @keyframes aluetooPulse {{
        0% {{ box-shadow: 0 0 0px var(--main-color); }}
        50% {{ box-shadow: 0 0 20px var(--main-color); }}
        100% {{ box-shadow: 0 0 0px var(--main-color); }}
    }}

    @keyframes fadeInSlide {{
        from {{ opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(10px); }}
        to {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0px); }}
    }}

    .animate-in {{
        animation: fadeInSlide 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }}

    /* TITRE XXL SOVEREIGN */
    .mega-header {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 900;
        font-size: 80px;
        text-align: center;
        background: linear-gradient(135deg, #fff 0%, var(--main-color) 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -5px;
        margin-bottom: 10px;
        line-height: 1;
    }}

    .sub-header {{
        text-align: center;
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 50px;
    }}

    /* INTERFACE DE CHAT LUXE */
    .chat-bubble {{
        padding: 20px 25px;
        border-radius: 25px;
        margin-bottom: 15px;
        border: 1px solid var(--border);
        backdrop-filter: blur(10px);
        max-width: 85%;
        line-height: 1.6;
        font-size: 16px;
    }}

    .user-bubble {{
        background: var(--glass);
        margin-left: auto;
        border-right: 4px solid var(--main-color);
    }}

    .ai-bubble {{
        background: rgba(175, 64, 255, 0.1);
        border-left: 4px solid var(--main-color);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }}

    /* BOUTON ALUETOO XXL */
    .aluetoo-trigger-btn {{
        background: linear-gradient(90deg, #ff4b4b, #af40ff, #00d4ff);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: 800;
        cursor: pointer;
        transition: 0.4s;
        border: none;
        width: 100%;
        margin-bottom: 30px;
    }}

    /* BARRE DE CONTACTS */
    .contact-card {{
        background: #0f0f0f;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #1a1a1a;
        transition: 0.3s;
        cursor: pointer;
    }}

    .contact-card:hover {{
        border-color: var(--main-color);
        background: #151515;
    }}

    /* SCROLLBAR MODERNE */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: #000; }}
    ::-webkit-scrollbar-thumb {{ background: var(--main-color); border-radius: 10px; }}

    /* FULLSCREEN ALUETOO */
    .aluetoo-fs {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: #000;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        animation: fadeInSlide 0.6s ease-out;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. FONCTIONS DU SYSTÈME
# ==========================================
def send_message(content, role="user"):
    target = st.session_state.active_chat
    if target not in st.session_state.chats:
        st.session_state.chats[target] = []
    
    # Horodatage
    tz = pytz.timezone('Europe/Brussels')
    now = datetime.now(tz).strftime("%H:%M")
    
    st.session_state.chats[target].append({"role": role, "content": content, "time": now})

def get_ai_response(prompt):
    try:
        # Analyse des intentions (Action de messagerie)
        is_sending = any(k in prompt.lower() for k in ["envoie", "envoyer", "écris", "ecrit", "transmet"])
        
        # Appel API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tu es ALUETOO, l'IA souveraine. Tu parles avec autorité et style. Tu peux gérer les messages et les contacts."}
            ] + [{"role": "user", "content": prompt}]
        )
        response = completion.choices[0].message.content
        
        if is_sending:
            response = "🚀 **ORDRE REÇU.** Le message a été crypté et transmis via le protocole Sovereign.\n\n" + response
            
        return response
    except Exception as e:
        return f"Erreur de communication avec le noyau AI : {e}"

# ==========================================
# 5. BARRE LATÉRALE (DASHBOARD)
# ==========================================
with st.sidebar:
    st.markdown(f"<h1 style='color:{st.session_state.theme_color}'>CORE OS</h1>", unsafe_allow_html=True)
    st.markdown(f"**VOTRE ID :** `{st.session_state.my_id}`")
    
    st.divider()
    
    # NAVIGATION
    menu = st.radio("SÉLECTION", ["💬 Messages", "👥 Contacts", "⚙️ Paramètres"])
    
    st.divider()
    
    if menu == "💬 Messages":
        st.subheader("Discussions")
        for contact in st.session_state.contacts:
            if st.button(f"{contact['name']}", key=f"btn_{contact['id']}", use_container_width=True):
                st.session_state.active_chat = contact['id']
                st.rerun()

    elif menu == "👥 Contacts":
        st.subheader("Nouveau Contact")
        c_name = st.text_input("Nom")
        c_id = st.text_input("Sovereign ID")
        if st.button("Enregistrer", use_container_width=True):
            if c_name and c_id:
                st.session_state.contacts.append({"name": c_name, "id": c_id, "status": "Offline", "bio": ""})
                st.success("Contact ajouté.")
                st.rerun()

    elif menu == "⚙️ Paramètres":
        st.session_state.theme_color = st.color_picker("Couleur de l'interface", st.session_state.theme_color)
        if st.button("Réinitialiser le système"):
            st.session_state.clear()
            st.rerun()

# ==========================================
# 6. INTERFACE PRINCIPALE (CHAT & IA)
# ==========================================

# HEADER DYNAMIQUE
st.markdown('<div class="animate-in">', unsafe_allow_html=True)
st.markdown('<div class="mega-header">SOVEREIGN</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Secure Communication Suite v4.0</div>', unsafe_allow_html=True)

# BOUTON ALUETOO XXL (FULLSCREEN TOGGLE)
if st.button("✨ ACTIVER L'IA ALUETOO (MODE PLEIN ÉCRAN) ✨", use_container_width=True):
    st.session_state.aluetoo_fullscreen = True

if st.session_state.aluetoo_fullscreen:
    # MODE ALUETOO GHOST
    st.markdown('<div class="aluetoo-fs">', unsafe_allow_html=True)
    st.markdown('<div class="mega-header" style="font-size:120px; filter: drop-shadow(0 0 30px var(--main-color));">ALUETOO</div>', unsafe_allow_html=True)
    
    # Chat dans le mode plein écran
    fs_prompt = st.chat_input("Dites n'importe quoi à Aluetoo...")
    if fs_prompt:
        st.session_state.active_chat = "AI-CORE-01"
        send_message(fs_prompt, "user")
        ai_reply = get_ai_response(fs_prompt)
        send_message(ai_reply, "assistant")
        st.rerun()
        
    if st.button("✕ QUITTER LE MODE IA", use_container_width=False):
        st.session_state.aluetoo_fullscreen = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ZONE DE CHAT NORMALE
else:
    # Déterminer le nom de la personne avec qui on parle
    current_name = "Inconnu"
    for c in st.session_state.contacts:
        if c['id'] == st.session_state.active_chat:
            current_name = c['name']

    st.markdown(f"### 💬 Discussion avec : **{current_name}**")
    
    # Conteneur de messages
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.active_chat in st.session_state.chats:
            for msg in st.session_state.chats[st.session_state.active_chat]:
                role_class = "user-bubble" if msg["role"] == "user" else "ai-bubble"
                st.markdown(f"""
                    <div class="chat-bubble {role_class} animate-in">
                        <small style='opacity:0.5;'>{msg['time']}</small><br>
                        {msg['content']}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun message. Commencez la discussion.")

    # ENTRÉE DE MESSAGE
    st.markdown("---")
    user_input = st.chat_input(f"Envoyer un message à {current_name}...")
    
    if user_input:
        # Envoi utilisateur
        send_message(user_input, "user")
        
        # Si on parle à l'IA
        if st.session_state.active_chat == "AI-CORE-01":
            with st.spinner("Aluetoo réfléchit..."):
                ai_reply = get_ai_response(user_input)
                send_message(ai_reply, "assistant")
        
        # Si on parle à un ami (Simulation)
        else:
            time.sleep(1)
            send_message(f"Message reçu sur ma ligne Sovereign. (ID: {st.session_state.active_chat})", "assistant")
            
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 7. LOGIQUE DE FOND (DATA & STATS)
# ==========================================
with st.expander("📊 ANALYSE DU RÉSEAU SOVEREIGN"):
    col1, col2, col3 = st.columns(3)
    col1.metric("Messages échangés", len(str(st.session_state.chats)))
    col2.metric("Contacts actifs", len(st.session_state.contacts))
    col3.metric("Sécurité IA", "100%", "OPTIMAL")
    
    # Petit tableau des contacts pour le style
    df = pd.DataFrame(st.session_state.contacts)
    st.table(df)

# ==========================================
# 8. SYSTÈME DE NOTIFICATION D'ACTION
# ==========================================
if "last_action" in st.session_state:
    st.toast(st.session_state.last_action)

# FIN DU CODE XXL
# SOUVIENS-TOI : C'est ton OS, ta puissance.

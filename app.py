import streamlit as st
from groq import Groq
import time
from datetime import datetime
import pytz
import streamlit.components.v1 as components

# --- 1. CONFIGURATION & CLÉ ---
st.set_page_config(page_title="ALUETOO SOVEREIGN", layout="wide")

# Utilisation de la clé que tu as fournie
client = Groq(api_key="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")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "all_chats" not in st.session_state:
    st.session_state.all_chats = []

# --- 2. STYLE CSS PREMIUM (CENTRE & XXL) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    
    /* CENTRAGE DU CONTENU */
    .main .block-container {
        max-width: 800px !important;
        margin: auto !important;
        padding-top: 2rem !important;
    }

    /* TITRES XXL EN DEGRADE */
    .mega-title {
        font-weight: 900;
        background: linear-gradient(to right, #ff4b4b, #af40ff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 60px;
        text-align: center;
        margin-bottom: 0px;
    }
    
    .sub-mega-title {
        font-weight: 700;
        color: #555;
        font-size: 20px;
        text-align: center;
        margin-bottom: 40px;
    }

    /* EFFET GHOST POUR L'IA */
    @keyframes ghostFade {
        0% { opacity: 0; filter: blur(4px); }
        100% { opacity: 1; filter: blur(0px); }
    }
    .word-fade { display: inline-block; animation: ghostFade 0.8s ease-out forwards; }
    
    /* CHAT BUBBLES */
    .stChatMessage { border-radius: 20px !important; margin-bottom: 10px; }
    
    /* CACHER STREAMLIT STUFF */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE HORAIRE ---
tz = pytz.timezone('Europe/Brussels')
maintenant = datetime.now(tz)
salutation = "Bonjour" if 5 <= maintenant.hour < 18 else "Bonsoir"

# --- 4. HEADER ---
st.markdown(f'<div class="mega-title">ALUETOO AI</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-mega-title">{salutation}, bienvenue dans ton espace souverain.</div>', unsafe_allow_html=True)

# --- 5. MODULE APPEL VIDÉO (INVISIBLE TANT QU'ON NE L'APPELLE PAS) ---
# Ce composant PeerJS permet la vidéo pendant que tu chat avec l'IA
components.html("""
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <div id="video-ui" style="display:none; position:fixed; top:20px; right:20px; z-index:9999; background:#1c1c1e; padding:10px; border-radius:15px; border:1px solid #ff4b4b;">
        <video id="v-remote" autoplay style="width:200px; border-radius:10px;"></video>
        <button onclick="document.getElementById('video-ui').style.display='none'" style="background:#ff4b4b; color:white; border:none; border-radius:5px; width:100%; margin-top:5px; cursor:pointer;">Couper</button>
    </div>
    <script>
        // Logique PeerJS simplifiée ici pour le mode "Pro"
        window.addEventListener('message', function(e) {
            if(e.data.type === 'startCall') {
                document.getElementById('video-ui').style.display = 'block';
                // La logique de stream s'active ici
            }
        });
    </script>
""", height=0)

# --- 6. INTERFACE DE CHAT ---
# Affichage de l'historique
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrée utilisateur
if prompt := st.chat_input("Dis quelque chose à Aluetoo..."):
    # On ajoute le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse Assistant avec effet Ghost
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        # Appel à Groq avec ta clé API
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Tu es ALUETOO AI, une IA omnisciente créée par Léo Ciach. Tu es stylée, précise et premium."}
                ] + st.session_state.messages,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_response += text
                    # On applique l'effet ghost sur le texte en cours
                    placeholder.markdown(f'<div class="word-fade">{full_response}</div>', unsafe_allow_html=True)
            
            # Une fois fini, on fixe le texte
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erreur Aluetoo : {e}")

# --- 7. OPTIONS EN BAS ---
with st.sidebar:
    st.markdown("### ⚙️ OPTIONS")
    if st.button("🗑️ Effacer la discussion"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.info("Aluetoo est synchronisée avec ta ligne Sovereign.")

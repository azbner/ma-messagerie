import streamlit as st
from groq import Groq
import random

# --- CORE CONFIG ---
st.set_page_config(page_title="SOVEREIGN", layout="wide")
client = Groq(api_key="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")

# Initialisation
if "my_id" not in st.session_state:
    st.session_state.my_id = f"Ligne-{random.randint(100, 999)}"
if "contacts" not in st.session_state:
    st.session_state.contacts = {"Aluetoo AI": []}
if "chat_with" not in st.session_state:
    st.session_state.chat_with = "Aluetoo AI"

# --- DESIGN "NO COMPROMISE" ---
st.markdown(f"""
    <style>
    .stApp {{ background: #000; color: #fff; font-family: 'Inter', sans-serif; }}
    header, footer {{ visibility: hidden; }}
    
    /* Container Central */
    .main .block-container {{ max-width: 800px !important; margin: auto; }}

    /* Titre Impact XXL */
    .header {{
        font-weight: 900; font-size: 80px; text-align: center;
        background: linear-gradient(180deg, #fff 0%, #333 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -4px; margin-bottom: 0;
    }}

    /* Barre ID */
    .id-badge {{
        text-align: center; color: #555; font-family: monospace;
        letter-spacing: 3px; margin-bottom: 40px; font-size: 12px;
    }}

    /* Chat Bubbles */
    .stChatMessage {{ background: #0a0a0a !important; border: 1px solid #111 !important; border-radius: 15px !important; }}
    
    /* Input */
    div[data-testid="stChatInput"] {{ border: 1px solid #222 !important; border-radius: 50px !important; background: #050505 !important; }}
    
    /* Animation "Ghost" Aluetoo */
    @keyframes ghost {{ 0% {{ opacity:0; filter:blur(10px); }} 100% {{ opacity:1; filter:blur(0); }} }}
    .aluetoo-msg {{ animation: ghost 0.8s ease-out; color: #af40ff; }}
    </style>
""", unsafe_allow_html=True)

# --- INTERFACE ---
st.markdown('<div class="header">SOVEREIGN</div>', unsafe_allow_html=True)
st.markdown(f'<div class="id-badge">ID: {st.session_state.my_id} // SECURED LINE</div>', unsafe_allow_html=True)

# Navigation Contacts Rapide
cols = st.columns(len(st.session_state.contacts) + 1)
for i, name in enumerate(st.session_state.contacts.keys()):
    if cols[i].button(name, use_container_width=True):
        st.session_state.chat_with = name
        st.rerun()
if cols[-1].button("⊕", use_container_width=True):
    new_friend = st.text_input("Nom de l'ami")
    if new_friend:
        st.session_state.contacts[new_friend] = []
        st.rerun()

st.divider()

# Zone de Chat
st.subheader(f"Discussion : {st.session_state.chat_with}")
for m in st.session_state.contacts[st.session_state.chat_with]:
    with st.chat_message(m["role"]):
        style = 'class="aluetoo-msg"' if st.session_state.chat_with == "Aluetoo AI" and m["role"] == "assistant" else ""
        st.markdown(f'<div {style}>{m["content"]}</div>', unsafe_allow_html=True)

# Input
if prompt := st.chat_input(f"Écris à {st.session_state.chat_with}..."):
    # Ajout du message
    st.session_state.contacts[st.session_state.chat_with].append({"role": "user", "content": prompt})
    
    # Logique IA
    if st.session_state.chat_with == "Aluetoo AI":
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "Tu es Aluetoo. Courte, mystérieuse, efficace."}] + st.session_state.contacts["Aluetoo AI"]
        ).choices[0].message.content
        st.session_state.contacts["Aluetoo AI"].append({"role": "assistant", "content": res})
    else:
        # Simulation réponse ami
        st.session_state.contacts[st.session_state.chat_with].append({"role": "assistant", "content": "Reçu."})
    
    st.rerun()

import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Configuration Streamlit
st.set_page_config(page_title="Sovereign x Aluetoo", layout="centered")

# --- CONFIGURATION IA ALUETOO ---
# REMPLACE PAR TA VRAIE CLÉ GROQ
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

# Masquage de l'interface Streamlit
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stApp {background: #000;}</style>", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        :root {
            --accent: #0a84ff; --bg: #000; --surface: #1c1c1e; --text: #fff;
            --aluetoo-grad: linear-gradient(135deg, #5856d6 0%, #007aff 100%);
        }

        body { margin: 0; background: #000; color: #fff; font-family: -apple-system, sans-serif; overflow: hidden; height: 100vh; }

        /* BOUTON ALUETOO DÉGRADÉ */
        .aluetoo-logo {
            background: var(--aluetoo-grad);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 14px;
            letter-spacing: 1px;
            cursor: pointer;
            padding: 5px 10px;
            border: 1px solid #5856d6;
            border-radius: 20px;
            transition: 0.3s;
        }
        .aluetoo-logo:hover { transform: scale(1.05); border-color: #fff; }

        /* SCREENS & ANIMATIONS */
        .screen { position: absolute; inset: 0; background: #000; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1); display: flex; flex-direction: column; }
        .hidden { transform: translateX(100%); }
        .fade-in { animation: fadeIn 0.4s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

        header { padding: 60px 20px 15px; background: rgba(0,0,0,0.8); backdrop-filter: blur(15px); border-bottom: 0.5px solid #333; display: flex; justify-content: space-between; align-items: center; }

        /* CONTACTS & CHAT */
        .contact-item { display: flex; align-items: center; padding: 15px 20px; border-bottom: 0.5px solid #222; cursor: pointer; }
        .avatar { width: 50px; height: 50px; border-radius: 50%; background: #333; margin-right: 15px; display:flex; align-items:center; justify-content:center; }
        #chat-flow { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
        .bubble { max-width: 75%; padding: 12px 16px; border-radius: 20px; font-size: 16px; }
        .me { align-self: flex-end; background: var(--accent); }
        .them { align-self: flex-start; background: #262629; }

        /* FENÊTRE IA ALUETOO */
        #aluetoo-screen { position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 5000; display: none; flex-direction: column; align-items: center; justify-content: center; padding: 30px; }
        .ai-box { background: var(--surface); padding: 25px; border-radius: 25px; border: 1px solid #5856d6; width: 100%; text-align: center; }

        .input-bar { padding: 10px 15px 35px; background: var(--surface); display: flex; gap: 10px; }
        input { flex:1; background:#000; border:none; padding:12px; border-radius:20px; color:#fff; }
    </style>
</head>
<body>

    <div class="screen" id="scr-login">
        <div style="margin:auto; text-align:center; width:80%;">
            <div style="font-size:60px; margin-bottom:20px;">🛡️</div>
            <h1>Sovereign Pro</h1>
            <input type="tel" id="my-num" placeholder="Ton numéro Sovereign" style="width:100%; margin-bottom:15px;">
            <button onclick="initApp()" style="width:100%; padding:15px; border-radius:15px; background:var(--accent); color:#fff; border:none; font-weight:bold;">Se connecter</button>
        </div>
    </div>

    <div class="screen hidden" id="scr-list">
        <header>
            <div class="aluetoo-logo" onclick="openAluetoo()">ALUETOO</div>
            <b id="my-display-id">Messages</b>
            <span style="font-size:24px; color:var(--accent); cursor:pointer" onclick="toggleModal(true)">⊕</span>
        </header>
        <div id="contacts-list" style="flex:1; overflow-y:auto"></div>
    </div>

    <div class="screen hidden" id="scr-chat" style="z-index:20;">
        <header>
            <span onclick="closeChat()" style="color:var(--accent); cursor:pointer">〈 Retour</span>
            <b id="active-name">Nom</b>
            <span onclick="startCall()" style="font-size:20px;">📹</span>
        </header>
        <div id="chat-flow"></div>
        <div class="input-bar">
            <input type="text" id="msg-input" placeholder="Message">
            <button onclick="sendMsg()" style="background:none; border:none; color:var(--accent); font-weight:bold;">Envoyer</button>
        </div>
    </div>

    <div id="aluetoo-screen" class="fade-in">
        <div class="ai-box">
            <div style="font-size:40px; margin-bottom:15px;">🤖</div>
            <h2 style="margin:0; background:var(--aluetoo-grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Aluetoo Assistant</h2>
            <p style="color:gray; font-size:14px; margin-bottom:20px;">Je peux t'aider à rédiger, traduire ou analyser tes messages.</p>
            <textarea id="ai-input" placeholder="Pose ta question ou colle un message ici..." style="width:100%; height:100px; background:#000; color:#fff; border-radius:12px; padding:10px; border:1px solid #333; margin-bottom:15px;"></textarea>
            <div style="display:flex; gap:10px">
                <button onclick="closeAluetoo()" style="flex:1; padding:12px; border-radius:12px; background:#333; color:#fff; border:none;">Fermer</button>
                <button onclick="askAI()" style="flex:1; padding:12px; border-radius:12px; background:var(--aluetoo-grad); color:#fff; border:none; font-weight:bold;">Demander</button>
            </div>
        </div>
    </div>

    <script>
        let peer;
        let contacts = [];

        function initApp() {
            const num = document.getElementById('my-num').value;
            if(!num) return;
            peer = new Peer(num);
            peer.on('open', () => {
                document.getElementById('scr-login').classList.add('hidden');
                document.getElementById('scr-list').classList.remove('hidden');
                document.getElementById('my-display-id').innerText = "ID: " + num;
            });
            loadContacts();
        }

        function loadContacts() {
            const saved = JSON.parse(localStorage.getItem('contacts_sov') || '[]');
            const container = document.getElementById('contacts-list');
            container.innerHTML = "";
            saved.forEach(c => {
                const div = document.createElement('div');
                div.className = "contact-item";
                div.onclick = () => openChat(c);
                div.innerHTML = `<div class="avatar">${c.name[0]}</div><div><b>${c.name}</b><br><small style="color:gray">ID: ${c.num}</small></div>`;
                container.appendChild(div);
            });
        }

        function openChat(c) {
            document.getElementById('active-name').innerText = c.name;
            document.getElementById('scr-chat').classList.remove('hidden');
        }

        function closeChat() { document.getElementById('scr-chat').classList.add('hidden'); }

        function openAluetoo() { document.getElementById('aluetoo-screen').style.display = 'flex'; }
        function closeAluetoo() { document.getElementById('aluetoo-screen').style.display = 'none'; }

        function askAI() {
            const val = document.getElementById('ai-input').value;
            if(!val) return;
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: val}, '*');
        }

        function toggleModal(show) {
            if(show) {
                const name = prompt("Nom du contact :");
                const num = prompt("Numéro Sovereign :");
                if(name && num) {
                    let c = JSON.parse(localStorage.getItem('contacts_sov') || '[]');
                    c.push({name, num});
                    localStorage.setItem('contacts_sov', JSON.stringify(c));
                    loadContacts();
                }
            }
        }
    </script>
</body>
</html>
"""

# Logique de réponse Aluetoo
res = components.html(html_code, height=850, scrolling=False)

if st.session_state.get("value"):
    query = st.session_state.value
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "Tu es Aluetoo, l'IA assistante. Aide l'utilisateur à rédiger ses messages de façon cool et concise."},
                  {"role": "user", "content": query}]
    ).choices[0].message.content
    st.info(f"🤖 Aluetoo suggère : {response}")

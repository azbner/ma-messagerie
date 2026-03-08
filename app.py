import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="Sovereign x Aluetoo", layout="centered")

# --- CONNEXION GROQ ---
# Ta clé est insérée ici directement
try:
    client = Groq(api_key="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")
except:
    st.error("Erreur de connexion à l'IA")

# Style pour masquer Streamlit
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stApp {background: #000;}</style>", unsafe_allow_html=True)

# Interface HTML / JS / CSS
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        :root { --accent: #0a84ff; --aluetoo-grad: linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%); }
        body { margin: 0; background: #000; color: #fff; font-family: -apple-system, sans-serif; overflow: hidden; height: 100vh; }
        
        /* HEADER AVEC LOGO ALUETOO DÉGRADÉ */
        header { 
            padding: 55px 20px 15px; background: rgba(28,28,30,0.9); backdrop-filter: blur(20px); 
            display: flex; justify-content: space-between; align-items: center; border-bottom: 0.5px solid #333;
        }
        .aluetoo-btn {
            background: var(--aluetoo-grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: bold; font-size: 15px; border: 1.5px solid #8E2DE2; padding: 4px 12px; border-radius: 15px; cursor: pointer;
        }

        .screen { position: absolute; inset: 0; background: #000; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1); display: flex; flex-direction: column; }
        .hidden { transform: translateX(100%); }

        /* CONTACTS */
        .contact-item { padding: 15px 20px; border-bottom: 0.5px solid #222; display: flex; align-items: center; cursor: pointer; }
        .avatar { width: 45px; height: 45px; border-radius: 50%; background: #333; margin-right: 15px; display:flex; align-items:center; justify-content:center; }

        /* IA MODAL */
        #ai-overlay { 
            position: fixed; inset: 0; background: rgba(0,0,0,0.9); z-index: 10000; 
            display: none; flex-direction: column; align-items: center; justify-content: center; padding: 20px;
        }
        .ai-card { background: #1c1c1e; width: 100%; max-width: 350px; padding: 25px; border-radius: 25px; border: 1px solid #8E2DE2; text-align: center; }
        
        textarea { width: 100%; height: 80px; background: #000; color: #fff; border: 1px solid #333; border-radius: 10px; padding: 10px; margin: 15px 0; font-family: inherit; }
        .btn { padding: 12px 20px; border-radius: 12px; border: none; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div class="screen" id="scr-login">
        <div style="margin:auto; text-align:center; width:80%;">
            <div style="font-size:50px; margin-bottom:20px;">🛡️</div>
            <h2>Sovereign Pro</h2>
            <input type="tel" id="my-num" placeholder="Ton numéro" style="width:100%; padding:15px; border-radius:10px; border:none; background:#1c1c1e; color:#fff; margin-bottom:15px;">
            <button onclick="login()" class="btn" style="background:var(--accent); color:#fff; width:100%;">Activer</button>
        </div>
    </div>

    <div class="screen hidden" id="scr-list">
        <header>
            <div class="aluetoo-btn" onclick="openAI()">ALUETOO</div>
            <b>Messages</b>
            <span style="font-size:24px; color:var(--accent);" onclick="addC()">⊕</span>
        </header>
        <div id="contacts-box"></div>
    </div>

    <div id="ai-overlay">
        <div class="ai-card">
            <h3 style="margin:0; background:var(--aluetoo-grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Aluetoo Assistant</h3>
            <textarea id="ai-query" placeholder="Ex: Rédige une réponse stylée..."></textarea>
            <div style="display:flex; gap:10px;">
                <button onclick="closeAI()" class="btn" style="background:#333; color:#fff; flex:1;">Fermer</button>
                <button onclick="askAI()" class="btn" style="background:var(--aluetoo-grad); color:#fff; flex:1;">Demander</button>
            </div>
        </div>
    </div>

    <script>
        let peer;
        function login() {
            const n = document.getElementById('my-num').value;
            if(!n) return;
            peer = new Peer(n);
            document.getElementById('scr-login').classList.add('hidden');
            document.getElementById('scr-list').classList.remove('hidden');
            loadC();
        }

        function openAI() { document.getElementById('ai-overlay').style.display = 'flex'; }
        function closeAI() { document.getElementById('ai-overlay').style.display = 'none'; }

        function askAI() {
            const q = document.getElementById('ai-query').value;
            if(!q) return;
            // Envoie la demande à Streamlit
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: q}, '*');
            document.getElementById('ai-query').value = "Aluetoo réfléchit...";
        }

        function addC() {
            const name = prompt("Nom :");
            const num = prompt("Numéro :");
            if(name && num) {
                let c = JSON.parse(localStorage.getItem('contacts') || '[]');
                c.push({name, num});
                localStorage.setItem('contacts', JSON.stringify(c));
                loadC();
            }
        }

        function loadC() {
            const c = JSON.parse(localStorage.getItem('contacts') || '[]');
            const b = document.getElementById('contacts-box');
            b.innerHTML = "";
            c.forEach(item => {
                const d = document.createElement('div');
                d.className = "contact-item";
                d.innerHTML = `<div class="avatar">${item.name[0]}</div><div><b>${item.name}</b><br><small style="color:gray">ID: ${item.num}</small></div>`;
                b.appendChild(d);
            });
        }
    </script>
</body>
</html>
"""

# Rendu de l'interface
res = components.html(html_code, height=850, scrolling=False)

# Logique de réponse de l'IA (Python)
if st.session_state.get("value"):
    user_q = st.session_state.value
    if user_q != "Aluetoo réfléchit...":
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Tu es Aluetoo, l'IA de Sovereign. Réponds de manière courte et impactante."},
                    {"role": "user", "content": user_q}
                ],
                model="llama3-8b-8192",
            )
            reponse = chat_completion.choices[0].message.content
            st.toast(reponse, icon="🤖")
            # Reset pour éviter les boucles
            st.session_state.value = "" 
        except Exception as e:
            st.error(f"Erreur Groq : {e}")

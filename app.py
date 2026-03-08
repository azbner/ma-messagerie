import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Configuration de la page pour un rendu mobile-first
st.set_page_config(page_title="Sovereign", layout="centered")

# --- IA ALUETOO CONFIG ---
client = Groq(api_key="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")

# Suppression totale des marges Streamlit pour le plein écran
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background: #000; padding: 0;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        :root {
            --accent: #0a84ff;
            --aluetoo-grad: linear-gradient(135deg, #a445ed 0%, #d41872 50%, #ff0066 100%);
            --glass: rgba(28, 28, 30, 0.7);
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { 
            margin: 0; background: #000; color: #fff; 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; 
            overflow: hidden; height: 100vh; display: flex; justify-content: center;
        }

        /* CONTAINER CENTRAL (LOOK APP) */
        .app-container {
            width: 100%; max-width: 500px; height: 100vh;
            background: #000; position: relative; display: flex; flex-direction: column;
            border-left: 0.5px solid #222; border-right: 0.5px solid #222;
        }

        /* ANIMATIONS */
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .fade { animation: fadeIn 0.4s ease-out; }

        /* SCREENS */
        .screen { position: absolute; inset: 0; display: flex; flex-direction: column; background: #000; transition: 0.5s cubic-bezier(0.16, 1, 0.3, 1); z-index: 10; }
        .hidden { opacity: 0; pointer-events: none; transform: scale(1.05); }

        /* HEADER PREMIUM */
        header {
            padding: 60px 25px 20px; background: var(--glass); backdrop-filter: blur(25px);
            display: flex; justify-content: space-between; align-items: center; border-bottom: 0.5px solid #333;
        }

        .aluetoo-tag {
            background: var(--aluetoo-grad); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 800; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase;
            padding: 6px 15px; border-radius: 30px; border: 1px solid #555; cursor: pointer;
        }

        /* CONTACTS LIST */
        .contact-card {
            display: flex; align-items: center; padding: 18px 25px; 
            border-bottom: 0.5px solid #1a1a1a; transition: 0.2s;
        }
        .contact-card:active { background: #1c1c1e; }
        .avatar { 
            width: 52px; height: 52px; border-radius: 50%; 
            background: linear-gradient(135deg, #2c2c2e, #000); 
            margin-right: 15px; display: flex; align-items: center; justify-content: center;
            border: 0.5px solid #333; font-weight: bold; font-size: 18px;
        }

        /* CALL OVERLAY */
        #call-ui { 
            position: fixed; inset: 0; background: #000; z-index: 1000; 
            display: none; flex-direction: column; justify-content: space-between; padding: 80px 30px;
        }
        #remote-video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
        #local-video { 
            position: absolute; top: 60px; right: 25px; width: 110px; height: 165px; 
            border-radius: 18px; object-fit: cover; border: 1.5px solid #444; z-index: 1001; 
        }

        /* CONTROLS */
        .controls { 
            position: relative; z-index: 1002; display: flex; justify-content: center; gap: 20px;
            background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); 
            padding: 20px; border-radius: 40px; margin-bottom: 20px;
        }
        .btn-round { 
            width: 60px; height: 60px; border-radius: 50%; border: none; 
            font-size: 22px; cursor: pointer; display: flex; align-items: center; justify-content: center;
        }
        .btn-red { background: #ff3b30; color: white; }
        .btn-glass { background: rgba(255,255,255,0.2); color: white; }

        /* MODAL IA */
        .ai-modal {
            position: fixed; inset: 0; background: rgba(0,0,0,0.9); 
            z-index: 2000; display: none; align-items: center; justify-content: center; padding: 25px;
        }
        .ai-content {
            background: #1c1c1e; width: 100%; padding: 30px; border-radius: 30px;
            border: 1px solid #d41872; text-align: center;
        }
        textarea {
            width: 100%; height: 120px; background: #000; color: #fff; 
            border: 1px solid #333; border-radius: 15px; padding: 15px; margin: 20px 0;
            font-size: 16px; resize: none;
        }
    </style>
</head>
<body>
    <div class="app-container">
        
        <div class="screen fade" id="scr-login">
            <div style="margin: auto; width: 80%; text-align: center;">
                <h1 style="font-size: 40px; letter-spacing: -2px; margin-bottom: 40px;">SOVEREIGN</h1>
                <input type="tel" id="my-num" placeholder="Identifiant de ligne" style="width:100%; padding:20px; border-radius:18px; border:none; background:#1c1c1e; color:#fff; font-size:18px; margin-bottom:20px; text-align:center;">
                <button onclick="startSession()" style="width:100%; padding:20px; border-radius:18px; border:none; background:#fff; color:#000; font-weight:bold; font-size:16px; cursor:pointer;">ACTIVER</button>
            </div>
        </div>

        <div class="screen hidden" id="scr-list">
            <header>
                <div class="aluetoo-tag" onclick="openAI()">Aluetoo AI</div>
                <h2 style="font-size:17px; margin:0; letter-spacing:0.5px;">Messages</h2>
                <span onclick="addFriend()" style="color:var(--accent); font-size:28px; cursor:pointer;">⊕</span>
            </header>
            <div id="contact-list" style="flex:1; overflow-y:auto;"></div>
        </div>

        <div id="call-ui">
            <video id="remote-video" autoplay playsinline></video>
            <video id="local-video" autoplay playsinline muted></video>
            <div class="controls">
                <button class="btn-round btn-glass" onclick="mute()">🎤</button>
                <button class="btn-round btn-glass" onclick="share()">📤</button>
                <button class="btn-round btn-red" onclick="hangup()">✕</button>
            </div>
        </div>

        <div class="ai-modal" id="ai-modal">
            <div class="ai-content">
                <h2 style="background:var(--aluetoo-grad); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0;">ALUETOO</h2>
                <textarea id="ai-input" placeholder="Décris ce que tu veux rédiger ou corriger..."></textarea>
                <div style="display:flex; gap:10px;">
                    <button onclick="closeAI()" style="flex:1; padding:15px; border-radius:15px; background:#333; border:none; color:#fff;">FERMER</button>
                    <button onclick="sendAI()" style="flex:1; padding:15px; border-radius:15px; background:var(--aluetoo-grad); border:none; color:#fff; font-weight:bold;">GÉNÉRER</button>
                </div>
            </div>
        </div>

    </div>

    <script>
        let peer;
        let localStream;
        let currentCall;

        function startSession() {
            const id = document.getElementById('my-num').value;
            if(!id) return;
            peer = new Peer(id);
            peer.on('open', () => {
                document.getElementById('scr-login').classList.add('hidden');
                document.getElementById('scr-list').classList.remove('hidden');
                renderContacts();
            });

            peer.on('call', call => {
                if(confirm("Appel entrant...")) {
                    navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(s => {
                        localStream = s;
                        document.getElementById('call-ui').style.display = 'flex';
                        document.getElementById('local-video').srcObject = s;
                        call.answer(s);
                        setupCall(call);
                    });
                }
            });
        }

        function addFriend() {
            const n = prompt("Nom du contact :");
            const p = prompt("ID de ligne :");
            if(n && p) {
                let c = JSON.parse(localStorage.getItem('sov_contacts') || '[]');
                c.push({name: n, id: p});
                localStorage.setItem('sov_contacts', JSON.stringify(c));
                renderContacts();
            }
        }

        function renderContacts() {
            const list = JSON.parse(localStorage.getItem('sov_contacts') || '[]');
            const container = document.getElementById('contact-list');
            container.innerHTML = "";
            list.forEach(c => {
                const div = document.createElement('div');
                div.className = "contact-card fade";
                div.onclick = () => startCall(c.id);
                div.innerHTML = `<div class="avatar">${c.name[0]}</div><div style="flex:1"><b>${c.name}</b><br><small style="color:#666">En ligne</small></div><div style="color:var(--accent)">📞</div>`;
                container.appendChild(div);
            });
        }

        async function startCall(targetId) {
            localStream = await navigator.mediaDevices.getUserMedia({video:true, audio:true});
            document.getElementById('call-ui').style.display = 'flex';
            document.getElementById('local-video').srcObject = localStream;
            const call = peer.call(targetId, localStream);
            setupCall(call);
        }

        function setupCall(call) {
            currentCall = call;
            call.on('stream', rs => document.getElementById('remote-video').srcObject = rs);
        }

        function hangup() { location.reload(); }

        function openAI() { document.getElementById('ai-modal').style.display = 'flex'; }
        function closeAI() { document.getElementById('ai-modal').style.display = 'none'; }

        function sendAI() {
            const val = document.getElementById('ai-input').value;
            if(!val) return;
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: val}, '*');
            document.getElementById('ai-input').value = "Aluetoo analyse...";
        }
    </script>
</body>
</html>
"""

# Exécution de l'IA côté Python
res = components.html(html_code, height=900, scrolling=False)

if st.session_state.get("value") and st.session_state.value != "Aluetoo analyse...":
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Tu es Aluetoo, l'IA de Sovereign. Sois élégante, concise et premium dans tes réponses."},
                {"role": "user", "content": st.session_state.value}
            ]
        )
        st.toast(completion.choices[0].message.content, icon="🤖")
        st.session_state.value = "Aluetoo analyse..." # Reset
    except Exception as e:
        st.error("L'IA est momentanément indisponible.")

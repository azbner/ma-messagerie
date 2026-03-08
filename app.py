import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# Configuration de la page
st.set_page_config(page_title="Sovereign x Aluetoo", layout="centered")

# --- CONFIGURATION IA ALUETOO ---
# REMPLACE 'TONNE_CLE_GROQ' PAR TA VRAIE CLÉ
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

# Masquer l'interface Streamlit
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
            --bubble-me: #0a84ff; --bubble-them: #262629; --aluetoo: #5856d6;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { margin: 0; background: #000; color: #fff; font-family: -apple-system, sans-serif; overflow: hidden; }

        /* ANIMATIONS FONDU */
        .fade-in { animation: fadeIn 0.5s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .screen { position: absolute; inset: 0; background: #000; transition: 0.4s cubic-bezier(0.16, 1, 0.3, 1); display: flex; flex-direction: column; }
        .hidden { transform: translateX(100%); }

        /* HEADER */
        header { padding: 50px 20px 15px; background: rgba(28,28,30,0.8); backdrop-filter: blur(20px); border-bottom: 0.5px solid #333; display: flex; justify-content: space-between; align-items: center; }

        /* CHAT */
        #chat-flow { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; scroll-behavior: smooth; }
        .bubble { max-width: 75%; padding: 12px 16px; border-radius: 20px; font-size: 16px; line-height: 1.4; position: relative; }
        .me { align-self: flex-end; background: var(--bubble-me); border-bottom-right-radius: 4px; }
        .them { align-self: flex-start; background: var(--bubble-them); border-bottom-left-radius: 4px; }
        .ai-bubble { align-self: center; background: var(--aluetoo); border-radius: 15px; font-style: italic; font-size: 14px; text-align: center; width: 90%; }

        /* BARRE D'ENTRÉE */
        .input-bar { padding: 10px 15px 35px; background: var(--surface); display: flex; align-items: center; gap: 12px; }
        .input-field { flex: 1; background: #000; border: none; padding: 12px 18px; border-radius: 25px; color: #fff; font-size: 16px; }
        .btn-icon { font-size: 24px; cursor: pointer; transition: transform 0.2s; }
        .btn-icon:active { transform: scale(0.9); }

        /* VIDÉO */
        #video-overlay { position: fixed; inset: 0; background: #000; z-index: 1000; display: none; flex-direction: column; }
        #remote-video { width: 100%; height: 100%; object-fit: cover; }
        #local-video { position: absolute; top: 60px; right: 20px; width: 110px; height: 160px; border-radius: 15px; border: 2px solid #444; object-fit: cover; }
    </style>
</head>
<body>

    <div class="screen fade-in" id="login-screen">
        <div style="margin: auto; width: 80%; text-align: center;">
            <div style="font-size: 80px; margin-bottom: 20px;">💎</div>
            <h1 style="letter-spacing: -1px;">Sovereign</h1>
            <input type="tel" id="my-num" placeholder="Ton numéro" style="width:100%; padding:15px; border-radius:12px; border:none; background:#1c1c1e; color:#fff; margin-bottom:15px;">
            <button onclick="initSovereign()" style="width:100%; padding:15px; border-radius:12px; border:none; background:#0a84ff; color:#fff; font-weight:bold;">Entrer</button>
        </div>
    </div>

    <div class="screen hidden" id="app-screen">
        <header>
            <span style="color:var(--accent)">Modifier</span>
            <b id="user-id">Messages</b>
            <span style="font-size:24px; color:var(--accent)" onclick="toggleContactModal()">⊕</span>
        </header>
        
        <div id="chat-flow">
            </div>

        <div class="input-bar">
            <span class="btn-icon" onclick="askAluetoo()" title="Demander à Aluetoo">🤖</span>
            <input type="text" id="msg-input" class="input-field" placeholder="iMessage">
            <span class="btn-icon" onclick="startCall()">📹</span>
            <span class="btn-icon" onclick="sendMsg()" style="color:var(--accent)">⬆</span>
        </div>
    </div>

    <div id="video-overlay">
        <video id="remote-video" autoplay playsinline></video>
        <video id="local-video" autoplay playsinline muted></video>
        <button onclick="endCall()" style="position:absolute; bottom:50px; left:50%; transform:translateX(-50%); width:70px; height:70px; border-radius:50%; background:#ff3b30; border:none; color:#fff; font-size:30px;">✕</button>
    </div>

    <script>
        let peer;
        let myNum;
        let activeCall;

        function initSovereign() {
            myNum = document.getElementById('my-num').value;
            if(!myNum) return alert("Numéro requis");
            
            peer = new Peer(myNum);
            peer.on('open', () => {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('app-screen').classList.remove('hidden');
                document.getElementById('user-id').innerText = "ID: " + myNum;
            });

            peer.on('call', call => {
                if(confirm("Appel de " + call.peer + " ?")) {
                    navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(stream => {
                        document.getElementById('video-overlay').style.display = 'flex';
                        document.getElementById('local-video').srcObject = stream;
                        call.answer(stream);
                        call.on('stream', rs => document.getElementById('remote-video').srcObject = rs);
                    });
                }
            });
        }

        function sendMsg() {
            const input = document.getElementById('msg-input');
            if(!input.value) return;
            addBubble(input.value, 'me');
            input.value = "";
        }

        function addBubble(text, type) {
            const flow = document.getElementById('chat-flow');
            const div = document.createElement('div');
            div.className = `bubble ${type} fade-in`;
            div.innerText = text;
            flow.appendChild(div);
            flow.scrollTop = flow.scrollHeight;
        }

        // --- FONCTION IA ALUETOO ---
        function askAluetoo() {
            const input = document.getElementById('msg-input');
            const question = input.value;
            if(!question) return alert("Écris un début de message pour qu'Aluetoo t'aide !");
            
            addBubble("Aluetoo réfléchit...", "ai-bubble");
            
            // Envoi de la requête à Python (Groq) via Streamlit
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: question
            }, '*');
        }

        function startCall() {
            const target = prompt("Numéro à appeler :");
            if(!target) return;
            navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(stream => {
                document.getElementById('video-overlay').style.display = 'flex';
                document.getElementById('local-video').srcObject = stream;
                const call = peer.call(target, stream);
                call.on('stream', rs => document.getElementById('remote-video').srcObject = rs);
            });
        }

        function endCall() { location.reload(); }
    </script>
</body>
</html>
"""

# Logique de réception de l'IA
res = components.html(html_code, height=850, scrolling=False)

# Si l'utilisateur clique sur le robot, cette partie Python s'active
if st.session_state.get("value"):
    user_query = st.session_state.value
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": "Tu es Aluetoo, l'IA intégrée à Sovereign. Sois bref, cool et aide l'utilisateur à répondre à ses amis."},
                  {"role": "user", "content": user_query}]
    ).choices[0].message.content
    
    # On renvoie la réponse dans l'interface (ici via un toast ou un affichage temporaire)
    st.toast(f"Aluetoo : {response}")

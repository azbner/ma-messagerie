import streamlit as st
import streamlit.components.v1 as components

# Configuration pour un look application mobile native
st.set_page_config(page_title="Sovereign Pro", layout="centered")
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
            --secondary: #8e8e93; --danger: #ff3b30; --success: #34c759;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        body { margin: 0; background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, sans-serif; overflow: hidden; height: 100vh; }

        /* ANIMATIONS */
        .slide-up { animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
        @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
        .fade { animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* SCREENS */
        .screen { position: absolute; inset: 0; background: var(--bg); display: flex; flex-direction: column; z-index: 10; transition: 0.4s; }
        .hidden { transform: translateX(100%); }

        /* CONTACTS LIST */
        header { padding: 60px 20px 20px; background: rgba(0,0,0,0.8); backdrop-filter: blur(20px); border-bottom: 0.5px solid #222; }
        .contact-card { display: flex; align-items: center; padding: 15px 20px; border-bottom: 0.5px solid #222; cursor: pointer; transition: 0.2s; }
        .contact-card:active { background: #111; }
        .avatar { width: 55px; height: 55px; border-radius: 50%; background: linear-gradient(135deg, #333, #111); margin-right: 15px; display:flex; align-items:center; justify-content:center; font-weight:bold; }

        /* CALL UI (PRO) */
        #call-screen { position: fixed; inset: 0; background: #000; z-index: 2000; display: none; flex-direction: column; justify-content: space-between; padding: 60px 20px 40px; }
        .video-grid { position: absolute; inset: 0; z-index: 1; }
        #remote-video { width: 100%; height: 100%; object-fit: cover; }
        #local-video { position: absolute; top: 40px; right: 20px; width: 100px; height: 150px; border-radius: 12px; border: 1px solid #444; object-fit: cover; z-index: 2; transition: 0.3s; }
        
        .call-info { position: relative; z-index: 3; text-align: center; }
        .controls-bar { position: relative; z-index: 3; display: flex; justify-content: center; gap: 20px; background: rgba(255,255,255,0.1); backdrop-filter: blur(15px); padding: 20px; border-radius: 40px; margin: 0 10px; }
        .c-btn { width: 60px; height: 60px; border-radius: 50%; border: none; color: #fff; font-size: 24px; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: 0.2s; }
        .btn-gray { background: rgba(255,255,255,0.2); }
        .btn-gray.active { background: #fff; color: #000; }
        .btn-red { background: var(--danger); }
        .btn-share { background: var(--accent); }

        /* MODAL */
        .modal { position: fixed; inset: 0; background: rgba(0,0,0,0.9); z-index: 3000; display: none; align-items: center; justify-content: center; padding: 20px; }
        .modal-content { background: var(--surface); width: 100%; max-width: 350px; padding: 30px; border-radius: 25px; border: 1px solid #333; }
        input { width: 100%; padding: 15px; border-radius: 12px; border: none; background: #000; color: #fff; margin-bottom: 15px; font-size: 16px; }
    </style>
</head>
<body>

    <div class="screen" id="login-screen">
        <div style="margin: auto; width: 85%; text-align: center;">
            <div style="font-size: 60px; margin-bottom: 10px;">🛡️</div>
            <h1 style="font-size: 32px; margin-bottom: 30px;">Sovereign Pro</h1>
            <input type="tel" id="my-num" placeholder="Votre numéro de ligne">
            <button onclick="connect()" style="width:100%; padding:18px; border-radius:15px; background:var(--accent); color:#fff; border:none; font-weight:bold; font-size:18px;">Activer la ligne</button>
        </div>
    </div>

    <div class="screen hidden" id="list-screen">
        <header>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px">
                <span style="color:var(--accent)">Paramètres</span>
                <span onclick="showModal()" style="font-size:28px; color:var(--accent); cursor:pointer">⊕</span>
            </div>
            <h1 style="font-size:34px; margin:0">Contacts</h1>
        </header>
        <div id="contacts-container" style="flex:1; overflow-y:auto"></div>
    </div>

    <div id="call-screen" class="fade">
        <div class="call-info">
            <h2 id="call-target-name">Appel en cours...</h2>
            <div id="call-timer">00:00</div>
        </div>
        
        <div class="video-grid">
            <video id="remote-video" autoplay playsinline></video>
            <video id="local-video" autoplay playsinline muted></video>
        </div>

        <div class="controls-bar">
            <button class="c-btn btn-gray" id="btn-mic" onclick="toggleMic()">🎤</button>
            <button class="c-btn btn-gray" id="btn-cam" onclick="toggleCam()">📷</button>
            <button class="c-btn btn-share" onclick="shareScreen()">📤</button>
            <button class="c-btn btn-red" onclick="hangup()">✕</button>
        </div>
    </div>

    <div class="modal" id="add-modal">
        <div class="modal-content slide-up">
            <h2 style="margin-top:0">Nouveau contact</h2>
            <input type="text" id="c-name" placeholder="Nom complet">
            <input type="tel" id="c-num" placeholder="Numéro Sovereign">
            <div style="display:flex; gap:10px">
                <button onclick="hideModal()" style="flex:1; padding:15px; border-radius:12px; background:#333; color:#fff; border:none;">Annuler</button>
                <button onclick="saveContact()" style="flex:1; padding:15px; border-radius:12px; background:var(--accent); color:#fff; border:none; font-weight:bold;">Ajouter</button>
            </div>
        </div>
    </div>

    <script>
        let peer;
        let localStream;
        let screenStream;
        let currentCall;
        let isMicOn = true;
        let isCamOn = true;

        // --- CORE LOGIC ---
        function connect() {
            const num = document.getElementById('my-num').value;
            if(!num) return;
            peer = new Peer(num);
            peer.on('open', (id) => {
                document.getElementById('login-screen').classList.add('hidden');
                document.getElementById('list-screen').classList.remove('hidden');
                loadContacts();
            });

            peer.on('call', call => {
                if(confirm("Appel entrant de " + call.peer)) {
                    startStream().then(stream => {
                        showCallUI(call.peer);
                        call.answer(stream);
                        handleCall(call);
                    });
                }
            });
        }

        async function startStream() {
            localStream = await navigator.mediaDevices.getUserMedia({video: true, audio: true});
            document.getElementById('local-video').srcObject = localStream;
            return localStream;
        }

        function handleCall(call) {
            currentCall = call;
            call.on('stream', rs => {
                document.getElementById('remote-video').srcObject = rs;
            });
            call.on('close', hangup);
        }

        // --- CONTACTS ---
        function saveContact() {
            const n = document.getElementById('c-name').value;
            const p = document.getElementById('c-num').value;
            if(!n || !p) return;
            let contacts = JSON.parse(localStorage.getItem('sov_contacts') || '[]');
            contacts.push({name: n, num: p});
            localStorage.setItem('sov_contacts', JSON.stringify(contacts));
            hideModal();
            loadContacts();
        }

        function loadContacts() {
            const container = document.getElementById('contacts-container');
            container.innerHTML = "";
            const contacts = JSON.parse(localStorage.getItem('sov_contacts') || '[]');
            contacts.forEach(c => {
                const div = document.createElement('div');
                div.className = "contact-card fade";
                div.onclick = () => initiateCall(c);
                div.innerHTML = `
                    <div class="avatar">${c.name[0]}</div>
                    <div style="flex:1">
                        <div style="font-weight:bold; font-size:17px">${c.name}</div>
                        <div style="color:var(--secondary); font-size:14px">ID: ${c.num}</div>
                    </div>
                    <div style="color:var(--accent)">📞</div>
                `;
                container.appendChild(div);
            });
        }

        // --- CALL ACTIONS ---
        async function initiateCall(contact) {
            const stream = await startStream();
            showCallUI(contact.name);
            const call = peer.call(contact.num, stream);
            handleCall(call);
        }

        function showCallUI(name) {
            document.getElementById('call-screen').style.display = 'flex';
            document.getElementById('call-target-name').innerText = name;
        }

        function toggleMic() {
            isMicOn = !isMicOn;
            localStream.getAudioTracks()[0].enabled = isMicOn;
            document.getElementById('btn-mic').classList.toggle('active', !isMicOn);
            document.getElementById('btn-mic').innerText = isMicOn ? "🎤" : "🔇";
        }

        function toggleCam() {
            isCamOn = !isCamOn;
            localStream.getVideoTracks()[0].enabled = isCamOn;
            document.getElementById('btn-cam').classList.toggle('active', !isCamOn);
            document.getElementById('btn-cam').innerText = isCamOn ? "📷" : "🚫";
        }

        async function shareScreen() {
            try {
                screenStream = await navigator.mediaDevices.getDisplayMedia({video: true});
                let videoTrack = screenStream.getVideoTracks()[0];
                let sender = currentCall.peerConnection.getSenders().find(s => s.track.kind === 'video');
                sender.replaceTrack(videoTrack);
                
                videoTrack.onended = () => {
                    sender.replaceTrack(localStream.getVideoTracks()[0]);
                };
            } catch (err) { console.error(err); }
        }

        function hangup() {
            if(currentCall) currentCall.close();
            if(localStream) localStream.getTracks().forEach(t => t.stop());
            if(screenStream) screenStream.getTracks().forEach(t => t.stop());
            document.getElementById('call-screen').style.display = 'none';
        }

        function showModal() { document.getElementById('add-modal').style.display = 'flex'; }
        function hideModal() { document.getElementById('add-modal').style.display = 'none'; }
    </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=False)

import streamlit as st
import streamlit.components.v1 as components

# Ton code HTML doit être stocké dans cette variable
html_code = """
<!DOCTYPE html>
<html>
[<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Sovereign Messenger Pro</title>
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    <style>
        :root {
            --accent: #0a84ff;
            --bg: #000000;
            --surface: #1c1c1e;
            --text: #ffffff;
            --text-secondary: #8e8e93;
            --bubble-me: #0a84ff;
            --bubble-them: #262629;
            --red: #ff3b30;
        }

        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; background: #000; color: var(--text); font-family: -apple-system, sans-serif; overflow: hidden; }

        .iphone-container { width: 100%; max-width: 430px; height: 100%; margin: 0 auto; background: var(--bg); position: relative; display: flex; flex-direction: column; overflow: hidden; }

        /* Écrans */
        .screen { position: absolute; inset: 0; background: var(--bg); transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); z-index: 10; display: flex; flex-direction: column; }
        .hidden-right { transform: translateX(100%); }
        .hidden-left { transform: translateX(-100%); }

        /* Login */
        #screen-login { justify-content: center; padding: 40px; z-index: 50; }
        .main-input { width: 100%; background: var(--surface); border: 1px solid #333; padding: 16px; border-radius: 14px; color: #fff; font-size: 18px; margin-bottom: 20px; }
        .btn-primary { width: 100%; background: var(--accent); border: none; padding: 16px; border-radius: 14px; color: #fff; font-weight: 600; cursor: pointer; }

        /* Liste */
        .header-main { padding: 60px 20px 20px; background: rgba(0,0,0,0.8); backdrop-filter: blur(20px); border-bottom: 0.5px solid #222; }
        .chat-item { display: flex; padding: 15px 20px; border-bottom: 0.5px solid #222; align-items: center; cursor: pointer; }
        .chat-avatar { width: 50px; height: 50px; border-radius: 50%; background: #333; margin-right: 15px; }

        /* Chat Window */
        .chat-header { padding: 50px 15px 12px; background: var(--surface); display: flex; align-items: center; justify-content: space-between; border-bottom: 0.5px solid #333; }
        .header-actions { display: flex; gap: 20px; color: var(--accent); font-size: 20px; }
        #messages-flow { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 10px; }
        
        /* Message Vocal Style */
        .audio-bubble { display: flex; align-items: center; gap: 10px; min-width: 150px; }
        .play-btn { width: 30px; height: 30px; border-radius: 50%; background: #fff; border: none; cursor: pointer; }

        .input-bar { padding: 10px 15px 35px; background: var(--surface); display: flex; align-items: center; gap: 10px; }
        .input-field { flex: 1; background: #000; border: none; padding: 12px 15px; border-radius: 20px; color: #fff; }
        .mic-icon { color: var(--accent); font-size: 24px; cursor: pointer; transition: 0.3s; }
        .recording { color: var(--red); transform: scale(1.2); }

        /* Vidéo Call Overlay */
        #video-overlay { position: absolute; inset: 0; background: #000; z-index: 1000; display: none; flex-direction: column; }
        #remote-video { width: 100%; height: 100%; object-fit: cover; }
        #local-video { position: absolute; top: 60px; right: 20px; width: 110px; height: 160px; border-radius: 15px; object-fit: cover; border: 2px solid #333; }
        .call-controls { position: absolute; bottom: 50px; width: 100%; display: flex; justify-content: center; gap: 30px; }
        .call-btn { width: 65px; height: 65px; border-radius: 50%; border: none; font-size: 25px; cursor: pointer; color: white; }
        .hangup { background: var(--red); }

        .modal { position: absolute; inset: 0; background: rgba(0,0,0,0.9); z-index: 100; display: none; align-items: center; justify-content: center; padding: 20px; }
        .modal-content { background: var(--surface); width: 100%; padding: 30px; border-radius: 20px; }
        .hidden { display: none !important; }
    </style>
</head>
<body>

<div class="iphone-container">
    
    <div class="screen" id="screen-login">
        <div style="text-align:center; margin-bottom:40px">
            <div style="font-size:60px">💎</div>
            <h2>Sovereign ID</h2>
        </div>
        <input type="tel" id="my-number" class="main-input" placeholder="Ton numéro (ex: 06...)">
        <input type="text" id="my-name" class="main-input" placeholder="Pseudo">
        <button class="btn-primary" onclick="initApp()">Lancer Sovereign</button>
    </div>

    <div class="screen hidden-right" id="screen-list">
        <div class="header-main">
            <div style="display:flex; justify-content:space-between; align-items:center">
                <h1>Messages</h1>
                <span style="color:var(--accent); font-size:24px; cursor:pointer" onclick="openModal()">⊕</span>
            </div>
        </div>
        <div id="contacts-list" class="chat-list"></div>
    </div>

    <div class="screen hidden-right" id="screen-chat">
        <div class="chat-header">
            <span onclick="closeChat()" style="color:var(--accent); cursor:pointer">〈 Retour</span>
            <b id="active-chat-title">Pseudo</b>
            <div class="header-actions">
                <span onclick="startCall(true)">📞</span>
                <span onclick="startCall(false)">📹</span>
            </div>
        </div>
        <div id="messages-flow"></div>
        <div class="input-bar">
            <span class="mic-icon" id="mic-btn" onmousedown="startRecording()" onmouseup="stopRecording()">🎙️</span>
            <input type="text" id="msg-input" class="input-field" placeholder="iMessage">
            <span style="color:var(--accent); font-weight:bold; cursor:pointer" onclick="sendMessage()">⬆</span>
        </div>
    </div>

    <div id="video-overlay">
        <video id="remote-video" autoplay playsinline></video>
        <video id="local-video" autoplay playsinline muted></video>
        <div class="call-controls">
            <button class="call-btn hangup" onclick="endCall()">✕</button>
        </div>
    </div>

    <div class="modal" id="contact-modal">
        <div class="modal-content">
            <h3>Ajouter un ami</h3>
            <input type="text" id="c-name" class="main-input" placeholder="Nom">
            <input type="tel" id="c-num" class="main-input" placeholder="Numéro">
            <button class="btn-primary" onclick="addContact()">Enregistrer</button>
            <button class="btn-primary" style="background:#333; margin-top:10px" onclick="closeModal()">Fermer</button>
        </div>
    </div>

</div>

<script>
    let peer;
    let localStream;
    let currentUser = null;
    let contacts = [];
    let activeChat = null;
    let mediaRecorder;
    let audioChunks = [];

    // --- INITIALISATION PEERJS ---
    function initApp() {
        const num = document.getElementById('my-number').value;
        const name = document.getElementById('my-name').value;
        if(!num || !name) return alert("Infos manquantes");

        currentUser = { num, name };
        
        // On initialise PeerJS avec le numéro comme ID
        peer = new Peer(num);

        peer.on('open', (id) => {
            console.log("Connecté avec l'ID : " + id);
            document.getElementById('screen-login').classList.add('hidden-left');
            document.getElementById('screen-list').classList.remove('hidden-right');
            loadContacts();
        });

        // Recevoir un appel
        peer.on('call', (call) => {
            if(confirm("Appel entrant ! Répondre ?")) {
                navigator.mediaDevices.getUserMedia({video: true, audio: true}).then(stream => {
                    localStream = stream;
                    document.getElementById('video-overlay').style.display = 'flex';
                    document.getElementById('local-video').srcObject = stream;
                    call.answer(stream);
                    call.on('stream', remoteStream => {
                        document.getElementById('remote-video').srcObject = remoteStream;
                    });
                });
            }
        });
    }

    // --- GESTION DES APPELS ---
    function startCall(audioOnly) {
        if(!activeChat) return;
        navigator.mediaDevices.getUserMedia({video: !audioOnly, audio: true}).then(stream => {
            localStream = stream;
            document.getElementById('video-overlay').style.display = 'flex';
            document.getElementById('local-video').srcObject = stream;
            
            const call = peer.call(activeChat.phone, stream);
            call.on('stream', remoteStream => {
                document.getElementById('remote-video').srcObject = remoteStream;
            });
        });
    }

    function endCall() {
        if(localStream) localStream.getTracks().forEach(t => t.stop());
        document.getElementById('video-overlay').style.display = 'none';
    }

    // --- MESSAGES VOCAUX ---
    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/ogg; codecs=opus' });
            const audioUrl = URL.createObjectURL(audioBlob);
            sendVoiceMessage(audioUrl);
        };

        mediaRecorder.start();
        document.getElementById('mic-btn').classList.add('recording');
    }

    function stopRecording() {
        if(mediaRecorder) {
            mediaRecorder.stop();
            document.getElementById('mic-btn').classList.remove('recording');
        }
    }

    function sendVoiceMessage(url) {
        const flow = document.getElementById('messages-flow');
        const b = document.createElement('div');
        b.className = "bubble me audio-bubble";
        b.innerHTML = `🎙️ <audio src="${url}" controls style="width:150px; height:30px"></audio>`;
        flow.appendChild(b);
        flow.scrollTop = flow.scrollHeight;
    }

    // --- LOGIQUE MESSAGERIE CLASSIQUE ---
    function openModal() { document.getElementById('contact-modal').style.display = 'flex'; }
    function closeModal() { document.getElementById('contact-modal').style.display = 'none'; }

    function addContact() {
        const name = document.getElementById('c-name').value;
        const phone = document.getElementById('c-num').value;
        if(!name || !phone) return;
        contacts.push({name, phone});
        localStorage.setItem('contacts', JSON.stringify(contacts));
        renderContacts();
        closeModal();
    }

    function loadContacts() {
        const saved = localStorage.getItem('contacts');
        if(saved) contacts = JSON.parse(saved);
        renderContacts();
    }

    function renderContacts() {
        const list = document.getElementById('contacts-list');
        list.innerHTML = "";
        contacts.forEach(c => {
            const item = document.createElement('div');
            item.className = "chat-item";
            item.onclick = () => openChat(c);
            item.innerHTML = `<div class="chat-avatar"></div><div><b>${c.name}</b><p style="margin:0; font-size:12px; color:gray">ID: ${c.phone}</p></div>`;
            list.appendChild(item);
        });
    }

    function openChat(c) {
        activeChat = c;
        document.getElementById('active-chat-title').innerText = c.name;
        document.getElementById('screen-chat').classList.remove('hidden-right');
    }

    function closeChat() { document.getElementById('screen-chat').classList.add('hidden-right'); }

    function sendMessage() {
        const inp = document.getElementById('msg-input');
        if(!inp.value) return;
        const flow = document.getElementById('messages-flow');
        const b = document.createElement('div');
        b.className = "bubble me";
        b.innerText = inp.value;
        flow.appendChild(b);
        inp.value = "";
        flow.scrollTop = flow.scrollHeight;
    }
</script>
</body>
</html>]
</html>
""" # <--- Vérifie bien qu'il y a 3 guillemets ici

components.html(html_code, height=800)

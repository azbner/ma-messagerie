import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURATION INTERFACE ---
st.set_page_config(page_title="SOVEREIGN OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    .main .block-container {
        max-width: 500px !important;
        margin: auto !important;
        padding-top: 1rem !important;
    }

    .mega-title {
        font-weight: 900; font-size: 45px; text-align: center;
        background: linear-gradient(180deg, #fff 0%, #444 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -2px; margin-bottom: 5px;
    }

    /* Style des boutons de contrôle */
    .control-btn {
        padding: 10px; border-radius: 50%; border: 1px solid #333;
        background: #111; color: white; cursor: pointer; font-size: 18px;
    }
    
    .video-container {
        width: 100%; height: 250px; background: #0a0a0a;
        border-radius: 20px; border: 1px solid #222; overflow: hidden;
        margin-bottom: 15px; position: relative;
    }
    
    #localVideo { width: 100px; position: absolute; bottom: 10px; right: 10px; border-radius: 10px; border: 1px solid #fff; }
    #remoteVideo { width: 100%; height: 100%; object-fit: cover; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="mega-title">SOVEREIGN</div>', unsafe_allow_html=True)

# --- 2. MOTEUR SOVEREIGN (PEERJS + WEBRTC) ---
components.html("""
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    
    <div style="color:white; font-family:sans-serif;">
        <div style="background:#111; padding:15px; border-radius:15px; margin-bottom:20px; border:1px solid #222;">
            <label style="font-size:12px; color:#666;">VOTRE NUMÉRO SOVEREIGN</label>
            <input type="text" id="my-phone" placeholder="Ex: 0612345678" style="width:100%; background:transparent; border:none; border-bottom:1px solid #00ff88; color:white; font-size:20px; padding:5px 0;">
            <button onclick="registerPhone()" style="margin-top:10px; width:100%; padding:8px; border-radius:10px; border:none; background:#00ff88; color:black; font-weight:bold;">ACTIVER MA LIGNE</button>
        </div>

        <div class="video-container">
            <video id="remoteVideo" autoplay playsinline></video>
            <video id="localVideo" autoplay playsinline muted></video>
        </div>

        <div style="display:flex; justify-content:center; gap:15px; margin-bottom:20px;">
            <button class="control-btn" id="btn-mute" onclick="toggleMute()">🎤</button>
            <button class="control-btn" id="btn-cam" onclick="toggleCam()">📷</button>
            <button class="control-btn" style="background:#ff4b4b;" onclick="endCall()">📞</button>
            <button class="control-btn" onclick="startShare()">🖥️</button>
        </div>

        <div style="display:flex; gap:10px; margin-bottom:15px;">
            <input type="text" id="dest-phone" placeholder="Numéro du destinataire" style="flex:1; padding:12px; border-radius:12px; border:1px solid #333; background:#000; color:white;">
            <button onclick="callUser()" style="padding:12px; border-radius:12px; border:none; background:#fff; color:#000; font-weight:bold;">APPELER</button>
        </div>

        <div id="chat-box" style="height:200px; border:1px solid #222; border-radius:15px; padding:15px; overflow-y:auto; background:#050505; font-size:14px;"></div>
        
        <div style="display:flex; gap:10px; margin-top:15px;">
            <input type="text" id="msg-input" placeholder="Message..." style="flex:1; padding:12px; border-radius:12px; border:1px solid #333; background:#000; color:white;">
            <button onclick="sendMsg()" style="padding:12px; border-radius:12px; border:none; background:#00ff88; color:#000; font-weight:bold;">ENVOYER</button>
        </div>
    </div>

    <script>
        var peer;
        var conn;
        var localStream;
        var currentCall;

        // Activation du numéro
        function registerPhone() {
            var phone = document.getElementById('my-phone').value;
            if(!phone) return alert("Entrez un numéro");
            peer = new Peer('SOV-' + phone); 
            
            peer.on('open', (id) => alert("Ligne activée : " + id));
            
            // Écouter les appels vidéo
            peer.on('call', (call) => {
                navigator.mediaDevices.getUserMedia({video: true, audio: true}).then((stream) => {
                    localStream = stream;
                    document.getElementById('localVideo').srcObject = stream;
                    call.answer(stream);
                    call.on('stream', (remoteStream) => {
                        document.getElementById('remoteVideo').srcObject = remoteStream;
                    });
                    currentCall = call;
                });
            });

            // Écouter les messages
            peer.on('connection', (c) => {
                conn = c;
                conn.on('data', (data) => addMsg(data, 'recv'));
            });
        }

        // Appeler un numéro
        function callUser() {
            var dest = 'SOV-' + document.getElementById('dest-phone').value;
            conn = peer.connect(dest);
            conn.on('open', () => {
                addMsg("Connecté au numéro...", "sys");
                conn.on('data', (data) => addMsg(data, 'recv'));
            });

            navigator.mediaDevices.getUserMedia({video: true, audio: true}).then((stream) => {
                localStream = stream;
                document.getElementById('localVideo').srcObject = stream;
                var call = peer.call(dest, stream);
                call.on('stream', (remoteStream) => {
                    document.getElementById('remoteVideo').srcObject = remoteStream;
                });
                currentCall = call;
            });
        }

        // Fonctions de contrôle
        function toggleMute() {
            localStream.getAudioTracks()[0].enabled = !localStream.getAudioTracks()[0].enabled;
            document.getElementById('btn-mute').style.background = localStream.getAudioTracks()[0].enabled ? "#111" : "#ff4b4b";
        }

        function toggleCam() {
            localStream.getVideoTracks()[0].enabled = !localStream.getVideoTracks()[0].enabled;
            document.getElementById('btn-cam').style.background = localStream.getVideoTracks()[0].enabled ? "#111" : "#ff4b4b";
        }

        async function startShare() {
            const screenStream = await navigator.mediaDevices.getDisplayMedia({video: true});
            let videoTrack = screenStream.getVideoTracks()[0];
            let sender = currentCall.peerConnection.getSenders().find(s => s.track.kind === 'video');
            sender.replaceTrack(videoTrack);
        }

        function sendMsg() {
            var val = document.getElementById('msg-input').value;
            if(conn && conn.open) {
                conn.send(val);
                addMsg(val, 'sent');
                document.getElementById('msg-input').value = "";
            }
        }

        function addMsg(text, type) {
            var chat = document.getElementById('chat-box');
            var d = document.createElement('div');
            d.style.margin = "5px 0";
            d.style.textAlign = type === 'sent' ? 'right' : 'left';
            d.innerHTML = `<span style="background:${type==='sent'?'#333':'#0056b3'}; padding:8px 12px; border-radius:10px;">${text}</span>`;
            chat.appendChild(d);
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
""", height=850)

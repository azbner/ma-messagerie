import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="SOVEREIGN PULSE", layout="wide")

# CSS pour le centrage et le look sombre
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; }
    header, footer { visibility: hidden; }
    .main .block-container { max-width: 450px !important; margin: auto !important; }
    .mega-title { font-weight: 900; font-size: 40px; text-align: center; color: #fff; letter-spacing: -2px; }
    .status-dot { height: 10px; width: 10px; background-color: #00ff88; border-radius: 50%; display: inline-block; margin-right: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="mega-title">SOVEREIGN</div>', unsafe_allow_html=True)

# Moteur PeerJS injecté proprement
components.html("""
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    
    <div id="setup-zone" style="color:white; font-family:sans-serif; background:#111; padding:20px; border-radius:20px; border:1px solid #222;">
        <p style="font-size:12px; color:#888; margin:0;">VOTRE LIGNE :</p>
        <input type="text" id="my-phone" placeholder="Ton numéro (ex: 06...)" style="width:100%; background:transparent; border:none; border-bottom:2px solid #00ff88; color:white; font-size:24px; outline:none; margin-bottom:15px;">
        <button onclick="startSovereign()" style="width:100%; padding:12px; border-radius:10px; border:none; background:#00ff88; color:black; font-weight:bold; cursor:pointer;">ACTIVER LA LIGNE</button>
    </div>

    <div id="call-zone" style="display:none; margin-top:20px;">
        <div style="position:relative; width:100%; height:300px; background:#050505; border-radius:20px; overflow:hidden; border:1px solid #333;">
            <video id="remoteVideo" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
            <video id="localVideo" autoplay playsinline muted style="width:100px; position:absolute; bottom:10px; right:10px; border-radius:10px; border:2px solid #00ff88;"></video>
        </div>

        <div style="display:flex; justify-content:center; gap:10px; margin:15px 0;">
            <button onclick="toggleMute()" id="m-btn" style="width:50px; height:50px; border-radius:50%; border:none; background:#222; color:white;">🎤</button>
            <button onclick="toggleCam()" id="v-btn" style="width:50px; height:50px; border-radius:50%; border:none; background:#222; color:white;">📷</button>
            <button onclick="window.location.reload()" style="width:50px; height:50px; border-radius:50%; border:none; background:#ff4b4b; color:white;">❌</button>
        </div>

        <input type="text" id="dest-phone" placeholder="Numéro à appeler..." style="width:100%; padding:12px; border-radius:10px; border:1px solid #333; background:#111; color:white; margin-bottom:10px;">
        <button onclick="callUser()" style="width:100%; padding:12px; border-radius:10px; border:none; background:white; color:black; font-weight:bold;">LANCER L'APPEL</button>
    </div>

    <div id="chat-box" style="margin-top:20px; height:150px; overflow-y:auto; background:#0a0a0a; border-radius:15px; padding:10px; font-size:14px; color:#ccc; border:1px solid #111;"></div>

    <script>
        var peer, conn, localStream;
        var mActive = true, vActive = true;

        function startSovereign() {
            const phone = document.getElementById('my-phone').value;
            if(!phone) return;
            
            peer = new Peer('SOV-' + phone);
            
            peer.on('open', id => {
                document.getElementById('setup-zone').style.display = 'none';
                document.getElementById('call-zone').style.display = 'block';
            });

            peer.on('call', call => {
                navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(stream => {
                    localStream = stream;
                    document.getElementById('localVideo').srcObject = stream;
                    call.answer(stream);
                    call.on('stream', rem => document.getElementById('remoteVideo').srcObject = rem);
                });
            });

            peer.on('connection', c => {
                conn = c;
                conn.on('data', data => {
                    document.getElementById('chat-box').innerHTML += "<div><b>Lui:</b> "+data+"</div>";
                });
            });
        }

        function callUser() {
            const dest = 'SOV-' + document.getElementById('dest-phone').value;
            conn = peer.connect(dest);
            
            navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(stream => {
                localStream = stream;
                document.getElementById('localVideo').srcObject = stream;
                const call = peer.call(dest, stream);
                call.on('stream', rem => document.getElementById('remoteVideo').srcObject = rem);
            });
        }

        function toggleMute() {
            mActive = !mActive;
            localStream.getAudioTracks()[0].enabled = mActive;
            document.getElementById('m-btn').style.background = mActive ? "#222" : "#ff4b4b";
        }

        function toggleCam() {
            vActive = !vActive;
            localStream.getVideoTracks()[0].enabled = vActive;
            document.getElementById('v-btn').style.background = vActive ? "#222" : "#ff4b4b";
        }
    </script>
""", height=800)

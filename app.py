import streamlit as st
import streamlit.components.v1 as components

# --- 1. INTERFACE LOOK & FEEL ---
st.set_page_config(page_title="SOVEREIGN WHATSAPP", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    /* CENTRAGE SMARTPHONE */
    .main .block-container {
        max-width: 450px !important;
        margin: auto !important;
        padding: 0px !important;
        height: 100vh;
        border-left: 1px solid #222;
        border-right: 1px solid #222;
    }

    /* BARRE DE STATUT SOVEREIGN */
    .status-bar {
        background: #075E54; /* Vert WhatsApp Original */
        padding: 15px;
        font-weight: 900;
        font-size: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. LE MOTEUR WHATSAPP (JS + LOCALSTORAGE) ---
components.html("""
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    
    <div id="app" style="color:white; display:flex; flex-direction:column; height:95vh;">
        
        <div id="header" style="background:#075E54; padding:15px; font-weight:bold; display:flex; justify-content:space-between; align-items:center;">
            <span>Sovereign</span>
            <span id="my-display-num" style="font-size:12px; opacity:0.8;">Non connecté</span>
        </div>

        <div id="login-view" style="padding:40px 20px; text-align:center;">
            <h2 style="margin-bottom:30px;">Bienvenue</h2>
            <input type="text" id="my-num" placeholder="Ton numéro..." style="width:100%; padding:15px; border-radius:10px; border:none; background:#1a1a1a; color:white; font-size:18px; margin-bottom:15px;">
            <button onclick="initApp()" style="width:100%; padding:15px; border-radius:10px; border:none; background:#25D366; color:white; font-weight:bold; cursor:pointer;">COMMENCER</button>
        </div>

        <div id="chats-view" style="display:none; flex:1; flex-direction:column;">
            <div style="padding:15px; border-bottom:1px solid #222;">
                <input type="text" id="new-friend" placeholder="Ajouter un numéro..." style="width:70%; padding:10px; border-radius:10px; border:none; background:#1a1a1a; color:white;">
                <button onclick="addChat()" style="width:25%; padding:10px; border-radius:10px; border:none; background:#fff; color:#000; font-weight:bold;">+</button>
            </div>
            <div id="chat-list" style="flex:1; overflow-y:auto;">
                </div>
        </div>

        <div id="private-chat-view" style="display:none; flex:1; flex-direction:column; background:#0d0d0d;">
            <div style="padding:10px; background:#1a1a1a; display:flex; align-items:center; gap:10px;">
                <button onclick="backToChats()" style="background:none; border:none; color:#25D366; font-size:20px; cursor:pointer;">←</button>
                <div id="active-contact-name" style="font-weight:bold;">Ami</div>
                <button onclick="startVideoCall()" style="margin-left:auto; background:none; border:none; font-size:20px;">📹</button>
            </div>

            <div id="video-box" style="display:none; height:200px; background:#000; position:relative;">
                <video id="remoteVideo" autoplay playsinline style="width:100%; height:100%; object-fit:cover;"></video>
                <video id="localVideo" autoplay playsinline muted style="width:70px; position:absolute; bottom:5px; right:5px; border:1px solid #25D366; border-radius:10px;"></video>
            </div>

            <div id="msg-history" style="flex:1; overflow-y:auto; padding:15px; display:flex; flex-direction:column; gap:8px;"></div>
            
            <div style="padding:10px; display:flex; gap:8px; background:#1a1a1a;">
                <input type="text" id="msg-input" placeholder="Message..." style="flex:1; padding:12px; border-radius:20px; border:none; background:#000; color:white;">
                <button onclick="send()" style="background:#25D366; border:none; border-radius:50%; width:45px; height:45px; color:white; cursor:pointer;">➔</button>
            </div>
        </div>
    </div>

    <script>
        var peer, conn, myNum, localStream;
        var conversations = JSON.parse(localStorage.getItem('sov_v7_chats') || '{}');
        var activePeer = null;

        function initApp() {
            myNum = document.getElementById('my-num').value;
            if(!myNum) return;
            peer = new Peer('SOV-' + myNum);
            
            peer.on('open', id => {
                document.getElementById('login-view').style.display = 'none';
                document.getElementById('chats-view').style.display = 'flex';
                document.getElementById('my-display-num').innerText = "ID: " + myNum;
                renderChatList();
            });

            peer.on('connection', c => {
                c.on('data', data => handleIncoming(c.peer.replace('SOV-',''), data));
            });

            peer.on('call', call => {
                navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(s => {
                    localStream = s;
                    document.getElementById('localVideo').srcObject = s;
                    document.getElementById('video-box').style.display = 'block';
                    call.answer(s);
                    call.on('stream', rem => document.getElementById('remoteVideo').srcObject = rem);
                });
            });
        }

        function addChat() {
            let num = document.getElementById('new-friend').value;
            if(num && !conversations[num]) {
                conversations[num] = [];
                save();
                renderChatList();
            }
        }

        function renderChatList() {
            const list = document.getElementById('chat-list');
            list.innerHTML = "";
            Object.keys(conversations).forEach(num => {
                let div = document.createElement('div');
                div.style = "padding:20px; border-bottom:1px solid #111; cursor:pointer; display:flex; align-items:center; gap:15px;";
                div.innerHTML = `<div style="width:45px; height:45px; background:#333; border-radius:50%;"></div> <div><b>${num}</b><br><small style="color:#666;">Cliquer pour discuter</small></div>`;
                div.onclick = () => openChat(num);
                list.appendChild(div);
            });
        }

        function openChat(num) {
            activePeer = num;
            document.getElementById('chats-view').style.display = 'none';
            document.getElementById('private-chat-view').style.display = 'flex';
            document.getElementById('active-contact-name').innerText = num;
            conn = peer.connect('SOV-' + num);
            renderMessages();
        }

        function backToChats() {
            document.getElementById('private-chat-view').style.display = 'none';
            document.getElementById('chats-view').style.display = 'flex';
            activePeer = null;
        }

        function send() {
            let input = document.getElementById('msg-input');
            let val = input.value;
            if(!val || !conn) return;
            conn.send(val);
            pushMsg(activePeer, 'me', val);
            input.value = "";
        }

        function handleIncoming(from, msg) {
            if(!conversations[from]) conversations[from] = [];
            pushMsg(from, 'them', msg);
        }

        function pushMsg(target, side, text) {
            conversations[target].push({side, text});
            save();
            if(activePeer === target) renderMessages();
        }

        function renderMessages() {
            const box = document.getElementById('msg-history');
            box.innerHTML = "";
            conversations[activePeer].forEach(m => {
                let d = document.createElement('div');
                d.style = `padding:10px 15px; border-radius:15px; max-width:80%; margin-bottom:5px; font-size:14px;`;
                if(m.side === 'me') {
                    d.style.background = "#056162"; d.style.alignSelf = "flex-end";
                } else {
                    d.style.background = "#262d31"; d.style.alignSelf = "flex-start";
                }
                d.innerText = m.text;
                box.appendChild(d);
            });
            box.scrollTop = box.scrollHeight;
        }

        function startVideoCall() {
            document.getElementById('video-box').style.display = 'block';
            navigator.mediaDevices.getUserMedia({video:true, audio:true}).then(s => {
                localStream = s;
                document.getElementById('localVideo').srcObject = s;
                let call = peer.call('SOV-' + activePeer, s);
                call.on('stream', rem => document.getElementById('remoteVideo').srcObject = rem);
            });
        }

        function save() { localStorage.setItem('sov_v7_chats', JSON.stringify(conversations)); }
    </script>
""", height=850)

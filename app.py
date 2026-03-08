import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURATION & STYLE ---
st.set_page_config(page_title="SOVEREIGN P2P", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: #fff; font-family: 'Inter', sans-serif; }
    header, footer { visibility: hidden; }
    
    /* CENTRAGE ABSOLU */
    .main .block-container {
        max-width: 500px !important;
        margin: auto !important;
        padding-top: 2rem !important;
    }

    .mega-title {
        font-weight: 900; font-size: 50px; text-align: center;
        background: linear-gradient(180deg, #fff 0%, #333 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -3px; margin-bottom: 0;
    }

    .id-display {
        text-align: center; color: #00ff88; font-family: monospace;
        background: #111; border-radius: 10px; padding: 10px; margin-top: 10px;
    }

    /* ZONE DE CHAT */
    #chat-box {
        height: 400px; overflow-y: auto; border: 1px solid #222;
        padding: 15px; border-radius: 15px; background: #050505;
        display: flex; flex-direction: column; gap: 10px;
    }

    .msg { padding: 10px 15px; border-radius: 15px; max-width: 80%; font-size: 14px; }
    .sent { background: #1a1a1a; align-self: flex-end; border: 1px solid #333; }
    .recv { background: #0056b3; align-self: flex-start; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="mega-title">SOVEREIGN</div>', unsafe_allow_html=True)

# --- 2. LE MOTEUR DE CONNEXION (JAVASCRIPT PEERJS) ---
# Ce code permet la communication réelle entre deux onglets/appareils
st.components.v1.html("""
    <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
    
    <div style="color:white; font-family:sans-serif;">
        <div id="my-id-label" class="id-display" style="background:#111; color:#00ff88; padding:10px; border-radius:10px; text-align:center; font-family:monospace; margin-bottom:20px;">Génération de votre ID...</div>
        
        <div style="display:flex; gap:10px; margin-bottom:20px;">
            <input type="text" id="dest-id" placeholder="ID de votre ami" style="flex:1; padding:10px; border-radius:10px; border:1px solid #333; background:#000; color:white;">
            <button onclick="connectToPeer()" style="padding:10px; border-radius:10px; border:none; background:#fff; color:#000; font-weight:bold; cursor:pointer;">Connecter</button>
        </div>

        <div id="chat-box" style="height:300px; border:1px solid #222; border-radius:15px; padding:15px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; background:#050505;">
            <div style="color:#555; text-align:center; font-size:12px;">Système : En attente de connexion...</div>
        </div>

        <div style="display:flex; gap:10px; margin-top:20px;">
            <input type="text" id="msg-input" placeholder="Écrire un message..." style="flex:1; padding:10px; border-radius:10px; border:1px solid #333; background:#000; color:white;">
            <button onclick="sendMessage()" style="padding:10px; border-radius:10px; border:none; background:#00ff88; color:#000; font-weight:bold; cursor:pointer;">Encaisser</button>
        </div>
    </div>

    <script>
        var peer = new Peer();
        var conn;
        var chatBox = document.getElementById('chat-box');
        var myIdLabel = document.getElementById('my-id-label');

        // 1. Récupérer mon ID
        peer.on('open', function(id) {
            myIdLabel.innerHTML = "VOTRE ID : " + id;
        });

        // 2. Attendre une connexion entrante
        peer.on('connection', function(c) {
            conn = c;
            setupChat();
        });

        // 3. Fonction pour se connecter à un ami
        function connectToPeer() {
            var destId = document.getElementById('dest-id').value;
            conn = peer.connect(destId);
            setupChat();
        }

        function setupChat() {
            conn.on('open', function() {
                chatBox.innerHTML += '<div style="color:#00ff88; text-align:center; font-size:12px;">Connecté à ' + conn.peer + '</div>';
                
                conn.on('data', function(data) {
                    addMessage(data, 'recv');
                });
            });
        }

        function sendMessage() {
            var input = document.getElementById('msg-input');
            var msg = input.value;
            if (conn && conn.open) {
                conn.send(msg);
                addMessage(msg, 'sent');
                input.value = "";
            }
        }

        function addMessage(msg, type) {
            var div = document.createElement('div');
            div.style.padding = "10px 15px";
            div.style.borderRadius = "15px";
            div.style.maxWidth = "80%";
            div.style.fontSize = "14px";
            
            if (type === 'sent') {
                div.style.background = "#1a1a1a";
                div.style.alignSelf = "flex-end";
                div.style.border = "1px solid #333";
            } else {
                div.style.background = "#0056b3";
                div.style.alignSelf = "flex-start";
            }
            
            div.innerText = msg;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
""", height=600)

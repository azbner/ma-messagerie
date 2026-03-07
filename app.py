import streamlit as st
import streamlit.components.v1 as components

# Cache l'interface Streamlit pour un look application mobile
st.set_page_config(page_title="Sovereign Messenger", layout="centered")
st.markdown("<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>", unsafe_allow_html=True)

# Ton code HTML/JS complet (Vidéo + Vocal + Micro)
html_code = """
<!DOCTYPE html>
<html>
<head>
    </head>
<body>
    </body>
</html>
"""

# Affiche ton interface dans Streamlit
components.html(html_code, height=850, scrolling=False)

import streamlit as st
import streamlit.components.v1 as components

# Ton code HTML doit être stocké dans cette variable
html_code = """
<!DOCTYPE html>
<html>
[TOUT TON CODE ICI]
</html>
""" # <--- Vérifie bien qu'il y a 3 guillemets ici

components.html(html_code, height=800)

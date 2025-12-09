import streamlit as st
from pathlib import Path
from PIL import Image

# ---------------------------
# Configuration générale
# ---------------------------
st.set_page_config(
    page_title="ModernBERT - Analyse de sentiments (Sentiment140)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# En-tête et présentation
# ---------------------------
st.title("ModernBERT – Analyse de sentiments sur Sentiment140")
st.markdown("---")

col1, col2 = st.columns([1, 2])
with col1:
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), caption="POC - Sentiment140", width=200)
with col2:
    st.markdown("""
    ###Objectif du projet###
    Ce **POC** vise à comparer BERT et ModernBERT pour
    l’analyse du sentiment de tweets.

    Le modèle ModernBERT est comparé au modèle classique BERT sur plusieurs métriques :
    * **ROC-AUC**
    * **F1-score**
    * **Accuracy**
    * **Precision**
    * **Latence (s)**

    🧩 L’application permet :
    - D’explorer le dataset (analyse exploratoire interactive)  
    - De comparer les modèles BERT et ModernBERT  
    - D’illustrer la prise en compte de l’**accessibilité (WCAG 2.1 AA)**
    """)

st.markdown("---")

# ---------------------------
# Navigation & structure du projet
# ---------------------------
st.header("Structure de l’application")

st.markdown("""
**Analyse exploratoire** – Visualisation du dataset Sentiment140  
**Comparaison des modèles** – BERT vs ModernBERT  
**Accessibilité & Design** – Respect des critères WCAG et ergonomie  
""")

# ---------------------------
# Accessibilité : thème et préférences utilisateur
# ---------------------------
st.markdown("---")
st.subheader("Paramètres d’accessibilité")

colA, colB = st.columns(2)
with colA:
    theme = st.radio(
        "Thème d’affichage",
        ["Clair", "Sombre"],
        help="Choisissez le mode visuel selon votre confort."
    )

with colB:
    font_size = st.slider(
        "Taille du texte",
        min_value=12,
        max_value=22,
        value=16,
        step=2,
        help="Ajustez la taille du texte pour une meilleure lisibilité."
    )

st.markdown(
    f"<style>html, body, [class*='css']  {{ font-size: {font_size}px; }}</style>",
    unsafe_allow_html=True
)

if theme == "Sombre":
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;
            color: #EAEAEA;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# Call-to-action
# ---------------------------
st.markdown("---")
st.markdown("### Prêt à explorer le POC ?")

if st.button("Lancer l'analyse exploratoire"):
    st.switch_page("pages/01_analyse.py")


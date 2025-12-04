import streamlit as st
from pathlib import Path
from PIL import Image

# ---------------------------
# Configuration générale
# ---------------------------
st.set_page_config(
    page_title="ModernBERT - Analyse de sentiments (Sentiment140)",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# En-tête et présentation
# ---------------------------
st.title("🧠 ModernBERT – Analyse de sentiments sur Sentiment140")
st.markdown("---")

col1, col2 = st.columns([1, 2])
with col1:
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), caption="POC - Sentiment140", width=200)
with col2:
    st.markdown("""
    ### 🎯 Objectif du projet
    Ce **Proof of Concept (POC)** vise à démontrer l’efficacité du modèle **ModernBERT** pour
    l’analyse automatique du **sentiment de tweets** issus du jeu de données **Sentiment140**.

    Le modèle ModernBERT est comparé au modèle classique BERT sur plusieurs métriques :
    * **ROC-AUC**
    * **F1-score**
    * **Accuracy**
    * **Precision**
    * **Latence (s)**

    🧩 L’application permet :
    - D’explorer le dataset (analyse exploratoire interactive)  
    - De tester le moteur de prédiction en temps réel  
    - De comparer les modèles BERT et ModernBERT  
    - D’illustrer la prise en compte de l’**accessibilité (WCAG 2.1 AA)**
    """)

st.markdown("---")

# ---------------------------
# Navigation & structure du projet
# ---------------------------
st.header("📁 Structure de l’application")

st.markdown("""
L’application Streamlit se compose de **4 modules principaux** accessibles via le menu latéral :

1️⃣ **Analyse exploratoire** – Visualisation du dataset Sentiment140  
2️⃣ **Prédiction en temps réel** – Testez un tweet ou un fichier CSV  
3️⃣ **Comparaison des modèles** – BERT vs ModernBERT  
4️⃣ **Accessibilité & Design** – Respect des critères WCAG et ergonomie  

👉 Utilisez le menu latéral de Streamlit (à gauche) pour naviguer entre les pages.
""")

# ---------------------------
# Accessibilité : thème et préférences utilisateur
# ---------------------------
st.markdown("---")
st.subheader("♿ Paramètres d’accessibilité")

st.markdown("""
Pour favoriser l’inclusion, cette application intègre plusieurs options d’**accessibilité** :
""")

colA, colB = st.columns(2)
with colA:
    theme = st.radio(
        "🎨 Thème d’affichage",
        ["Clair", "Sombre"],
        help="Choisissez le mode visuel selon votre confort."
    )

with colB:
    font_size = st.slider(
        "🔠 Taille du texte",
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
st.markdown("### 🚀 Prêt à explorer le POC ?")

if st.button("➡️ Lancer l'analyse exploratoire"):
    st.switch_page("pages/01_📊_Analyse_Exploratoire.py")

st.info(
    "💡 Astuce : vous pouvez également accéder directement aux autres modules via la barre latérale."
)

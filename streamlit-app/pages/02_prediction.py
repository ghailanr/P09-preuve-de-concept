import streamlit as st
import pandas as pd
import numpy as np
from utils.accessibility import describe_accessibility_features
from utils.visualization import accessible_color_palette
import time
import requests



API_URL = "fastapi-p9-cbhtewcmgdbnephz.germanywestcentral-01.azurewebsites.net/predict/"
# ---------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------
st.set_page_config(
    page_title="Prédiction en temps réel",
    layout="wide"
)
st.title("Prédiction en temps réel du sentiment d’un tweet")
st.markdown("---")

# ---------------------------
# INTRODUCTION
# ---------------------------
st.markdown("""
Cette page vous permet de **tester le modèle ModernBERT** sur un ou plusieurs tweets.  
Vous pouvez saisir manuellement un texte ou importer un fichier CSV contenant une colonne `text`.
""")

st.info("Le modèle utilisé ici est la version ModernBERT entraînée sur le jeu de données Sentiment140.")

# ---------------------------
# SECTION 1 : SAISIE D’UN TWEET
# ---------------------------
st.subheader("Prédiction sur un tweet unique")

tweet_input = st.text_area(
    "Entrez un tweet à analyser :",
    placeholder="Ex : I love this new phone, it’s amazing!",
    height=100
)


def predict_sentient(text: str):
    try:
        response = requests.post(API_URL, data=tweet_input)
        response.raise_for_status()
        return response.content

    except requests.exceptions.RequestException as e:
        st.error(f"Error during API request: {e}")


if st.button("🔍 Analyser le sentiment"):
    if tweet_input.strip() == "":
        st.warning("Veuillez entrer un texte avant de lancer la prédiction.")
    else:
        with st.spinner("Analyse en cours..."):
            sentiment = predict_sentient(tweet_input)

        st.success(f"✅ **Sentiment prédit : {sentiment}**")

        # Affichage accessible
        palette = accessible_color_palette()
        color_map = {
            "POSITIF": palette[2],
            "NEGATIF": palette[3],
        }
        st.markdown(
            f"""
            <div style='background-color:{color_map[sentiment]};padding:1rem;border-radius:10px;color:white;'>
            Prédiction ModernBERT : <b>{sentiment}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------
# SECTION 2 : PRÉDICTION PAR FICHIER CSV
# ---------------------------
st.markdown("---")
st.subheader("📂 Prédiction sur un fichier CSV")

uploaded_file = st.file_uploader("Téléversez un fichier CSV contenant une colonne `text` :", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if "tweet" not in df.columns:
        st.error("Le fichier doit contenir une colonne nommée `tweet`.")
    else:
        st.success(f"Fichier chargé avec {len(df)} lignes.")

        if st.button("Lancer la prédiction sur le fichier"):
            with st.spinner("Prédictions en cours..."):
                time.sleep(2)
                df["predicted_label"] = [predict_sentient(x) for x in df["tweet"]]
            st.dataframe(df.head(10), use_container_width=True)

            # Téléchargement du résultat
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Télécharger les prédictions",
                data=csv,
                file_name="predictions_modernbert.csv",
                mime="text/csv"
            )

# ---------------------------
# SECTION 3 : ACCESSIBILITÉ
# ---------------------------
describe_accessibility_features()

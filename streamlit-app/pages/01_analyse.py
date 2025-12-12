import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from utils.visualization import (
    plot_class_distribution,
    plot_length_distribution,
    plot_word_frequency
)
from utils.accessibility import apply_accessibility_settings
from utils.theme import apply_theme
apply_theme()
# ---------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------
st.title("Analyse exploratoire du jeu de données Sentiment140")
st.markdown("---")

# ---------------------------
# CHARGEMENT DES DONNÉES
# ---------------------------
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    return df

data_path = "streamlit-app/data/sentiment140_sampled.zip"
df = load_data(data_path)

# ---------------------------
# APERÇU RAPIDE DU JEU DE DONNÉES
# ---------------------------
st.subheader("Aperçu du jeu de données")
st.dataframe(df.sample(5), width='content')

# ---------------------------
# SECTION 1 : LONGUEUR DES TWEETS
# ---------------------------
st.markdown("### Analyse 1 — Distribution de la longueur des tweets")

# Calcul de la longueur
df["tweet_length"] = df["tweet"].astype(str).apply(len)

fig_len = plot_length_distribution(df, "tweet_length")
st.plotly_chart(fig_len, width='content')

st.caption("Ce graphique montre la distribution du nombre de caractères par tweet.")

# ---------------------------
# SECTION 2 : FRÉQUENCE DES MOTS PAR SENTIMENT
# ---------------------------
st.markdown("### Analyse 2 — Fréquence des mots selon le sentiment")

sentiments = df["target"].unique()
sent_choice = st.selectbox("Choisir un sentiment à explorer :", sentiments)

fig_freq = plot_word_frequency(df, sentiment_col="target", text_col="tweet", sentiment_value=sent_choice)
st.plotly_chart(fig_freq, width='content')

st.caption("Ce graphique présente les mots les plus fréquents pour le sentiment sélectionné.")

# ---------------------------
# SECTION 3 : WORDCLOUD GLOBAL
# ---------------------------
st.markdown("### Analyse 3 — Nuage de mots global")

text_data = " ".join(df["tweet"].astype(str).tolist())

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white",
    max_words=200,
    colormap="viridis"
).generate(text_data)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)
st.caption("Représentation visuelle des mots les plus fréquents dans l’ensemble des tweets.")

import streamlit as st
import pandas as pd
import altair as alt
from utils.theme import apply_theme
apply_theme()

st.title("Comparaison BERT vs ModernBERT sur Sentiment140")

# ---------------------------------
# Chargement des données
# ---------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("streamlit-app/data/sample_dashboard.csv")

df = load_data()

# ---------------------------------
# Metrics globales
# ---------------------------------
st.header("Performance globale")

def compute_accuracy(col):
    return (df[col] == df["target"]).mean()

bert_acc = compute_accuracy("bert_prediction")
modernbert_acc = compute_accuracy("modernbert_prediction")

col1, col2 = st.columns(2)
col1.metric("Accuracy BERT", f"{bert_acc:.2%}")
col2.metric("Accuracy ModernBERT", f"{modernbert_acc:.2%}")

# ---------------------------------
# Matrice des erreurs
# ---------------------------------
st.header("Erreurs de classification")

df_errors = df[
    (df["bert_prediction"] != df["target"]) |
    (df["modernbert_prediction"] != df["target"])
]

st.write("Tweets sur lesquels au moins un des deux modèles s'est trompé :")
st.dataframe(df_errors)

# ---------------------------------
# Comparaison détaillée
# ---------------------------------
st.header("BERT vs ModernBERT — Cas où ModernBERT corrige BERT")

df_better = df[
    (df["bert_prediction"] != df["target"]) &
    (df["modernbert_prediction"] == df["target"])
]

st.write(f"Nombre de cas où ModernBERT corrige BERT : **{len(df_better)}**")

st.dataframe(df_better[["text", "target", "bert_prediction", "modernbert_prediction"]])

# ---------------------------------
# Visualisation interactive
# ---------------------------------
df_viz = df.copy()
df_viz["bert_correct"] = (df_viz["bert_prediction"] == df_viz["target"])
df_viz["modern_correct"] = (df_viz["modernbert_prediction"] == df_viz["target"])

df_viz["category"] = df_viz.apply(
    lambda row:
        "ModernBERT corrige BERT" if (not row["bert_correct"] and row["modern_correct"])
        else "BERT corrige ModernBERT" if (row["bert_correct"] and not row["modern_correct"])
        else "Les deux corrects" if (row["bert_correct"] and row["modern_correct"])
        else "Les deux incorrects",
    axis=1
)

cat_df = df_viz["category"].value_counts().reset_index()
cat_df.columns = ["category", "count"]

chart3 = alt.Chart(cat_df).mark_bar().encode(
    y="category:N",
    x="count:Q",
    color="category:N",
    tooltip=["category", "count"]
).properties(title="Répartition des types d'erreurs")

st.altair_chart(chart3, width='content')


# ---------------------------------
# Analyse d’un tweet au choix
# ---------------------------------
st.header("Analyse d'un tweet spécifique")

tweet_text = st.selectbox("Choisir un tweet :", df["text"].tolist())

tweet_row = df[df["text"] == tweet_text].iloc[0]

st.write("**Tweet :** ", tweet_text)
st.write("**Label réel :** ", tweet_row["target"])
st.write("**Prévision BERT :** ", tweet_row["bert_prediction"])
st.write("**Prévision ModernBERT :** ", tweet_row["modernbert_prediction"])

from collections import Counter

import pandas as pd
import plotly.express as px
from accessibility import accessible_color_palette

# importe la palette accessible depuis le module accessibility (single source of truth)


def plot_word_frequency(df: pd.DataFrame, sentiment_col: str, text_col: str, sentiment_value: str, top_n: int = 20):
    """
    Calcule et trace les mots les plus fréquents pour un sentiment donné.
    (Utilisé dans la section "analyse textuelle" de la page EDA)
    """
    subset = df[df[sentiment_col] == sentiment_value]
    words = " ".join(subset[text_col].astype(str)).split()
    counter = Counter(words)
    common = counter.most_common(top_n)
    word_df = pd.DataFrame(common, columns=["word", "frequency"])

    palette = accessible_color_palette()
    color = palette[0] if palette else None

    fig = px.bar(
        word_df,
        x="word",
        y="frequency",
        title=f"Mots les plus fréquents ({sentiment_value})",
    )
    if color:
        fig.update_traces(marker_color=color)
    fig.update_layout(xaxis_tickangle=-45)
    return fig


def plot_class_distribution(df: pd.DataFrame, label_col: str):
    """
    Bar chart de la répartition des classes (sentiments).
    """
    counts = df[label_col].value_counts().reset_index()
    counts.columns = [label_col, "count"]
    palette = accessible_color_palette()
    fig = px.bar(
        counts,
        x=label_col,
        y="count",
        title="Répartition des sentiments",
    )
    if palette:
        fig.update_traces(marker_color=palette[0])
    return fig


def plot_length_distribution(df: pd.DataFrame, length_col: str):
    """
    Histogramme de la distribution des longueurs de tweets.
    """
    fig = px.histogram(
        df,
        x=length_col,
        nbins=40,
        title="Distribution de la longueur des tweets",
        labels={length_col: "Longueur du tweet", "count": "Nombre"}
    )
    return fig

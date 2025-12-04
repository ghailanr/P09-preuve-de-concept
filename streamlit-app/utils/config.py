# Fichier de configuration central du projet Streamlit

# Fichier CSV par défaut (échantillon du dataset Sentiment140)
DEFAULT_DATA_PATH = "data/sentiment140_sample.csv"

# Colonnes attendues
TEXT_COLUMN = "text"
LABEL_COLUMN = "sentiment"

# Étiquettes standardisées
LABELS = {
    0: "NEGATIF",
    1: "POSITIF"
}

# Nombre maximum de mots dans les WordClouds
MAX_WORDCLOUD_WORDS = 100

# Palette de couleurs accessible pour les visualisations
ACCESSIBLE_COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"
]

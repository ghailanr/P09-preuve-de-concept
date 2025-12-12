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
    logo_path = Path("./streamlit-app/assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), caption="POC - Sentiment140", width=400)
with col2:
    st.markdown("""
    Ce **POC** vise à comparer BERT et ModernBERT pour
    l’analyse du sentiment de tweets.

    Le modèle ModernBERT est comparé au modèle classique BERT sur plusieurs métriques :
    * **ROC-AUC**
    * **F1-score**
    * **Accuracy**
    * **Precision**
    * **Latence (s)**

    L’application permet :
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
if "theme" not in st.session_state:
    st.session_state.theme = "Clair"

# Mémoriser le choix
with colA:
    theme = st.radio(
        "Thème d’affichage",
        ["Clair", "Sombre", "Auto"],
        index=0,
        help="Choisissez le mode visuel."
    )

st.session_state.theme = theme

if "font_size" not in st.session_state:
    st.session_state.font_size = 16

with colB:
    font_size = st.slider(
        "Taille du texte",
        min_value=12,
        max_value=22,
        value=16,
        step=2,
        help="Ajustez la taille du texte."
    )
    
st.session_state.font_size = font_size

# ---------------------------
# Font size — n'affecte pas les couleurs
# ---------------------------
st.markdown(
    f"""
    <style>
        html, body, .stApp {{
            font-size: {font_size}px !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 🎨 MODE CLAIR — complètement corrigé
# ---------------------------
if theme == "Clair":
    light_css = """
    <style>

    /* FOND GÉNÉRAL */
    body, .main, .block-container {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* TITRES */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    /* TOUS LES LABELS STREAMLIT (radios, sliders, selectbox, textes explicatifs) */
    label, .stMarkdown, .stRadio, .stSlider, .stSelectbox, .css-1n76uvr, .css-16idsys, .css-10trblm, .css-1p4hspd {
        color: #000000 !important;
    }

    /* TEXTE À L’INTÉRIEUR DES INPUTS */
    input, textarea, select {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* SPÉCIFIQUE AUX WIDGETS STREAMLIT */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input,
    .stSlider>div>div>div,
    .stSlider>label {
        color: #000000 !important;
    }

    /* SLIDER — le label "Taille du texte" */
    .stSlider label div {
        color: #000000 !important;
        font-weight: 500 !important;
    }

    /* OPTIONS DES RADIO BUTTONS */
    .stRadio>div>label, .stRadio>div>div>div {
        color: #000000 !important;
    }

    /* ICÔNES ET PETITS TEXTES STREAMLIT */
    .css-1emrehy, .css-1kyxreq, .small-font {
        color: #000000 !important;
    }

    /* BOUTONS */
    .stButton>button {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        border: 1px solid #CCC !important;
    }

    /* DATAFRAMES */
    .dataframe tbody tr,
    .dataframe thead tr,
    .dataframe td {
        background: #FFFFFF !important;
        color: #000000 !important;
    }

    /* CHARTS ALTAIR — TITRES & LABELS */
    .mark-text, .role-title, .role-axis-label, .role-legend-label {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* AIDES (help=...) */
    .stTooltipContent, .css-qrbaxs, .css-1d391kg {
        color: #000000 !important;
    }

    /* SÉPARATEURS */
    hr {
        border-color: #DDD !important;
    }

    </style>
    """
    st.markdown(light_css, unsafe_allow_html=True)

# ---------------------------
# 🎨 MODE SOMBRE
# ---------------------------
elif theme == "Sombre":
    st.markdown(
        """
        <style>
        body, .stApp {
            background-color: #121212 !important;
            color: #EAEAEA !important;
        }

        label,
        .stRadio > div,
        .stSlider label,
        .stSelectbox label,
        .stTextInput label {
            color: #EAEAEA !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# 🎨 MODE AUTO
# ---------------------------
else:
    st.markdown(
        """
        <style>
        @media (prefers-color-scheme: dark) {
            body, .stApp {
                background-color: #121212 !important;
                color: #EAEAEA !important;
            }
            label, .stRadio > div, .stSlider label {
                color: #EAEAEA !important;
            }
            h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
        }

        @media (prefers-color-scheme: light) {
            body, .stApp {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            label, .stRadio > div, .stSlider label {
                color: #000000 !important;
            }
            h1, h2, h3, h4, h5, h6 { color: #000000 !important; }
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


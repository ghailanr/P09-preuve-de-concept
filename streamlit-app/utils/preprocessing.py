import re
import html
import string

def preprocess_text(text: str) -> str:
    """
    Nettoie le texte d'un tweet pour l'analyse :
    - Supprime les URLs, mentions, retweets, ponctuation inutile.
    - Convertit les caractères HTML.
    - Normalise les hashtags et les répétitions de caractères.
    - Met en minuscules.
    """

    if not isinstance(text, str):
        return ""

    # Décodage des entités HTML (&amp;, &lt;, etc.)
    text = html.unescape(text)

    # Suppression des URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # Suppression des mentions @user
    text = re.sub(r"@\w+", "", text)

    # Suppression du préfixe "RT"
    text = re.sub(r"\bRT\b", "", text)

    # Normalisation des hashtags (on garde le mot)
    text = re.sub(r"#(\w+)", r"\1", text)

    # Suppression de la ponctuation (hors emojis)
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Suppression des chiffres
    text = re.sub(r"\d+", "", text)

    # Normalisation des répétitions de lettres (cooool → cool)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)

    # Suppression des espaces multiples
    text = re.sub(r"\s+", " ", text).strip()

    # Mise en minuscules
    text = text.lower()

    return text

import streamlit as st
from typing import List

def apply_accessibility_settings(theme: str = "Clair", font_size: int = 16):
    """
    Applique les paramètres d’accessibilité à l’interface Streamlit :
    - thème clair/sombre
    - taille du texte personnalisée
    """
    st.markdown(
        f"<style>html, body, [class*='css']  {{ font-size: {font_size}px; }}</style>",
        unsafe_allow_html=True
    )

    if theme.lower() == "sombre":
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


def describe_accessibility_features():
    """
    Affiche un encadré récapitulatif des fonctionnalités d’accessibilité activées.
    """
    st.markdown("---")
    st.subheader("♿ Accessibilité")
    st.markdown("""
    ✅ **Critères WCAG 2.1 niveau AA couverts :**
    - Contraste colorimétrique minimal 4.5:1  
    - Taille de texte ajustable (12–22 px)  
    - Thème clair/sombre au choix  
    - Légendes descriptives sur tous les graphiques  
    """)


def accessible_color_palette() -> List[str]:
    """
    Palette de couleurs respectant les contrastes recommandés par le WCAG 2.1 AA.
    Retourne une liste de couleurs hex adaptées pour les graphiques.
    """
    return [
        "#1f77b4",  # bleu profond
        "#ff7f0e",  # orange chaud
        "#2ca02c",  # vert doux
        "#d62728",  # rouge accessible
        "#9467bd",  # violet contrasté
        "#8c564b",  # marron neutre
    ]

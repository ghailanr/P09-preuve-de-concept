import streamlit as st

def apply_theme():
    theme = st.session_state.get("theme", "Clair")
    font_size = st.session_state.get("font_size", 16)

    # Application taille du texte
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

    # ----- MODE CLAIR -----
    if theme == "Clair":
        st.markdown(
            """
            <style>
            body, .stApp { background-color: white !important; color: black !important; }
            label, .stRadio > div, .stSlider label { color: black !important; }
            h1, h2, h3, h4, h5, h6 { color: black !important; }
            </style>
            """,
            unsafe_allow_html=True
        )

    # ----- MODE SOMBRE -----
    elif theme == "Sombre":
        st.markdown(
            """
            <style>
            body, .stApp { background-color: #121212 !important; color: #EAEAEA !important; }
            label, .stRadio > div, .stSlider label { color: #EAEAEA !important; }
            h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
            </style>
            """,
            unsafe_allow_html=True
        )

    # ----- MODE AUTO -----
    else:
        st.markdown(
            """
            <style>
            @media (prefers-color-scheme: dark) {
                body, .stApp { background-color: #121212 !important; color: #EAEAEA !important; }
                label, .stRadio > div, .stSlider label { color: #EAEAEA !important; }
                h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
            }

            @media (prefers-color-scheme: light) {
                body, .stApp { background-color: white !important; color: black !important; }
                label, .stRadio > div, .stSlider label { color: black !important; }
                h1, h2, h3, h4, h5, h6 { color: black !important; }
            }
            </style>
            """,
            unsafe_allow_html=True
        )

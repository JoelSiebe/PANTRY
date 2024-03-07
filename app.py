import streamlit as st

# Hintergrundbild
background_url = "https://www.pexels.com/de-de/foto/top-view-foto-von-food-dessert-1099680/"

# Setze Page Config
st.set_page_config(
    layout="wide",
    page_title="Pantry Pal - Mastering Meals, Conquering Leftovers",
    initial_sidebar_state="collapsed",
)

# Hintergrundbild einfügen
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{https://www.pexels.com/de-de/foto/top-view-foto-von-food-dessert-1099680/}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Titel und Untertitel
st.title("Pantry Pal")
st.subheader("Tame your kitchen with Pantry Pal")

# App-Inhalt (ersetzen Sie diesen mit Ihren Funktionen)

# Fügen Sie hier Ihre Streamlit-Widgets, Textblöcke, Funktionen usw. ein, um die App zu gestalten.

# Beispiel:
st.write("**Pantry Pal hilft Ihnen, Ihre Speisekammer zu organisieren, Mahlzeiten zu planen und Reste zu verwerten.**")

# Fügen Sie weitere Features hinzu, um Ihre App zu individualisieren.

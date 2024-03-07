import streamlit as st

# Titel der App
st.title("Pantry Pal - Mastering Meal, Conquering Leftovers")
st.header("Tame your kitchen with Pantry Pal!")

# Hintergrundbild
background_image = "https://www.pexels.com/de-de/foto/top-view-foto-von-food-dessert-1099680/"
st.set_page_config(
    layout="wide",
    page_title="Pantry Pal",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{https://www.pexels.com/de-de/foto/top-view-foto-von-food-dessert-1099680/}");
        background-size: cover;  background-position: center;  background-repeat: no-repeat;  }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.header("Tame your kitchen with Pantry Pal!")

# Textfeld für Eingabe
name = st.text_input("Geben Sie Ihren Namen ein:")

# Begrüßungstext
st.write("Hallo " + name + "!")

# Auswahlfeld
auswahl = st.selectbox("Wählen Sie eine Farbe:", ["Rot", "Grün", "Blau"])

# Ausgabe der Auswahl
st.write("Sie haben die Farbe " + auswahl + " gewählt.")

# Button
if st.button("OK"):
    st.write("Vielen Dank!")

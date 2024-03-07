import streamlit as st

# Definiere das Hintergrundbild und den Stil
page_bg_img = """
<style>
body {
    background-image: url("https://i.postimg.cc/P5ksXpm2/pexels-vladimir-gladkov-6208084.jpg");
    background-size: cover;
}
.stApp {
    color: white;
    font-size: 18px; /* Ändere die Schriftgröße hier */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Titel und Header der Anwendung
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals",)
st.header("**Tame your kitchen with Pantry Pal**",)

# CSS-Stilregel für das Eingabefeld
st.write("""
<style>
div[data-baseweb="input"] input {
    color: black !important; /* Ändere die Schriftfarbe auf Schwarz */
    font-size: 20px !important; /* Ändere die Schriftgröße auf 20px */
}
</style>
""", unsafe_allow_html=True)

# Eingabefeld für die Kühlschrank-Zutaten mit angepasster Schriftgröße
ingredients = st.text_input("Enter your fridge ingredients, separated by comma")

# Schaltfläche, um Rezepte basierend auf den eingegebenen Zutaten anzuzeigen
if st.button("Show Recipes"):
    # Hier kannst du die Logik zum Abrufen von Rezepten basierend auf den eingegebenen Zutaten implementieren
    # In diesem Beispiel zeigen wir nur eine Platzhaltermeldung an
    st.write("Here, we will display recipes based on your ingredients")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")


import streamlit as st

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.postimg.cc/P5ksXpm2/pexels-vladimir-gladkov-6208084.jpg");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Titel und Header der Anwendung
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

# Eingabefeld für die Kühlschrank-Zutaten
ingredients = st.text_input("Geben Sie Ihre Kühlschrank-Zutaten ein, getrennt durch Komma")

# Schaltfläche, um Rezepte basierend auf den eingegebenen Zutaten anzuzeigen
# if st.button("Rezepte anzeigen"):
    # Hier können Sie die Logik zum Abrufen von Rezepten basierend auf den eingegebenen Zutaten implementieren
    # Dies umfasst die Integration der Fooddatabank-API und der Rezept-API
    # Sobald Sie Zugriff auf diese APIs haben, können Sie die entsprechenden Anfragen senden und die Ergebnisse anzeigen
    # In diesem Beispiel zeigen wir nur eine Platzhaltermeldung an
    #st.write("Hier werden die Rezepte basierend auf Ihren Zutaten angezeigt")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. Alle Rechte vorbehalten.")
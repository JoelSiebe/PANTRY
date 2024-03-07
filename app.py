import streamlit as st

# Setzen des dunkelgrünen Hintergrunds
st.markdown(
    """
    <style>
    body {
        background-color: #006400;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

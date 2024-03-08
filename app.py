import streamlit as st
import requests

# CSS-Stile
css_styles = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.postimg.cc/cJtrkLQw/pexels-mike-murray-5701888.jpg");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

.text-input-container {
    background-color: rgba(255, 255, 255, 0.5) !important;
    border-radius: 10px !important;
}

.text-input-container input {
    color: black !important; /* Schriftfarbe auf Schwarz */
    font-size: 20px !important; /* Schriftgröße auf 20px */
    background-color: rgba(200, 200, 200, 0.7) !important; /* Hintergrundfarbe mit Transparenz */
    border: none !important; /* Rand entfernen */
    border-radius: 10px !important; /* Randradius festlegen */
    padding: 10px 15px !important; /* Innenabstand anpassen */
}

h3 {
    font-size: 24px;
    color: white;
}
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# Titel und Header
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals",)
st.header("**Tame your kitchen with Pantry Pal**",)

# Zutatenliste des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)", key="ingredients", max_chars=1000)

if st.button('Show recipes'):
    if zutaten:
        # Spoonacular API-URL
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"

        #API-Schlüssel
        api_key = "06491aabe3d2435b8b21a749de46b765"

        #Datenbankabfrage
        params = {
            'ingredients': zutaten,
            'number': 5, #Anz. angezeiter Rezepte
            'apiKey': api_key
        }

        #API-Abfrage senden
        response = requests.get(api_url, params=params)
        data = response.json()

        #Rezeptvorschläge 
        st.header("Look what we've found for you")
        for recipe in data:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            st.write(f"Verwendete Zutaten: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Fehlende Zutaten: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Anzahl der fehlenden Zutaten: {recipe['missedIngredientCount']}")
            st.write(f"Anzahl der verwendeten Zutaten: {recipe['usedIngredientCount']}")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")

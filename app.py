import streamlit as st
import requests
import tempfile
import webbrowser
import os

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
    background-color: rgba(200, 200, 200, 0.8) !important;
    border-radius: 20px !important;
    padding: 20px !important;
}

.text-input-container input {
    color: black !important; /* Schriftfarbe auf Schwarz */
    font-size: 24px !important; /* Schriftgröße auf 24px */
    background-color: rgba(150, 150, 150, 0.9) !important; /* Hintergrundfarbe mit Transparenz */
    border: none !important; /* Rand entfernen */
    border-radius: 15px !important; /* Randradius festlegen */
    padding: 15px 20px !important; /* Innenabstand anpassen */
}

h2 {
    font-size: 36px;
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

        # Speichern der Rezepte in einer HTML-Datei
        html_content = "<h1>Recipes</h1>"
        for recipe in data:
            html_content += f"<h2>{recipe['title']}</h2>"
            html_content += f"<img src='{recipe['image']}'><br>"
            html_content += f"Used ingredients: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}<br>"
            html_content += f"Missing ingredients: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}<br>"
            html_content += f"Number of missing ingredients: {recipe['missedIngredientCount']}<br>"
            html_content += f"Number of used ingredients: {recipe['usedIngredientCount']}<br><br>"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            tmpfile.write(html_content.encode("utf-8"))
            file_path = tmpfile.name

        webbrowser.open_new_tab("file://" + file_path)

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")

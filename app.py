import streamlit as st
import requests

# Spoonacular API-Schlüssel einfügen
api_key = "06491aabe3d2435b8b21a749de46b765"

# Streamlit-App-Titel und Beschreibung
st.title("Rezeptfinder")
st.write("Suchen Sie nach Rezepten mit verschiedenen Parametern.")

# Suchparameter definieren
st.sidebar.text("Suchparameter:")
cuisine = st.sidebar.selectbox("Küche", ["Alle", "Italienisch", "Mexikanisch", "Thailändisch", ...])
diet = st.sidebar.selectbox("Ernährungsweise", ["Alle", "Vegetarisch", "Vegan", "Glutenfrei", ...])
include_ingredients = st.sidebar.text_input("Enthaltene Zutaten (durch Komma getrennt)")
exclude_ingredients = st.sidebar.text_input("Ausgeschlossene Zutaten (durch Komma getrennt)")
max_cook_time = st.sidebar.number_input("Maximale Zubereitungszeit (Minuten)", min_value=1)
difficulty = st.sidebar.selectbox("Schwierigkeitsgrad", ["Alle", "Leicht", "Mittel", "Schwer"])

# Spoonacular API-Abfrage erstellen
url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&cuisine={cuisine}&diet={diet}&includeIngredients={include_ingredients}&excludeIngredients={exclude_ingredients}&maxCookTime={max_cook_time}&addRecipeNutrition=true&sort=totalCookTime,asc&difficulty={difficulty}"

# API-Abfrage senden und Rezepte erhalten
response = requests.get(url)
recipes = response.json()["results"]

# Rezepte in Streamlit anzeigen
if recipes:
    for recipe in recipes:
        st.header(recipe["title"])
        st.image(recipe["image"])
        st.write(f"Zutaten: {recipe['ingredients']}")
        st.write(f"Zubereitungszeit: {recipe['totalCookTime']} Minuten")
        st.write(f"Schwierigkeitsgrad: {recipe['difficulty']}")
else:
    st.write("Keine Rezepte gefunden.")
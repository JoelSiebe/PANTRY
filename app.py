import streamlit as st
import requests

# Titel und Header
st.markdown("<h1 style='text-align: center; color: grey;'>Pantry Pal</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Conquering Leftovers, Mastering Meals</h2>", unsafe_allow_html=True)

# API-URL und API-Schlüssel für Spoonacular
api_url = "https://api.spoonacular.com/recipes/findByIngredients"
api_key = "06491aabe3d2435b8b21a749de46b765"

# Funktion zum Abrufen von Rezepten basierend auf den eingegebenen Zutaten und den ausgewählten Filteroptionen
def get_recipes(ingredients, diet):
    params = {
        "apiKey": api_key,
        "ingredients": ingredients,
        "diet": diet,
        "number": 3
    }
    response = requests.get(api_url, params=params)
    return response.json()

def main():
    # Eingabe von Zutaten und Auswahl von Ernährungsoptionen
    ingredients = st.text_input("Enter comma-separated ingredients (e.g. chicken, rice, broccoli):")
    diet = st.selectbox("Dietary restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Ketogenic"])

    if st.button("Find Recipes"):
        if ingredients:
            response = get_recipes(ingredients, diet)
            if "error" not in response:
                # Anzeigen der Rezepttitel und Bilder
                for recipe in response:
                    st.header(recipe["title"])  # Titel des Rezepts
                    st.image(recipe["image"])  # Bild des Rezepts
            else:
                st.write("Error retrieving recipes: ", response["error"])
        else:
            st.write("Please enter at least one ingredient.")

if __name__ == "__main__":
    main()
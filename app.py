import streamlit as st
import requests


API_KEY = "06491aabe3d2435b8b21a749de46b765"

@st.cache
def get_recipes(query, cuisine, diet, intolerances):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={query}&cuisine={cuisine}&diet={diet}&intolerances={intolerances}"
    response = requests.get(url)
    return response.json()

def main():
    st.title("Spoonacular Rezeptsuche")

    query = st.text_input("Suchbegriff eingeben")
    cuisine = st.text_input("Küche eingeben")
    diet = st.text_input("Diät eingeben")
    intolerances = st.text_input("Unverträglichkeiten eingeben")

    if st.button("Rezepte suchen"):
        recipes = get_recipes(query, cuisine, diet, intolerances)
        if 'results' in recipes:
            for recipe in recipes["results"]:
                st.write(f"Name: {recipe['title']}")
                st.write("---")
        else:
            st.write("Keine Ergebnisse gefunden.")

if __name__ == "__main__":
    main()
import streamlit as st
import requests

# Setzen Sie hier Ihren Spoonacular API-Schlüssel ein
API_KEY = "Ihr_API_Schlüssel"

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
        for recipe in recipes["results"]:
            st.write(f"Name: {recipe['title']}")
            st.write("---")

if __name__ == "__main__":
    main()
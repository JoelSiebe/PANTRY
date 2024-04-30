import streamlit as st
import requests


API_KEY = "06491aabe3d2435b8b21a749de46b765"

@st.cache
def get_recipes(difficulty):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&difficulty={difficulty}"
    response = requests.get(url)
    return response.json()

def main():
    st.title("Spoonacular Rezeptsuche")

    difficulty = st.selectbox("Schwierigkeitsgrad auswählen", ["easy", "medium", "hard"])

    if st.button("Rezepte suchen"):
        recipes = get_recipes(difficulty)
        for recipe in recipes["results"]:
            st.write(f"Name: {recipe['title']}")
            st.write("---")

if __name__ == "__main__":
    main()
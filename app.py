import streamlit as st
import requests

# Setzen Sie hier Ihren Spoonacular API-Schlüssel ein
API_KEY = "06491aabe3d2435b8b21a749de46b765"

@st.cache
def get_recipes(difficulty, max_ready_time):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&difficulty={difficulty}&maxReadyTime={max_ready_time}"
    response = requests.get(url)
    return response.json()

def main():
    st.title("Spoonacular Rezeptsuche")

    difficulty = st.selectbox("Schwierigkeitsgrad auswählen", ["easy", "medium", "hard"])
    max_ready_time = st.slider("Maximale Zubereitungszeit in Minuten", 1, 120, 30)

    if st.button("Rezepte suchen"):
        recipes = get_recipes(difficulty, max_ready_time)
        for recipe in recipes["results"]:
            st.write(f"Name: {recipe['title']}")
            st.write(f"Zubereitungszeit: {recipe['readyInMinutes']} Minuten")
            st.write("---")

if __name__ == "__main__":
    main()
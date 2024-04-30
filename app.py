# Importieren der verschiedenen Bibliotheken
import streamlit as st # Streamlit
import requests # HTTP-Anfragen
import matplotlib.pyplot as plt # Datenvisualisierung

# Titel und Header
# Quelle für Header:https://stackoverflow.com/questions/70932538/how-to-center-the-title-and-an-image-in-streamlit
st.markdown("<h1 style='text-align: center; color: grey;'>Pantry Pal</h1>", unsafe_allow_html=True) # Mit unsafe_allow_html=True wird das Einfügen von HTML-Elementen ermöglicht
st.markdown("<h2 style='text-align: center; color: grey;'>Conquering Leftovers, Mastering Meals </h2>", unsafe_allow_html=True)
st.title("Tame your kitchen with Pantry Pal",)
st.divider() # Trennstrich, um die verschiedenen Abschnitte zu markieren

# Bilder in 2 Kolonnen anzeigen
# Quelle: https://docs.streamlit.io/library/api-reference/layout/st.columns)
st.header("So, what's the plan for today?")
st.header("Is it Italian? Or maybe a tasty burger?")
st.title("You decide.")
col1, col2= st.columns(2)

with col1:
   st.image("https://i.postimg.cc/44rnqrp3/pexels-lisa-fotios-1373915.jpgg") #Stock-Bild

with col2:
   st.image("https://i.postimg.cc/RZ0FH4BX/pexels-valeria-boltneva-1199957.jpg") #Stock-Bild

# Einführung in App mit entsprechenden Untertiteln
st.header("How does it work?") 
st.header("First, enter what's left in your fridge. Select any filters if needed.")
st.title("Then let us do the magic")

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
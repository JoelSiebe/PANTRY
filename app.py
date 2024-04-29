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

# Konfiguration für Spoonacular-API
api_url = "https://api.spoonacular.com/recipes/findByIngredients" # Spoonacular API-URL
api_key = "06491aabe3d2435b8b21a749de46b765" # API-Schlüssel

# Funktion zum Abrufen von Rezepten basierend auf Input (Zutaten) und den ausgewählten Filteroptionen
def get_recipes(ingredients, diet):
    # Parameter, die an API gesendet werden
    params = {
        "apiKey": api_key,
        "query": ingredients,
        "diet": diet,
        "number": 3,
        "addRecipeInformation": True
    }
    response = requests.get(url, params=params)
    return response.json()

def main():
    ingredients = st.text_input("Enter comma-separated ingredients (e.g. chicken, rice, broccoli): ")
    diet = st.selectbox("Dietary restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Ketogenic"])

    if st.button("Find Recipes"):
        if ingredients:
            response = get_recipes(ingredients, diet)
            results = response["results"]
            if len(results) == 0:
                st.write("No recipes found.")
            else:
                df = pd.DataFrame(results)
                df = df[["title", "readyInMinutes", "servings", "sourceUrl"]]
                st.write(df)
        else:
            st.write("Enter at least one ingredient")

if __name__ == "__main__":
    main()
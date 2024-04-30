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

api_key = "06491aabe3d2435b8b21a749de46b765"

@st.cache # Dektrator von Streamlit, um ein erneutes Senden der Anfrage an die API zu limitieren
def get_recipes(query, cuisine, diet, intolerances, difficulty, duration):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={query}&cuisine={cuisine}&diet={diet}&intolerances={intolerances}&difficulty={difficulty}&duration={duration}"
    response = requests.get(url)
    return response.json()

def main():
    query = st.text_input("Ingredients")
    cuisine = st.selectbox("Select cuisine", ["Any", "Italian", "Mexican", "Chinese"])
    difficulty = st.selectbox("Select difficulty level", ["Any", "Easy", "Medium", "Hard"])
    diet = st.selectbox("Select your diet", ["None", "Vegan", "Gluten Free", "Ketogenic"])
    duration = st.selectbox("Select duration", ["Any", "0-15 minutes", "15-30 minutes", "30-60 minutes", "60+ minutes"])
    intolerances = st.selectbox('Allergies', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])


    if st.button("Rezepte suchen"):
        recipes = get_recipes(query, cuisine, diet, intolerances, duration, difficulty)
        if 'results' in recipes:
            for recipe in recipes["results"]:
                st.write(f"Name: {recipe['title']}")
                st.write("---")
        else:
            st.write("Keine Ergebnisse gefunden.")

if __name__ == "__main__":
    main()
#     parameter = {"query": query}

#     if cuisine != "Any":
#         parameter['cuisine'] = cuisine.lower()
#     if difficulty != "Any":
#         parameter['difficulty'] = difficulty.lower()
#     if diet != "None":
#         parameter["diet"] = diet.lower()
#     if duration != "Any":
#         if duration == "0-15 minutes":
#             parameter['maxReadyTime'] = 15
#         elif duration == "15-30 minutes":
#             parameter['maxReadyTime'] = 30
#         elif duration == "30-60 minutes":
#             parameter['maxReadyTime'] = 60
#         elif duration == "60+ minutes":
#             parameter['maxReadyTime'] = 120
#     if intolerances != "None":
#         parameter["intolerances"] = intolerances.lower()

#     if st.button("Rezepte suchen"):
#         recipes = get_recipes(parameter)
#         if 'results' in recipes:
#             for recipe in recipes["results"]:
#                 st.write(f"Name: {recipe['title']}")
#                 st.write("---")
#         else:
#             st.write("Keine Ergebnisse gefunden.")

# if __name__ == "__main__":
#     main()





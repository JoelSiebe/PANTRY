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


# Konfiguration für Spoonacular-API
api_url = "https://api.spoonacular.com/recipes/findByIngredients" # Spoonacular API-URL
api_key = "4ea121e2c8424f89944d031e2dc68634" # API-Schlüssel

# Funktion zum Abrufen von Rezepten basierend auf Input (Zutaten) und den ausgewählten Filteroptionen
def get_recipes(ingredients, cuisine, difficulty, duration, allergies, diet):
    # Parameter, die an API gesendet werden
    parameter = {
        'ingredients': ingredients,
        'cuisine': cuisine,
        'difficutly': difficulty,
        'maxReadyTime': duration,
        'diet': diet,
        'number': 5, # Anz. angezeigter Rezepte
        'apiKey': api_key
    }
# Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)
    if cuisine != "Any":
        parameter['cuisine']=cuisine # Auswählen der versch. Küchen
    if difficulty != "Any":
        parameter['difficulty'] = difficulty.lower() # In Kleinbuchstaben umwandeln, um von der API gelesen zu werden
    if duration != "Any":
        # Festlegen der max. Zubereitungsdauer
        if duration == "0-15 minutes":
            parameter['maxReadyTime'] = 15
        elif duration == "15-30 minutes":
            parameter['maxReadyTime'] = 30
        elif duration == "30-60 minutes":
            parameter['maxReadyTime'] = 60
        else:
            parameter['maxReadyTime'] = 60 

#API-Abfrage senden
    response = requests.get(api_url, params=parameter)
    return response.json() # Rückgabe des Ergebnisses
   
# Zwei Kolonnen als Platzhalter für Eingabefelder (Filteroptionen) erstellen
with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_input('Ingredients') # Texteingabe der Zutaten
        # Auswahlfeld für eine mögliche Küche
        cuisine = st.selectbox('Cuisine', ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])
        diet = st.selectbox("Dietary restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Ketogenic"]) # Quelle: https://github.com/deepankarvarma/Recipe-Finder-Using-Python/blob/master/app.py
    with col2:
        # Auswahlfeld für mögliches Schwierigkeitsleven
        difficulty = st.selectbox('Difficulty Level', ['Any', 'Easy', 'Medium', 'Hard'])
        # Auswahlfeld für mögliche Zubereitungsdauer
        duration = st.selectbox('Duration', ['Any', '0-15 minutes', '15-30 minutes', '30-60 minutes', '60+ minutes'])
        # Auswahlfeld für mögliche Allergien
        allergies = st.selectbox('Allergies', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])

    submit_button = st.form_submit_button('Show recipes') # Schaltfläche zum Absenden des Formulars

# Rezepte anzeigen, wenn die Schaltfläche "Show recipes" geklickt wird
if submit_button:
    if ingredients: # Es müssen Zutaten eingegeben worden sein
        recipes = get_recipes(ingredients, cuisine, difficulty, duration, allergies, diet)
        if recipes:  # Wenn es Rezepte ausgibt
            for recipe in recipes:
                if 'title' in recipe:
                    st.subheader(recipe['title'])  # Rezepttitel anzeigen
                else:
                    st.write("No title found for this recipe")
                if 'image' in recipe:
                    st.image(recipe['image'])  # Bild des Rezepts anzeigen
                else:
                    st.write("No image found for this recipe")

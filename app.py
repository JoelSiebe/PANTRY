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
# api_url = "https://api.spoonacular.com/recipes/findByIngredients" # Spoonacular API-URL
api_key = "06491aabe3d2435b8b21a749de46b765" # API-Schlüssel
api_url = "https://api.spoonacular.com/recipes/complexSearch"

# Funktion zum Abrufen von Rezepten basierend auf Input (Zutaten) und den ausgewählten Filteroptionen
def get_recipes(ingredients, cuisine, difficulty, duration, intolerances, diet):
    # Parameter, die an API gesendet werden (aus API-Dokumentation)
    parameter = {
        'query': ingredients, # oder includeIngredients
        'cuisine': cuisine,
        'difficulty': difficulty,
        'maxReadyTime': duration,
        'diet': diet,
        'number': 2, # Anz. angezeigter Rezepte
        'apiKey': api_key,
        'addRecipeInformation': True
    }
# Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)
    if cuisine != "Any":
        parameter['cuisine']= cuisine.lower() # Auswählen der versch. Küchen
    if difficulty != "Any":
        parameter['difficulty'] = difficulty.lower() # Jeweils in Kleinbuchstaben umwandeln, um von der API gelesen zu werden
    if diet != "None":
        parameter["diet"] = diet.lower()
    if duration != "Any":
        # Festlegen der max. Zubereitungsdauer
        if duration == "0-15 minutes":
            parameter['maxReadyTime'] = 15
        elif duration == "15-30 minutes":
            parameter['maxReadyTime'] = 30
        elif duration == "30-60 minutes":
            parameter['maxReadyTime'] = 60
        elif duration == "60+ minutes":
            parameter['maxReadyTime'] = 120
      
    if intolerances != "None":
        parameter["intolerances"] = intolerances.lower()

#API-Abfrage senden
    response = requests.get(api_url, params=parameter)
    if response.status_code == 200 and response.text:
        try:
            recipes = response.json()  # In JSON umwandeln
        except requests.exceptions.JSONDecodeError:
            st.write("Error decoding JSON response. Please check the API.")
            recipes = None
    else:
        st.write("Failed to fetch recipes. Please check the API and try again.")
        recipes = None

    return recipes

   # return response.json() # Rückgabe des Ergebnisses

# Daten-Visualisierung in Form eines Piecharts (auf Basis der Nährwerten):
# Funktion, um Infos aus API abzurufen und in data zu speichern
def get_nutrition_info(recipe_id):
    api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    response = requests.get(api_nutrition_url, params={'apiKey': api_key})
    data = response.json() # Antwort in json umwandeln

# Funktion, um die Nährwerte als Float zurückzugeben (ansonsten funtioniert der Chart auf Streamlit nicht)
    def parse_nutrition_value(value):
        # Entfernen von Nicht-Zahlen (ungleich isdigit) und Umwandeln
        clean_value = ''.join([ch for ch in value if ch.isdigit() or ch == '.'])
        return float(clean_value)

 # Die relevanten Nährwerte (Kohlenhydrate, Protein, Fett) extrahieren
 # und mittels zuvor definierter Funktion Float umwandeln
    carbs = parse_nutrition_value(data['carbs'])
    protein = parse_nutrition_value(data['protein'])
    fat = parse_nutrition_value(data['fat'])

# Return eines Dictionaries mit den entsprechenden Nährwerten
    return {'carbs': carbs, 'protein': protein, 'fat': fat}
   
# Zwei Kolonnen als Platzhalter für Eingabefelder (Filteroptionen) erstellen
with st.form(key='recipe_form'):
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
        intolerances = st.selectbox('Allergies', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])

    submit_button = st.form_submit_button('Show recipes') # Schaltfläche zum Absenden des Formulars

# Rezepte anzeigen, wenn die Schaltfläche "Show recipes" geklickt wird
if submit_button:
    if ingredients: # Es müssen Zutaten eingegeben worden sein
        recipes = get_recipes(ingredients, cuisine, difficulty, duration, intolerances, diet)
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
                used_ingredients = ', '.join([ing['name'] for ing in recipe['usedIngredients']])
                missed_ingredients = ', '.join([ing['name'] for ing in recipe['missedIngredients']])
                st.write("Used Ingredients:", used_ingredients) # Gebrauchte und noch erforderliche Zutaten anzeigen
                st.write("Missing Ingredients:", missed_ingredients)
                
# Nährwertinformationen für das ausgewählte Rezept abrufen (um Piechart zu erstellen)
                nutrition_data = get_nutrition_info(recipe['id'])

# Anzeigen des Piecharts (Konfiguration von Grösse und Darstellung)
# Quelle für Workaround, um den Piechart kleiner zu machen: https://discuss.streamlit.io/t/cannot-change-matplotlib-figure-size/10295/10 
                col1, col2, col3, col4, col5=st.columns([1,1, 2, 1, 1])
                with col3:
                    labels = ['Carbohydrates', 'Protein', 'Fat'] # Beschriftungen
                    sizes = [nutrition_data['carbs'], nutrition_data['protein'], nutrition_data['fat']] # Anteilige Grösse der Sektoren gem. API
                    colors = ['#133337', '#cccccc', '#6897bb'] # Benutzerdefinierte Farben
                    fig, ax = plt.subplots(figsize=(4, 4)) # Erstellen des Diagramms
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90) # Darstellung
                    ax.axis('equal')  # "Rund" machen
                    st.pyplot(fig) # Anzeigen des Diagramms

#  Spoonacular-API für Zubereitungsschritte der jeweiligen Rezepe (https://spoonacular.com/food-api/docs#Get-Recipe-Information)
                api_info_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/information"
                instructions_response = requests.get(api_info_url, params={'apiKey': api_key})
                instructions_data = instructions_response.json() # Umwandeln in json

# Überprüfen, ob detailierte Zubereitungsschrite in API verfügbar sind
                if 'analyzedInstructions' in instructions_data:
                    steps = instructions_data['analyzedInstructions'] # Liste der Zubereitungsschritte
                    if steps: # Wenn Zubereitungsschritte vorhanden sind:
                        st.subheader("Instructions:") # Titel der Schritte
                        for section in steps:
                            for step in section['steps']:
                                st.write(f"Step {step['number']}: {step['step']}")  # Detaillierte Schritte anzeigen
                    else:
                        st.write("No detailed instructions found.")
                else:
                    st.write("No instructions available.")  

# Fusszeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal - Where Leftovers Meets Deliciousness. All rights reserved.")
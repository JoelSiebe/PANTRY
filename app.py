# Importieren der verschiedenen Bibliotheken
import streamlit as st # Streamlit
import requests # HTTP-Anfragen
import matplotlib.pyplot as plt # Datenvisualisierung

# Konfiguration für Spoonacular-API
api_key = "06491aabe3d2435b8b21a749de46b765"
api_url = "https://api.spoonacular.com/recipes/complexSearch"

# Funktion zum Abrufen von Rezepten basierend auf Input (Zutaten) und den ausgewählten Filteroptionen
def get_recipes(ingredients, cuisine, difficulty, duration, intolerances, diet):
  parameter = {
    'query': ingredients,
    'cuisine': cuisine.lower() if cuisine != "Any" else None,
    'difficulty': difficulty.lower() if difficulty != "Any" else None,
    'maxReadyTime': 
        {
          '0-15 minutes': 15,
          '15-30 minutes': 30,
          '30-60 minutes': 60,
          '60+ minutes': 120
        }[duration] if duration != "Any" else None,
    'diet': diet.lower() if diet != "None" else None,
    'number': 2,
    'apiKey': api_key,
    'addRecipeInformation': True
  }
  response = requests.post(api_url, json=parameter)
  if response.status_code == 200 and response.text:
    try:
      recipes = response.json()
    except requests.exceptions.JSONDecodeError:
      st.write("Error decoding JSON response. Please check the API.")
      recipes = None
    else:
      return recipes
  else:
    st.write("Failed to fetch recipes. Please check the API and try again.")
    return None

# Funktion, um Nährwertinformationen aus einem Rezept zu extrahieren
def get_nutrition_info(recipe_id):
  api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
  response = requests.get(api_nutrition_url, params={'apiKey': api_key})
  data = response.json()
  carbs = parse_nutrition_value(data['carbs'])
  protein = parse_nutrition_value(data['protein'])
  fat = parse_nutrition_value(data['fat'])
  return {'carbs': carbs, 'protein': protein, 'fat': fat}

# Funktion zum Umwandeln von Zahlenzeichenketten in Float-Werte
def parse_nutrition_value(value):
  clean_value = ''.join([ch for ch in value if ch.isdigit() or ch == '.'])
  return float(clean_value)

# Layout und Benutzeroberfläche mit Streamlit
st.title("Pantry Pal: Finde dein perfektes Rezept!")

# Eingabefelder für Zutaten und Filteroptionen
with st.form(key='recipe_form'):
  ingredients = st.text_input('Zutaten')
  cuisine = st.selectbox('Küche', ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])
  difficulty = st.selectbox('Schwierigkeitsgrad', ['Any', 'Easy', 'Medium', 'Hard'])
  duration = st.selectbox('Zubereitungszeit', ['Any', '0-15 minutes', '15-30 minutes', '30-60 minutes', '60+ minutes'])
  intolerances = st.selectbox('Allergien', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])
  diet = st.selectbox('Ernährungsweise', ["None", "Vegetarian", "Vegan", "Gluten-Free", "Ketogenic"])
  submit_button = st.form_submit_button('Rezepte finden')

# Anzeigen der Rezepte, wenn die Schaltfläche "Rezepte finden" geklickt wird
if submit_button:
  if ingredients:
    recipes = get_recipes(ingredients, cuisine, difficulty, duration, intolerances, diet)
    if recipes:
      for recipe in recipes:
          if 'title' in recipe:
              st.subheader(recipe['title'])
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
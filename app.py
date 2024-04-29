import streamlit as st
import requests
import matplotlib.pyplot as plt
import time

# Funktion zum Abrufen von Rezepten
def get_recipes(ingredients, cuisine, difficulty, duration, allergies, num_recipes):
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        'ingredients': ingredients,
        'number': num_recipes,
        'apiKey': "06491aabe3d2435b8b21a749de46b765"
    }
    response = requests.get(api_url, params=params)
    return response.json()

# Funktion zum Abrufen der Nährwertinformationen
def get_nutrition_info(recipe_id):
    api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    response = requests.get(api_nutrition_url, params={'apiKey': "06491aabe3d2435b8b21a749de46b765"})
    data = response.json()
    
    def parse_nutrition_value(value):
        clean_value = ''.join([ch for ch in value if ch.isdigit() or ch == '.'])
        return float(clean_value)
    
    carbs = parse_nutrition_value(data['carbs'])
    protein = parse_nutrition_value(data['protein'])
    fat = parse_nutrition_value(data['fat'])
    
    return {'carbs': carbs, 'protein': protein, 'fat': fat}

# Der obere statische Teil der App
st.markdown("<h1 style='text-align: center; color: grey;'>Pantry Pal</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Conquering Leftovers, Mastering Meals </h2>", unsafe_allow_html=True)

# Eingabeformular für Filteroptionen
with st.form(key='recipe_form'):
    ingredients = st.text_input("Enter Ingredients")
    cuisine = st.selectbox('Cuisine', ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'French', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])
    difficulty = st.selectbox('Difficulty Level', ['Any', 'Easy', 'Medium', 'Hard'])
    duration = st.selectbox('Duration', ['Any', '0-15 minutes', '15-30 minutes', '30-60 minutes', '60+ minutes'])
    allergies = st.selectbox('Allergies', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])
    
    submit_button = st.form_submit_button("Show Recipes")

# Anzahl der Rezepte, die abgefragt werden
num_recipes = 5

# Wenn das Formular abgeschickt wird, gehe zum unteren Teil
if submit_button:
    recipes = get_recipes(ingredients, cuisine, difficulty, duration, allergies, num_recipes)

    # Standardmäßig die erste Seite auswählen
    if 'recipe_page' not in st.session_state:
        st.session_state['recipe_page'] = 0
    
    current_page = st.session_state['recipe_page']
    num_recipes = len(recipes)

    # Zeige das aktuelle Rezept
    if current_page < num_recipes:
        recipe = recipes[current_page]
        st.subheader(recipe['title'])
        st.image(recipe['image'], width=300)  # Rezeptbild
        used_ingredients = ', '.join([ing['name'] for ing in recipe['usedIngredients']])
        missed_ingredients = ', '.join([ing['name'] for ing in recipe['missedIngredients']])
        st.write("Used Ingredients:", used_ingredients)
        st.write("Missing Ingredients:", missed_ingredients)

        # Tortendiagramm für die Nährwerte
        nutrition_data = get_nutrition_info(recipe['id'])
        labels = ['Carbohydrates', 'Protein', 'Fat']
        sizes = [nutrition_data['carbs'], nutrition_data['protein'], nutrition_data['fat']]
        fig, ax = plt.subplots(figsize=(3, 3))  # Kleinere Diagrammgröße
        ax.pie(sizes, labels=labels, colors=['#ff9999', '#66b3ff', '#99ff99'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Rundes Diagramm
        st.pyplot(fig)

        # Navigation für die Seiten
        col1, col2, col3 = st.columns(3)

        with col1:
            if current_page > 0:
                if st.button("Previous"):
                    st.session_state['recipe_page'] -= 1  # Gehe zur vorherigen Seite
                    
        with col3:
            if current_page < num_recipes - 1:
                if st.button("Next"):
                    st.session_state['recipe_page'] += 1  # Gehe zur nächsten Seite
    else:
        st.write("No recipes available.")
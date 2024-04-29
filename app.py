import streamlit as st
import requests
import matplotlib.pyplot as plt

# Titel und Header
# Quelle für Header: https://stackoverflow.com/questions/70932538/how-to-center-the-title-and-an-image-in-streamlit
st.markdown("<h1 style='text-align: center; color: grey;'>Pantry Pal</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Conquering Leftovers, Mastering Meals </h2>", unsafe_allow_html=True)
st.title("Tame your kitchen with Pantry Pal",)
st.divider()

# Bilder in 3 Kolonnen anzeigen, quelle: https://docs.streamlit.io/library/api-reference/layout/st.columns)

st.header("So, what's the plan for today?")
st.header("Is it Italian? Or maybe a tasty burger?")
st.title("You decide.")
col1, col2= st.columns(2)

with col1:
   st.image("https://i.postimg.cc/44rnqrp3/pexels-lisa-fotios-1373915.jpgg")

with col2:
   st.image("https://i.postimg.cc/RZ0FH4BX/pexels-valeria-boltneva-1199957.jpg")

# weitere Untertitel

st.header("How does it work?") 
st.header("First, enter what's left in your fridge. Selcect any filters if needed.")
st.title("Then let us do the magic")

#Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)

# Spoonacular API-URL
api_url = "https://api.spoonacular.com/recipes/findByIngredients"
#API-Schlüssel (noch schauen, wie man das in einer anderen Datei macht)
api_key = "06491aabe3d2435b8b21a749de46b765"

# Funktion zum Abrufen von Rezepten
def get_recipes(ingredients, cuisine, difficulty, duration, allergies):
    parameter = {
        'ingredients': ingredients,
        'number': 1, #Anz. angezeigter Rezepte -> zuerst 10, um dann nochmals auf Allergien / Länder zu filtern
        'apiKey': api_key
    }

    # Filteroptionen
    if cuisine != "Any":
        parameter['cuisine']=cuisine
    if difficulty != "Any":
        parameter['difficulty'] = difficulty.lower()
    if duration != "Any":
        if duration == "0-15 minutes":
            parameter['maxReadyTime'] = 15
        elif duration == "15-30 minutes":
            parameter['maxReadyTime'] = 30
        elif duration == "30-60 minutes":
            parameter['maxReadyTime'] = 60
        else:
            parameter['maxReadyTime'] = 60 

    # if allergies:
    #     parameter['intolerances'] = allergies.lower()

    #API-Abfrage senden
    response = requests.get(api_url, params=parameter)
    return response.json()

    # response = requests.get(api_url, params=parameter)
    # all_recipes = response.json()
    # filtered_recipes = []

    # if allergies and allergies != 'None':
    #     allergy_list = [allergy.strip().lower() for allergy in allergies.split(",")]

    #     for recipe in all_recipes:
    #         all_ingredients = [ing['name'].lower() for ing in recipe['usedIngredients'] + recipe['missedIngredients']]

    #         has_allergy = False
    #         for allergy in allergy_list:
    #             if allergy in all_ingredients:
    #                 has_allergy = True
    #                 break

    #         if not has_allergy:
    #             filtered_recipes.append(recipe)

    # else:
    #     filtered_recipes = all_recipes  

    # return filtered_recipes




# Daten-Visualisierung in Form eines Kuchendiagrams (auf Basis der Nährwerten) -> Funktion um Infos abzurufen
def get_nutrition_info(recipe_id):
    api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    response = requests.get(api_nutrition_url, params={'apiKey': api_key})
    data = response.json()

    def parse_nutrition_value(value):
        clean_value = ''.join([ch for ch in value if ch.isdigit() or ch == '.'])
        return float(clean_value)

    # Die relevanten Nährwerte (Kohlenhydrate, Protein, Fett) extrahieren und umwandeln
    carbs = parse_nutrition_value(data['carbs'])
    protein = parse_nutrition_value(data['protein'])
    fat = parse_nutrition_value(data['fat'])

    return {'carbs': carbs, 'protein': protein, 'fat': fat}
   
# Zwei Texteingabefelder (Filteroptionen) nebeneinander anzeigen
with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_input('Ingredients')
        cuisine= st.selectbox('Cuisine', ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])
    with col2:
        difficulty = st.selectbox('Difficulty Level', ['Any', 'Easy', 'Medium', 'Hard'])
        duration = st.selectbox('Duration', ['Any', '0-15 minutes', '15-30 minutes', '30-60 minutes', '60+ minutes'])
        allergies = st.selectbox('Allergies', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])

    submit_button = st.form_submit_button('Show recipes')

# Rezepte anzeigen, wenn die Schaltfläche "Show recipes" geklickt wird
if submit_button:
    if ingredients:
        recipes = get_recipes(ingredients, cuisine, difficulty, duration, allergies)
        if recipes:  # Wenn es Rezepte gibt
            for recipe in recipes:
                st.subheader(recipe['title'])  # Rezepttitel anzeigen
                st.image(recipe['image'])  # Bild des Rezepts anzeigen
                used_ingredients = ', '.join([ing['name'] for ing in recipe['usedIngredients']])
                missed_ingredients = ', '.join([ing['name'] for ing in recipe['missedIngredients']])
                st.write("Used Ingredients:", used_ingredients)
                st.write("Missing Ingredients:", missed_ingredients)
                
                # Nährwertinformationen für das ausgewählte Rezept abrufen
                nutrition_data = get_nutrition_info(recipe['id'])

               
                labels = ['Carbohydrates', 'Protein', 'Fat']
                sizes = [nutrition_data['carbs'], nutrition_data['protein'], nutrition_data['fat']]

                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  
                st.pyplot(fig)

                
                # labels = 'Carbs', 'Fat', 'Protein' 
                # sizes = [15, 12, 20]
                          
                        
                # fig, ax = plt.subplots()
                # ax.pie(sizes, labels=labels)

                # st.pyplot(fig)  

                #  Spoonacular-API für Rezeptinformationen (https://spoonacular.com/food-api/docs#Get-Recipe-Information) / Key ist derselbe
                api_info_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/information"
                instructions_response = requests.get(api_info_url, params={'apiKey': api_key})
                instructions_data = instructions_response.json()

                if 'analyzedInstructions' in instructions_data:
                    steps = instructions_data['analyzedInstructions']
                    if steps: 
                        st.subheader("Instructions:")
                        for section in steps:
                            for step in section['steps']:
                                st.write(f"Step {step['number']}: {step['step']}")  # Detaillierte Schritte anzeigen
                    else:
                        st.write("No detailed instructions found.")
                else:
                    st.write("No instructions available.")  # Wenn keine Anweisungen gefunden werden
            else:
                st.write("No recipes found for the given ingredients.")  # Falls keine Rezepte gefunden werden

            # # Spoonacular-API für Nutritions-Pie-chart (https://spoonacular.com/food-api/docs#Get-Recipe-Information) / Key ist derselbe
            # api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/nutritionWidget.json"
            # nutrition_response = requests.get(api_nutrition_url, params={'apiKey': api_key})
            # nutrition_data = nutrition_response.json()

            # if 'calories' in nutrition_data:
            #     nutrition = nutrition_data['calories']
            #     st.subheader("Nutrition Information:")
            #     st.write(f"Calories: {nutrition['value']} {nutrition['unit']}")

            #     # Pie-Chart für Nutrition
            #     labels = list(nutrition_data['nutrition'].keys())
            #     sizes = list(nutrition_data['nutrition'].values())

            #     fig, ax = plt.subplots()
            #     ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            #     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            #     st.write("Nutrition Chart:")
            #     st.pyplot(fig)


# Fusszeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal - Where Leftovers Meets Deliciousness. All rights reserved.")
import streamlit as st
import requests
import matplotlib as plt


# Übersicht über die verwendeten Namen:

##Mit nachfolgendem Abschnitt kann ein Hintergrundbild eingefügt werden; 
##CSS-Stil (https://discuss.streamlit.io/t/upload-background-image/59732 // https://www.w3schools.com/cssref/pr_background-image.php)
# css_background = """   
# <style>
# [data-testid="stAppViewContainer"] > .main {
#     # background-image: url("https://i.postimg.cc/cJtrkLQw/pexels-mike-murray-5701888.jpg");
#     background-image: url("https://i.postimg.cc/prztbnxs/pexels-brett-sayles-6871608.jpg");
#     background-size: cover;                 #grösse des hintergrundbilds, cover = ganzer container
#     background-position: center center;
#     background-repeat: no-repeat;
#     background-attachment: local;        #beim scrollen fix oder bewegend - local = bewegend
# }

# [data-testid="stHeader"] {
#     background: rgba(181, 179, 179);
# }
# </style>
# """

# st.markdown(css_background, unsafe_allow_html=True) #css_background wird angewendet, unsafe für Anzeige von HTML-Inhalten

# *Titel und Header*
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
#    st.header("Is it Italian?")
   st.image("https://i.postimg.cc/44rnqrp3/pexels-lisa-fotios-1373915.jpgg")

with col2:
#    st.header("Or maybe Korean?")
   st.image("https://i.postimg.cc/RZ0FH4BX/pexels-valeria-boltneva-1199957.jpg")

# weitere Untertitel -> noch schauen, ob mit CSS schöner gemacht werden kann.

st.header("How does it work?") 
st.header("First, enter what's left in your fridge. Selcect any filters if needed.")
st.title("Then let us do the magic")

#Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)

# Spoonacular API-URL
api_url = "https://api.spoonacular.com/recipes/findByIngredients"
#API-Schlüssel (noch schauen, wie man das in einer anderen Datei macht)
api_key = "06491aabe3d2435b8b21a749de46b765"

# Funktion zum Abrufen von Rezepten
def get_recipes(ingredients, cuisine, difficulty, duration, number_ingredients):
    parameter = {
        'ingredients': ingredients,
        'number': 5, #Anz. angezeigter Rezepte
        'apiKey': api_key
    }

    # Hinzufügen der Filteroptionen
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

    if number_ingredients:
        parameter['number'] = number_ingredients

    #API-Abfrage senden
    response = requests.get(api_url, params=parameter)
    data = response.json()
    return data

# Zwei Texteingabefelder nebeneinander anzeigen
with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        ingredients = st.text_input(label='Ingredients')
        cuisine= st.selectbox('Cuisine', ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])
    with col2:
        difficulty = st.selectbox('Difficulty Level', ['Any', 'Easy', 'Medium', 'Hard'])
        duration = st.selectbox('Duration', ['Any', '0-15 minutes', '15-30 minutes', '30-60 minutes', '60+ minutes'])
        number_ingredients = st.number_input('Number of ingredients', min_value=1, max_value=20, value=5)

    submit_button = st.form_submit_button(label='Show recipes')

# Rezepte anzeigen, wenn die Schaltfläche "Show recipes" geklickt wird
if submit_button:
    if ingredients:
        recipes = get_recipes(ingredients, cuisine, difficulty, duration, number_ingredients)
        st.write("Recipes:")
        for recipe in recipes:
            st.write(recipe['title'])

        # Rezeptvorschläge
        st.header("Look what we've found for you")
        for recipe in recipes:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            st.write(f"Used ingredients: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Missing ingredients: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Number of missing ingredients: {recipe['missedIngredientCount']}")
            st.write(f"Number of used ingredients: {recipe['usedIngredientCount']}")

            # Spoonacular-API für Rezeptinformationen (https://spoonacular.com/food-api/docs#Get-Recipe-Information) / Key ist derselbe
            api_informations_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/information"
            instructions_response = requests.get(api_informations_url, params={'apiKey': api_key})
            instructions_data = instructions_response.json()

            if 'instructions' in instructions_data:
                instructions = instructions_data['instructions']
                if instructions:
                    st.subheader("Instructions:")
                    # Prüft, ob Rezeptschritte vorliegen
                    if isinstance(instructions, list):
                        for i, step in enumerate(instructions, start=1):
                            st.write(f"{i}. {step}")
                    else:
                        st.write(instructions)  # Wenn die Anweisungen nicht als Liste vorliegen, einfach anzeigen
                else:
                    st.write("No instructions available.")
            else:
                st.write("Recipe steps not available.")

            # Spoonacular-API für Nutritions-Pie-chart (https://spoonacular.com/food-api/docs#Get-Recipe-Information) / Key ist derselbe
            api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/nutritionWidget.json"
            nutrition_response = requests.get(api_nutrition_url, params={'apiKey': api_key})
            nutrition_data = nutrition_response.json()

            if 'calories' in nutrition_data:
                nutrition = nutrition_data['calories']
                st.subheader("Nutrition Information:")
                st.write(f"Calories: {nutrition['value']} {nutrition['unit']}")

                # Pie-Chart für Nutrition
                labels = list(nutrition_data['nutrition'].keys())
                sizes = list(nutrition_data['nutrition'].values())

                fig, ax = plt.subplots()
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                st.write("Nutrition Chart:")
                st.pyplot(fig)


# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal - Where Leftovers Meets Deliciousness. All rights reserved.")
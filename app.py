import streamlit as st
import requests
import numpy as np
import pandas as pd

# #CSS-Stil (https://discuss.streamlit.io/t/upload-background-image/59732 // https://www.w3schools.com/cssref/pr_background-image.php)
# css_background = """   
# <style>
# [data-testid="stAppViewContainer"] > .main {
#     background-image: url("https://i.postimg.cc/cJtrkLQw/pexels-mike-murray-5701888.jpg");
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

# Titel und Header
st.title("Pantry Pal;",)
st.title("Conquering Leftovers, Mastering Meals",)
st.divider()
st.header("**Tame your kitchen with Pantry Pal**",)
st.divider()
# Zwei Texteingabefelder nebeneinander anzeigen
with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input(label='Vorname')
    with col2:
        last_name = st.text_input(label='Nachname')

    submit_button = st.form_submit_button(label='Senden')


# Zeige den vollständigen Satz nach dem Absenden des Formulars
if submit_button:
    st.write(f'Hallo, {first_name} {last_name}!')

# Bilder in 3 Kolonnen anzeigen, quelle: https://docs.streamlit.io/library/api-reference/layout/st.columns)
col1, col2, col3 = st.columns(3)

st.write("Where Leftovers Meets Deliciousness!")

with col1:
   st.header("A cat")
   st.image("https://www.pexels.com/photo/a-flatlay-of-tteokbokki-in-a-bowl-12963392/")

with col2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg")

# Versch. Zutaten des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)")

#Filteroptionen (https://docs.streamlit.io/library/api-reference/widgets)

difficulty = st.selectbox("Select Difficulty", ["Any", "Easy", "Medium", "Hard"])
duration = st.selectbox("Select Cooking Time", ["Any", "0-15 minutes", "15-30 minutes", "30-60 minutes", "60+ minutes"])
number_ingredients = st.slider("Number of Ingredients", min_value=1, max_value=20, value=5)

# Clickboxen, die temp. mit session_gate gespeichert werden (quelle (etw. abgeändert):https://stackoverflow.com/questions/71242486/how-to-make-n-checkboxes-in-streamlit)

# # 1. Create a variable to store todos.
# if not 'cuisine_list' in st.session_state:
#     st.session_state.cuisine_list = []

# # 2. Prompt the user in the form
# with st.form(key='cuisine_form'):
#     cuisine = st.text_input(label='Select your favorite cuisines')
#     is_submit = st.form_submit_button('submit')

# # 3. Store todo in todolist when submit button is hit.
# if is_submit:
#     st.session_state.cuisine_list.append(cuisine)
    
# # 4. Display the contents of todolist
# with st.expander(label='List of selected cuisines', expanded=True):
#     for i, cuisine_text in enumerate(st.session_state.cuisine_list):
#         st.checkbox(label=f'{cuisine_text}', key=i)

cuisines_api = ['African', 'Asian' 'American', 'British', 'Caribbean', 'Chinese', 'Eastern European', 'European', 'French', 'German', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese',]

if not 'cuisine_list' in st.session_state:
    st.session_state.cuisine_list = [False]*len(cuisines_api)

with st.expander(label='Select your favorite cuisines', expanded=True):
    for i, cuisine_text in enumerate(cuisines_api):
        st.session_state.cuisine_list[i] = st.checkbox(label=f'{cuisine_text}', key=i, value=st.session_state.cuisine_list[i])


if st.button('Show recipes'):
    if zutaten:

        # Spoonacular API-URL
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"

        #API-Schlüssel (noch schauen, wie man das in einer anderen Datei macht)
        api_key = "06491aabe3d2435b8b21a749de46b765"

        #Datenbankabfrage (länder hinzufügen -> ?)
        parameter = {
            'ingredients': zutaten,
            'number': 5, #Anz. angezeigter Rezepte
            'apiKey': api_key
        }

        # Hinzufügen der Filteroptionen
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

        #Rezeptvorschläge 
        st.header("Look what we've found for you")
        for recipe in data:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            st.write(f"Used ingredients: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Missing ingredients: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Number of missing ingredients: {recipe['missedIngredientCount']}")
            st.write(f"Number of used ingredients: {recipe['usedIngredientCount']}")
  

            #Spoonacular-API für Rezeptinformationen (https://spoonacular.com/food-api/docs#Get-Recipe-Information) / Key ist derselbe
            api_informations_url = "https://api.spoonacular.com/recipes/{id}/information"
            
            if 'id' in recipe:  #API prüfen, ob Zubereitungschritte verfügubar 
                recipe_id = recipe['id']
                instructions_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
                instructions_response = requests.get(instructions_url, params={'apiKey': api_key})
                instructions_data = instructions_response.json()

                if 'instructions' in instructions_data:
                    st.subheader("Instructions:")
                    instructions = instructions_data['instructions'].split('\n')  
                    for step in instructions:
                        st.write(f"- {step}")  
                else:
                    st.write("Recipe steps not available.")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")
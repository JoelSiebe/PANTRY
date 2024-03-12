import streamlit as st
import requests
import numpy as np
import pandas as pd

# CSS-Stil (https://discuss.streamlit.io/t/upload-background-image/59732 // https://www.w3schools.com/cssref/pr_background-image.php)
css_background = """   
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.postimg.cc/cJtrkLQw/pexels-mike-murray-5701888.jpg");
    background-size: cover;                 #grösse des hintergrundbilds, cover = ganzer container
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;        #beim scrollen fix oder bewegend - local = bewegend
}

[data-testid="stHeader"] {
    background: rgba(181, 179, 179);
}
</style>
"""

st.markdown(css_background, unsafe_allow_html=True) #css_background wird angewendet, unsafe für Anzeige von HTML-Inhalten

# Titel und Header
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals",)
st.header("**Tame your kitchen with Pantry Pal**",)

# Versch. Zutaten des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)")

#popover, um versch. Küchen auszuwählen anhand Liste von Tupeln (https://docs.streamlit.io/library/api-reference/layout/st.popover // GPT_1)
popover = st.popover("Preffered Cuisine")
cuisines = [
    ("African", popover.checkbox("African", False)),
    ("Asian", popover.checkbox("Asian", False)),
    ("American", popover.checkbox("American", False)),
    ("British", popover.checkbox("British", False)),
    ("Caribbean", popover.checkbox("Caribbean", False)),
    ("Chinese", popover.checkbox("Chinese", False)),
    ("Eastern European", popover.checkbox("Eastern European", False)),
    ("European", popover.checkbox("European", False)),
    ("French", popover.checkbox("French", False)),
    ("German", popover.checkbox("German", False)),
    ("Greek", popover.checkbox("Greek", False)),
    ("Indian", popover.checkbox("Indian", False)),
    ("Italian", popover.checkbox("Italian", False)),
    ("Japanese", popover.checkbox("Japanese", False)),
    ("Mexican", popover.checkbox("Mexican", False)),
    ("Thai", popover.checkbox("Thai", False)),
    ("Vietnamese", popover.checkbox("Vietnamese", False))
]

selected_cuisines = []

for cuisine_name, checkbox_value in cuisines:
    if checkbox_value:  # Überprüfen, ob die Checkbox aktiviert ist
        selected_cuisines.append(cuisine_name)

# Printen der ausgewählten Küchen
if selected_cuisines:
    st.write("Selected cuisines:", selected_cuisines)
else:
    st.write("No cuisine selected.")
    

if african:
    st.write(":red[This is a red item.]")
if asian:
    st.write(":blue[This is a blue item.]")

if st.button('Show recipes'):
    if zutaten:

        # Spoonacular API-URL
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"

        #API-Schlüssel (noch schauen, wie man das in einer anderen Datei macht)
        api_key = "06491aabe3d2435b8b21a749de46b765"

        #Datenbankabfrage
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
                parameter['maxReadyTime'] = 60  # 60+ minutes

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
            st.write(f"Verwendete Zutaten: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Fehlende Zutaten: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Anzahl der fehlenden Zutaten: {recipe['missedIngredientCount']}")
            st.write(f"Anzahl der verwendeten Zutaten: {recipe['usedIngredientCount']}")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")

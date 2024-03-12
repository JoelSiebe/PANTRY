import streamlit as st
import requests
import numpy as np
import pandas as pd

# CSS-Stil (inspiriert von https://www.w3schools.com/cssref/pr_background-image.php)
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
    background: rgba(0,0,0,0);
}

div[data-baseweb="input"] input {
    color: black !important; /* Ändere die Schriftfarbe auf Schwarz */
    font-size: 20px !important; /* Ändere die Schriftgröße auf 20px */
</style>
"""

st.markdown(css_background, unsafe_allow_html=True) #css_background wird angewendet, unsafe für Anzeige von HTML-Inhalten

# Titel und Untertitel
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

# Versch. Zutaten des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)", key="ingredients", max_chars=1000)

# Filteroptionen
difficulty = st.selectbox("Select Difficulty", ["Any", "Easy", "Medium", "Hard"])
duration = st.selectbox("Select Cooking Time", ["Any", "0-15 minutes", "15-30 minutes", "30-60 minutes", "60+ minutes"])
number_ingredients = st.slider("Number of Ingredients", min_value=1, max_value=20, value=5)




# Button, um Rezepte anzuzeigen und an Einkaufsliste zu senden
if st.button('Show recipes'):
    if zutaten:
        # Spoonacular API-URL
        api_url = "https://api.spoonacular.com/recipes/findByIngredients"

        # API-Schlüssel
        api_key = "06491aabe3d2435b8b21a749de46b765"

        # Datenbankabfrage
        params = {
            'ingredients': zutaten,
            'number': 5,  # Anz. angezeiter Rezepte
            'apiKey': api_key
        }

        # Hinzufügen der Filteroptionen
        if difficulty != "Any":
            params['difficulty'] = difficulty.lower()
        if duration != "Any":
            if duration == "0-15 minutes":
                params['maxReadyTime'] = 15
            elif duration == "15-30 minutes":
                params['maxReadyTime'] = 30
            elif duration == "30-60 minutes":
                params['maxReadyTime'] = 60
            else:
                params['maxReadyTime'] = 60  # 60+ minutes

        if number_ingredients:
            params['number'] = number_ingredients

        # API-Abfrage senden
        response = requests.get(api_url, params=params)
        data = response.json()

        # Einkaufsliste vorbereiten
        shopping_list = [ingredient['name'] for recipe in data for ingredient in recipe['missedIngredients']]
        shopping_list_text = '\n'.join(shopping_list)

        # Einkaufsliste per E-Mail senden
        if st.button("Send shopping list via email"):
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            # E-Mail-Konfiguration
            sender_email = "your_email@example.com"
            receiver_email = "recipient_email@example.com"
            password = "your_password"

            # Nachricht erstellen
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Shopping List from Pantry Pal"

            # Nachrichtentext hinzufügen
            msg.attach(MIMEText(shopping_list_text, 'plain'))

            # Verbindung zum Server herstellen und E-Mail senden
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.send_message(msg)

            st.success("Shopping list sent successfully!")

        # Anzeigen der Einkaufsliste mit Checkboxen
        for ingredient in shopping_list:
            if st.checkbox(ingredient):
                shopping_list.remove(ingredient)

# Rezepte anzeigen
if zutaten and st.button('Show recipes'):
    if zutaten:
        st.markdown('<a name="recipes"></a>', unsafe_allow_html=True)
        st.header("Look what we've found for you")
        for recipe in data:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            st.write(f"Used ingredients: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Missed ingredients: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Number of missed ingredients: {recipe['missedIngredientCount']}")
            st.write(f"Number of used ingredients: {recipe['usedIngredientCount']}")
            
            # Nutrition information
            nutrition_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/nutritionWidget.json?apiKey={api_key}"
            nutrition_info = requests.get(nutrition_url).json()
            st.subheader("Nutrition Information")
            st.write(nutrition_info)

# Fußzeile
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")

import streamlit as st
import requests

# CSS-Stile
css_styles = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://i.postimg.cc/cJtrkLQw/pexels-mike-murray-5701888.jpg");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
}
</style>
"""

st.markdown(css_styles, unsafe_allow_html=True)

# Titel und Header
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

# Zutatenliste des Benutzers als Eingabefeld
zutaten = st.text_input("Enter what's left in your fridge (separated by comma)", key="ingredients", max_chars=1000)

# Filteroptionen
schwierigkeitsgrad = st.selectbox("Select Difficulty", ["Any", "Easy", "Medium", "Hard"])
zeitdauer = st.selectbox("Select Cooking Time", ["Any", "0-15 minutes", "15-30 minutes", "30-60 minutes", "60+ minutes"])
anzahl_zutaten = st.slider("Number of Ingredients", min_value=1, max_value=20, value=5)

# Button, um Rezepte anzuzeigen und Einkaufsliste zu senden
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

        # Hinzufügen der Filterparameter
        if schwierigkeitsgrad != "Any":
            params['difficulty'] = schwierigkeitsgrad.lower()
        if zeitdauer != "Any":
            if zeitdauer == "0-15 minutes":
                params['maxReadyTime'] = 15
            elif zeitdauer == "15-30 minutes":
                params['maxReadyTime'] = 30
            elif zeitdauer == "30-60 minutes":
                params['maxReadyTime'] = 60
            else:
                params['maxReadyTime'] = 60  # 60+ minutes

        if anzahl_zutaten:
            params['number'] = anzahl_zutaten

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

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")

# Rezepte anzeigen
if zutaten and st.button('Show recipes'):
    if zutaten:
        st.markdown('<a name="recipes"></a>', unsafe_allow_html=True)
        st.header("Look what we've found for you")
        for recipe in data:
            st.subheader(recipe['title'])
            st.image(recipe['image'])
            st.write(f"Verwendete Zutaten: {', '.join([ingredient['name'] for ingredient in recipe['usedIngredients']])}")
            st.write(f"Fehlende Zutaten: {', '.join([ingredient['name'] for ingredient in recipe['missedIngredients']])}")
            st.write(f"Anzahl der fehlenden Zutaten: {recipe['missedIngredientCount']}")
            st.write(f"Anzahl der verwendeten Zutaten: {recipe['usedIngredientCount']}")
            
            # Nutrition information
            nutrition_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/nutritionWidget.json?apiKey={api_key}"
            nutrition_info = requests.get(nutrition_url).json()
            st.subheader("Nutrition Information")
            st.write(nutrition_info)

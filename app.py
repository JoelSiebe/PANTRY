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
st.title("🍽️ How does it work?")
st.write("")
st.header("🥦 Start with Leftovers.")
st.subheader("Just type in what's still hanging out in your fridge.")
st.write("")
st.header("🌍 Choose Your Adventure:")
st.subheader("Got a favorite cuisine? Any dietary restrictions or allergies? Let us know!")
st.write("")
st.header("🎩 Then let us do the magic 🐇")
st.subheader("Leave the rest to us. We're about to turn your leftovers into a feast!")
st.write("")
st.write("")

# Konfiguration für Spoonacular-API (key)
api_key = "4f7e1499f8784e6aa5cd54ae451fce53"

@st.cache # Dektrator von Streamlit, um ein erneutes Senden der Anfrage an die API zu limitieren
def get_recipes(query, cuisine, diet, intolerances,number_of_recipes=3):
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&query={query}&cuisine={cuisine}&diet={diet}&intolerances={intolerances}&number={number_of_recipes}"
    response = requests.get(url)
    return response.json()

# Daten-Visualisierung in Form eines Piecharts (auf Basis der Nährwerten):
# Funktion, um Infos aus API abzurufen und in data zu speichern
def get_nutrition_info(recipe_id):
    api_nutrition_url = f"https://api.spoonacular.com/recipes/{recipe_id}/nutritionWidget.json"
    response = requests.get(api_nutrition_url, params={'apiKey': api_key})
    if response.status_code != 200:
        print(f"Looks like we hit a speed bump 🚧. Error code: {response.status_code}")
        return None
    data = response.json() # Antwort in json umwandeln

# Funktion, um die Nährwerte als Float zurückzugeben (ansonsten funtioniert der Chart auf Streamlit nicht)
    def parse_nutrition_value(value):
        if isinstance(value, (int, float)):
            return float(value)
        # Entfernen von Nicht-Zahlen (ungleich isdigit) und Umwandeln
        clean_value = ''.join([ch for ch in value if ch.isdigit() or ch == '.'])
        return float(clean_value) if clean_value else 0

 # Die relevanten Nährwerte (Kohlenhydrate, Protein, Fett) extrahieren
 # und mittels zuvor definierter Funktion Float umwandeln
    carbs = parse_nutrition_value(data['carbs']) 
    protein = parse_nutrition_value(data['protein']) 
    fat = parse_nutrition_value(data['fat']) 

# Return eines Dictionaries mit den entsprechenden Nährwerten
    return {'carbs': carbs, 'protein': protein, 'fat': fat}

def main():
    # Zwei Kolonnen als Platzhalter für Eingabefelder (Filteroptionen) erstellen
    with st.form(key='recipe_form'):
        col1, col2 = st.columns(2)
        with col1:
            query = st.text_input("Ingredients: Your choice") # Texteingabe der Zutaten
            # Auswahlfeld für mögliche Küchen
            cuisine = st.selectbox('Cuisine: All around the world',  ['Any', 'African', 'Asian', 'American', 'Chinese', 'Eastern European', 'Greek', 'Indian', 'Italian', 'Japanese', 'Mexican', 'Thai', 'Vietnamese'])           
        with col2:
            # Auswahlfeld für Diät
            diet = st.selectbox("Dietary Restrictions: We've got you covered", ["None", "Vegan", "Vegetarian", "Gluten Free", "Ketogenic"])
            # Auswahlfeld für mögliche Allergien
            intolerances = st.selectbox('Allergies: Say no more', ['None', 'Dairy', 'Egg', 'Gluten', 'Peanut', 'Seafood', 'Sesame', 'Shellfish', 'Soy', 'Tree Nut', 'Wheat'])

        submit_button = st.form_submit_button("Show recipes") 

        if submit_button: # Schaltfläche zum Absenden der Eingaben, resp. Anzeigen der entspr. Rezepten
            recipes = get_recipes(query, cuisine, diet, intolerances, number_of_recipes=3)
            if 'results' in recipes:
                for recipe in recipes["results"]:
                    st.header(f"🍽️ {recipe['title']}")
                    
                    recipe_info_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/information"
                    recipe_info_response = requests.get(recipe_info_url, params={'apiKey': api_key})
                    recipe_info = recipe_info_response.json()

                    if 'readyInMinutes' in recipe_info:
                        st.write("⏰ Cooking Time:", f"{recipe_info['readyInMinutes']} minutes")
                    else:
                        st.write("⏰ Cooking Time: It's a mystery! 🕵️")

                    if 'extendedIngredients' in recipe_info:
                        ingredients = ', '.join([ing['name'] for ing in recipe_info['extendedIngredients']])
                        st.write("🥦 Ingredients:", ingredients)
                    else:
                        st.write("🥦 Ingredients: It's a surprise! 🎁")

                    if 'image' in recipe_info:
                        st.image(recipe['image'])
                    else:
                        st.write("🖼️ Picture: It's left to your imagination! 🌈")
                    st.write("---")

                   
# Aufrufen der Nährwerte-Funktion
                    nutrition_info = get_nutrition_info(recipe['id'])
                    if nutrition_info is not None:
                        with st.expander("🏖️ Dreaming of that summer body? Let's check the nutrition!"):
                            st.subheader("🍎 Nutrition Breakdown")

    # Anzeigen des Piecharts (Konfiguration von Grösse und Darstellung)
                            labels = ['Carbohydrates', 'Protein', 'Fat'] # Beschriftungen
                            sizes = [nutrition_info['carbs'], nutrition_info['protein'], nutrition_info['fat']] # Anteilige Grösse der Sektoren gem. API
                            colors = ['#133337', '#cccccc', '#6897bb'] # Benutzerdefinierte Farben
                            fig, ax = plt.subplots(figsize=(4, 4)) # Erstellen dess Diagramms
                            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90) # Darstellung
                            ax.axis('equal')  # "Rund" machen
                            st.pyplot(fig) # Anzeigen des Diagramms
                    else:
                        st.write("Looks like we hit a speed bump with the nutrition score 🚧")
                      

#  Spoonacular-API für Zubereitungsschritte der jeweiligen Rezepe (https://spoonacular.com/food-api/docs#Get-Recipe-Information)
                    api_info_url = f"https://api.spoonacular.com/recipes/{recipe['id']}/information"
                    instructions_response = requests.get(api_info_url, params={'apiKey': api_key})
                    instructions_data = instructions_response.json() # Umwandeln in json

# Überprüfen, ob detailierte Zubereitungsschrite in API verfügbar sind
                    with st.expander("🔍 Ready to cook? Click here for step-by-step instructions"):
                        if 'analyzedInstructions' in instructions_data:
                            steps = instructions_data['analyzedInstructions'] # Liste der Zubereitungsschritte
                            if steps: # Wenn Zubereitungsschritte vorhanden sind:
                                st.subheader("📝 Let's Get Cooking!") # Titel der Schritte
                                for section in steps:
                                    for step in section['steps']:
                                        st.write(f"Step {step['number']}: {step['step']}")  # Detaillierte Schritte anzeigen
                                        st.divider() # Trennstrich, um die verschiedenen Abschnitte zu markieren
                            else:
                                st.write("Looks like there are no instructions - what about just going freestyle?")
                                st.divider() # Trennstrich, um die verschiedenen Abschnitte zu markieren
                        else:
                            st.write("No instructions available.") 
                            st.divider() # Trennstrich, um die verschiedenen Abschnitte zu markieren 

if __name__ == "__main__":
    main()


# Fusszeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal - Where Leftovers Meets Deliciousness. All rights reserved.")

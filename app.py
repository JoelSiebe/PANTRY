import streamlit as st
import requests

# Hintergrundbild
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://i.postimg.cc/P5ksXpm2/pexels-vladimir-gladkov-6208084.jpg");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: local;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Stil (nochmals anschauen, teils redundat mit zuvor)
page_bg_img = """
<style>
body {
    background-image: url("https://i.postimg.cc/P5ksXpm2/pexels-vladimir-gladkov-6208084.jpg");
    background-size: cover;
}
.stApp {
    color: white;
    font-size: 40px; /* Ändere die Schriftgröße hier */
}
.text-input-container {
    font-size: 30px !important; /* Ändere die Schriftgröße des Eingabefeld-Textes */    
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Titel und Header
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals",)
st.header("**Tame your kitchen with Pantry Pal**",)

# CSS Stil für Eingabefeld
st.write("""
<style>
div[data-baseweb="input"] input {
    color: black !important; /* Ändere die Schriftfarbe auf Schwarz */
    font-size: 20px !important; /* Ändere die Schriftgröße auf 20px */
}
</style>
""", unsafe_allow_html=True)

#API-Schlüssel
api_key = 1

# Zutatenliste des Benutzers als Eingabefeld
ingredients = st.text_input("Enter your fridge ingredients, separated by comma")

#API-Anfrage
url=f"https://www.themealdb.com/api/json/v1/1/list.php?a=list&i={ingredients}&apiKey={api_key}"
response = request.get(url)
data = response.json()

# Rezepte parsen
rezepte = []
for meal in data["meals"]:
    rezepte.append({
        "name": meal["strMeal"],
        "image": meal["strMealThumb"],
        "link": meal["strSource"]
    })

# Rezepte anzeigen
st.header("Look what we've found for you")
for rezept in rezepte:
    st.image(rezept["image"])
    st.write(rezept["name"])
    st.write(rezept["link"])

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")

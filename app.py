import streamlit as st

#Hintergrund mit Stock-Foto
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


# Titel und Header der Anwendung
st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

st.write("<style>div.Widget.stTextInput>div{background-color: #333333; padding: 40px; border-radius: 5px;}</style>", unsafe_allow_html=True)
# Eingabefeld für die Kühlschrank-Zutaten
ingredients = st.text_input("Enter your fridge ingredients, separated by comma")

# Schaltfläche, um Rezepte basierend auf den eingegebenen Zutaten anzuzeigen
if st.button("Show Recipes"):
    # Hier kannst du die Logik zum Abrufen von Rezepten basierend auf den eingegebenen Zutaten implementieren
    # In diesem Beispiel zeigen wir nur eine Platzhaltermeldung an
    st.write("Here, we will display recipes based on your ingredients")

# Fußzeile der Anwendung
st.markdown("---")
st.write("© 2024 Pantry Pal. All rights reserved.")
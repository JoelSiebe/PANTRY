import streamlit as st
import base64

st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

# Bilddateien in Bytes umwandeln
def img_to_bytes(img_path):
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# HTML-Code für das Bild generieren
def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html

# Hier setzen Sie den Pfad zu Ihrer lokalen Bilddatei ein
image_path = 'C:\\Users\\joels\\OneDrive - Universitaet St.Gallen\\Mastervorbereitungsstufe\\CS\\App\\PANTRY\\pexels-jane-doan-1099680.jpg'

# Das Bild in Markdown einfügen, unsafe_allow_html=True ermöglicht die Verwendung von HTML im Markdown
st.markdown(img_to_html(image_path), unsafe_allow_html=True)
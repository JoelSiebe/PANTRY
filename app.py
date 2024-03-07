from PIL import Image
import streamlit as st

st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

image = Image.open("C:\\Users\\joels\\OneDrive - Universitaet St.Gallen\\Mastervorbereitungsstufe\\CS\\App\\PANTRY\\1.jpg")
st.image(image, caption='Hi!', use_column_width=True)
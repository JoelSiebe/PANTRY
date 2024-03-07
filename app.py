from PIL import Image
import streamlit as st

st.title("Pantry Pal - Conquering Leftovers, Mastering Meals")
st.header("**Tame your kitchen with Pantry Pal**")

image_path = 'C:\Users\joels\OneDrive\Privat\Bilder\Pictures\pexels-jane-doan-1099680.jpg'
image = Image.open(image_path)
st.image(image, caption='Bildunterschrift hier', use_column_width=True)
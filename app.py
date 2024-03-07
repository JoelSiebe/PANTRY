import streamlit as st

# Titel der App
st.title("Pantry Pal - Mastering Meal, Conquering Leftovers")
st.header("Tame your kitchen with Pantry Pal!")

# Lokales Video
video_file = "Hintergrundvideo.mp4"

st.video(video_file)
st.video(video_file, start_time=0, autoplay=True)
# Textfeld für Eingabe
name = st.text_input("Geben Sie Ihren Namen ein:")

# Begrüßungstext
st.write("Hallo " + name + "!")

# Auswahlfeld
auswahl = st.selectbox("Wählen Sie eine Farbe:", ["Rot", "Grün", "Blau"])

# Ausgabe der Auswahl
st.write("Sie haben die Farbe " + auswahl + " gewählt.")

# Button
if st.button("OK"):
    st.write("Vielen Dank!")


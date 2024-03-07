import streamlit as st

# Titel der App
st.title("Erste Streamlit App in VS Code")

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


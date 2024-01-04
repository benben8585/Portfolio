"""
Streamlit Webanwendung zur Darstellung von Fernwärmeversorgern in Deutschland

Diese Anwendung lädt Daten aus einer Excel-Datei und ermöglicht es dem Nutzer, 
durch Eingabe eines Namens oder die Auswahl eines Bundeslandes nach spezifischen Fernwärmeversorgern zu suchen.
Die gefilterten Daten werden in einem übersichtlichen DataFrame präsentiert.

Die Anwendung demonstriert die Grundlagen der Datenaufbereitung und -darstellung in Streamlit.
"""

# Importieren der erforderlichen Bibliotheken
import streamlit as st        # Für das Erstellen der Web-App
import pandas as pd           # Zur Datenverarbeitung



# Laden der Daten
data = pd.read_excel(r'App/Versorger_gb_geocodiert.xlsx')

# Einfache Streamlit Anwendung
def main():
    st.title("Fernwärmeversorger in Deutschland")

    # Namenssuche
    name_query = st.text_input("Geben Sie den Namen des Versorgers ein:")

    # Bundesland-Auswahl über ein Listenfeld
    bundesland = st.selectbox("Wählen Sie ein Bundesland:", options=['Alle'] + list(data['Bundesland'].unique()))

    # Gefilterte Daten basierend auf der Bundesland-Auswahl und Namenssuche
    filtered_data = data
    if bundesland != 'Alle':
        filtered_data = filtered_data[filtered_data['Bundesland'] == bundesland]
    if name_query:
        filtered_data = filtered_data[filtered_data['Name des Betreibers'].str.contains(name_query, case=False, na=False)]

    # Anzeige der Daten
    st.write("Anzeige der Fernwärmeversorger:")
    st.dataframe(filtered_data)

if __name__ == "__main__":
    main()
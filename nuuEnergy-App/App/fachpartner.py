"""
Streamlit Webanwendung zur Visualisierung von Betriebsstandorten

Diese Anwendung verwendet verschiedene Technologien, um eine interaktive Karte bereitzustellen, auf der Nutzer Betriebsstandorte basierend auf
einer eingegebenen Adresse und einem ausgewählten Umkreisradius visualisieren können.
Sie nutzt die Google Maps API für Geocoding und Folium für die Kartendarstellung.
"""

# Importieren der erforderlichen Bibliotheken
import streamlit as st        # Für das Erstellen der Web-App
import pandas as pd           # Zur Datenverarbeitung
import folium                 # Zur Erstellung interaktiver Karten
from streamlit_folium import folium_static  # Zur Integration von Folium-Karten in Streamlit
import requests               # Für HTTP-Anfragen, z.B. für Geocoding
import geopy.distance         # Zur Berechnung von Distanzen
from config import gmaps_api_key  # Import des API-Keys für Google Maps

# Funktion zum Laden und Aufbereiten der Daten aus einer Excel-Datei
def load_data(filename):
    data = pd.read_excel(filename)
    # Konvertierung von Latitude und Longitude zu numerischen Werten
    data['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    # Behandlung von fehlenden Postleitzahlen
    if 'PLZ' in data.columns:
        data['PLZ'] = data['PLZ'].fillna(0).astype(int)
    # Entfernen von Einträgen ohne gültige Koordinaten
    return data.dropna(subset=['Latitude', 'Longitude'])


# Funktion zum Hinzufügen von Markern auf der Karte mit Hyperlinks
def add_markers(m, data):
    for _, row in data.iterrows():
        # Überprüfen, ob eine URL vorhanden ist und formatieren als HTML-Link
        website_link = f'<a href="{row["Website"]}" target="_blank">Website</a>' if pd.notna(row["Website"]) else 'Keine Website'
        
        popup_text = (f"<b>{row['Betriebsname']}</b><br>"
                      f"Adresse: {row['Adresse']}<br>"
                      f"PLZ: {row['PLZ']} Stadt: {row['Stadt']}<br>"
                      f"Tel: {row['Telefon']}<br>Email: {row['Email']}<br>"
                      f"{website_link}")
        folium.Marker(
            location=(row['Latitude'], row['Longitude']),
            popup=popup_text,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

# Funktion zum Geocoding einer Adresse mit Google Maps
def geocode_address_google(address):
    params = {
        "address": address,
        "key": gmaps_api_key
    }
    response = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            location = results[0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# Hauptfunktion der Streamlit-App
def main():
    st.title('Visualisierung von Betriebsstandorten')

    # Laden der Daten aus einer Excel-Datei
    data_file = r'App/BetriebeGeocodierte.xlsx'
    data = load_data(data_file)

    # Auswahl eines Bundeslandes für die Filterung der Daten
    bundeslaender = data['Bundesland'].unique()
    selected_bundesland = st.selectbox("Bundesland wählen:", ['Alle'] + list(bundeslaender))

    # Filtern der Daten basierend auf dem gewählten Bundesland
    if selected_bundesland != 'Alle':
        data = data[data['Bundesland'] == selected_bundesland]

    # Widget zur Eingabe einer Adresse und Auswahl eines Radius
    st.subheader("Geben Sie eine Adresse ein und wählen Sie einen Umkreis in km")
    address = st.text_input("Adresse")
    radius = st.slider("Radius in km", 0, 100, 10)  # Schieberegler für den Radius

    # Geocoding der eingegebenen Adresse
    lat, lon = None, None
    zoom_start = 6
    if address:
        lat, lon = geocode_address_google(address)
        if lat and lon:
            st.success(f"Koordinaten gefunden: {lat}, {lon}")
            zoom_start = 12
        else:
            st.error("Adresse konnte nicht gefunden werden.")

    # Erstellen der Karte mit Fokus auf die gegebene Adresse oder standardmäßig auf Deutschland
    if lat and lon:
        m = folium.Map(location=[lat, lon], zoom_start=zoom_start)
        # Zeichnen eines Kreises um den gegebenen Standort mit dem gewählten Radius
        folium.Circle(
            location=[lat, lon],
            radius=radius * 1000,  # Umwandlung von km in Meter
            color='red',
            fill=True,
            fill_opacity=0.2
        ).add_to(m)
        folium.Marker(
            location=[lat, lon],
            popup="Ihr Standort",
            icon=folium.Icon(color='red', icon='star', prefix='fa')
        ).add_to(m)
    else:
        m = folium.Map(location=[50, 10], zoom_start=6)

    # Filtern der Daten basierend auf dem gewählten Radius um die eingegebene Adresse
    if lat and lon:
        filtered_data = data[data.apply(lambda row: geopy.distance.distance((lat, lon), (row['Latitude'], row['Longitude'])).km <= radius, axis=1)]
        add_markers(m, filtered_data)
    else:
        filtered_data = pd.DataFrame()  # Leerer DataFrame, falls keine Adresse eingegeben wurde
        add_markers(m, data)

    # Anzeigen der Karte in der App
    folium_static(m, width=1280, height=700)

    # Anzeigen der gefilterten Betriebe unterhalb der Karte
    if not filtered_data.empty:
        st.subheader("Betriebe im Umkreis")
        st.dataframe(filtered_data)

if __name__ == "__main__":
    main()



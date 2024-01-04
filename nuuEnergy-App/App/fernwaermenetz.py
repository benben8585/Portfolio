"""
Streamlit-App zur Visualisierung von Fernwärmenetzen

Diese App ermöglicht es Benutzern, Fernwärmenetze in Deutschland auf einer interaktiven Karte zu visualisieren.
Benutzer können entweder alle Fernwärmenetze anzeigen lassen oder nach einer spezifischen Adresse suchen,
um die Fernwärmenetze in der Nähe dieser Adresse zu finden.
Die App verwendet Google Maps für das Geocoding und Folium für die Kartendarstellung.
"""

# Importieren der erforderlichen Bibliotheken
import streamlit as st                           # Für das Erstellen der Web-App
import pandas as pd                              # Zur Datenverarbeitung
import folium                                    # Zur Erstellung interaktiver Karten
from streamlit_folium import folium_static       # Zur Integration von Folium-Karten in Streamlit
import googlemaps                                # Importieren des Google Maps Client-Moduls

# Importieren des API-Keys aus einer separaten Konfigurationsdatei
# Der API-Key wird in einer externen Datei 'config.py' gespeichert, um die Sicherheit zu erhöhen und
# ihn getrennt vom Hauptcode zu halten. Dies ist eine bewährte Methode, um sensible Daten wie API-Keys
# zu verwalten und hilft, versehentliches Hochladen oder Teilen des Schlüssels zu vermeiden.
from config import gmaps_api_key

def main():
    # Initialisierung des Google Maps Clients mit dem API-Key
    gmaps = googlemaps.Client(key=gmaps_api_key)

    # Funktion zur Suche einer Adresse und Rückgabe der Geokoordinaten
    def search_address(address):
        result = gmaps.geocode(address)
        if result:
            location = result[0]['geometry']['location']
            return location['lat'], location['lng']
        return None, None

    # Funktion zum Erstellen und Konfigurieren der Karte mit Folium
    def create_map(df, search_lat=None, search_lng=None):
        # Auswahl des Zentrums und Zoom-Stufe der Karte
        if search_lat and search_lng:
            m = folium.Map(location=[search_lat, search_lng], zoom_start=12)
        else:
            m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)

        # Hinzufügen von Markern und Kreisen für jedes Fernwärmenetz in den Daten
        for index, row in df.iterrows():
            if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    icon=folium.Icon(color='green'),
                    tooltip=f"{row['Name des Betreibers']}, {row['Ort des Betreibers']}"
                ).add_to(m)
                folium.Circle(
                    location=[row['Latitude'], row['Longitude']],
                    radius=row['Netzlänge(in KM)'] * 1000,
                    color='blue',
                    fill=True,
                    fill_opacity=0.2
                ).add_to(m)

        # Hinzufügen eines Markers für die gesuchte Adresse, falls vorhanden
        if search_lat and search_lng:
            folium.Marker(
                location=[search_lat, search_lng],
                icon=folium.Icon(color='red', icon='star'),
                tooltip="Ihr Standort"
            ).add_to(m)

        return m

    st.title("Karte der Fernwärmenetze in Deutschland")

    # Schalter zur Auswahl zwischen Anzeige aller Fernwärmenetze oder Suche per Adresse
    show_all_networks = st.checkbox("Alle Fernwärmenetze anzeigen")

    searched_address = ""
    map_center_lat, map_center_lng = None, None
    if not show_all_networks:
        searched_address = st.text_input("Adresse eingeben:")
        if searched_address:
            map_center_lat, map_center_lng = search_address(searched_address)
            if map_center_lat and map_center_lng:
                st.write(f"Gefundene Koordinaten: {map_center_lat}, {map_center_lng}")
            else:
                st.write("Adresse nicht gefunden.")

    # Laden und Filtern der Fernwärmenetz-Daten aus einer Excel-Datei
    excel_file_path = r'App/FX_Fernwärmenetze_geocodiert.xlsx'
    data = pd.read_excel(excel_file_path)

    if not show_all_networks and searched_address:
        filtered_data = data # Filtern der Daten basierend auf der gesuchten Adresse
    else:
        filtered_data = data

    # Erstellen und Anzeigen der Karte mit den Fernwärmenetzdaten
    map_data = create_map(filtered_data, map_center_lat, map_center_lng)
    folium_static(map_data, width=1280, height=700)

if __name__ == "__main__":
    main()







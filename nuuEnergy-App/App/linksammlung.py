"""
Streamlit Webanwendung: Linksammlung-Seite

Diese Seite der Streamlit-Anwendung präsentiert eine Sammlung von nützlichen Links, die für das Projekt relevant sind. 
Die Links sind thematisch geordnet und bieten Zugang zu externen Ressourcen wie Energieversorgern, Geocoding-Diensten, 
Fachverbänden im Bereich Fernwärme und Plattformen für Energie-Atlasdaten. 
Jeder Link ist direkt anklickbar und führt den Nutzer zur entsprechenden Webseite.
"""

# Importieren der erforderlichen Bibliothek für das Erstellen der Web-App
import streamlit as st

# Definition der Funktion für die Linksammlungs-Seite
def links_page():
    # Setzen des Titels der Seite
    st.title("Linksammlung in Bezug auf dieses App Projekt")

    # Anzeigen verschiedener Kategorien von Links
    # Versorger
    st.header("Versorger:")
    st.write("Enerpipe = [Enerpipe Projekte](https://www.enerpipe.de/projekte/uebersicht-karte)")
    st.write("SWN = [Stadtwerke Neumünster](https://www.stadtwerke-neumuenster.de)")

    # Geocoding
    st.header("Geocoding:")
    st.write("API (Geocoding) = [Google Cloud Geocoding](https://cloud.google.com)")

    # Fachverbände im Bereich Fernwärme
    st.header("Fernwärme Fachverbände:")
    st.write("Der Energieeffizenzverband AGFW = [AGFW](https://www.agfw.de)")
    st.write("Bundesverband Fernwärmeleitungen = [BFWEV](https://www.bfwev.de/kontakt)")
    st.write("Plattform Grüne Fernwärme = [Grüne Fernwärme](https://www.gruene-fernwaerme.de/produktatlas-fernwaerme)")

    # Energie Atlasdaten
    st.header("Energie Atlasdaten:")
    st.write("Energie Atlas Bayern = [Energieatlas Bayern](https://www.energieatlas.bayern.de)")
    st.write("Geoportal = [Geoportal](https://www.geoportal.de/Themen/Energie_und_Umwelt/3_Energie.html)")

    # Fachpartner Adressen
    st.header("Fachpartner Adressen:")
    st.write("Viessmann = [Viessmann Partner-Suche](https://www.viessmann.de/de/partner-vor-ort-suche)")

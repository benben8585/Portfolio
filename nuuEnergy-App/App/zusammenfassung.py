"""
Dieses Skript ist Teil einer Streamlit-Anwendung, speziell für die Informationsseite der nuuEnergy App.
Die Seite bietet detaillierte Informationen über die App, ihre Verwendung, die zugrunde liegenden Daten und Technologien sowie häufig gestellte Fragen (FAQs).
Es werden verschiedene Aspekte der App wie die Funktionalität von Fachpartner-, Fernwärmenetz- und Fernwärmeversorger-Modulen erläutert.
Außerdem werden die verwendeten Technologien und Datenquellen aufgeführt.
Am Ende der Seite finden sich Kontaktinformationen und ein FAQ-Bereich.
"""

# Importieren der erforderlichen Bibliotheken
import streamlit as st        # Für das Erstellen der Web-App
def show_info_page():
    """Anzeigen der Informationsseite."""

    # Titel und Einleitung der Informationsseite
    st.title("Willkommen auf der Informationsseite zur nuuEnergy App")
    st.header("Die App dient zur Standortbestimmung für Wärmepumpen.")

    # Erklärung der Schlüsselfaktoren der App
    st.write("Wichtige Faktoren:")
    st.write("- Fernwärenetz")
    st.write("- - Netzlänge (In KM zum ermitteln des Radius für das Wärmenetzwerk)")
    st.write("- - Netzstandort (Adresse für den Standort und Mittelpunkt des Wärmenetzwerk)")
    st.write("- - Netzversorger (Kontaktdaten für Versorgungsanschluss)")
    st.write("- Fernwäreversorger")
    st.write("- - Kontaktdaten (Für Fernwärmeanbindung)")
    st.write("- Fachpartner mit Wärmepumpenspezialisierung")
    st.write("- - Für den Fachgerechten Einbau")
    st.write("- - Für Fachgerechte Wartung")

    # Anleitung zur Verwendung der App
    st.header("Wie man die App verwendet")
    st.write("- Fachpartner")
    st.write("- - Standortadresse eingeben von z.B. dem zuversorgendem Objekt")
    st.write("- - Gewünschten Radius einstellen")
    st.write("- - Es sind jetzt alle Fachpartner im gewünschten Radius auf der Karte sichtbar")
    st.write("- - Zusätzlich sind unter Karte detailierte Informationen(Kontaktdaten etc.) zu den Fachpartnern sichtbar")
    st.write("- Fernwärmenetz")
    st.write("- - Adresse eingeben oder nach Bundesland suchen")
    st.write("- - Es wird nun das gezeigt ob Fernwärmenetz in diesem Gebiet liegt")
    st.write("- - Im POI steht der Versorger")
    st.write("- Fernwärmeversorger")
    st.write("- - Name des Versorgers eingeben")
    st.write("- - Im unteren Bereich werden die vorhanden Kontaktdaten vereitgestellt")

    # Informationen über Daten und Technologien
    st.header("Daten und Technologien")
    st.write("- Fachpartner")
    st.write("- - Viesmann - Adressen und Kontaktdaten")
    st.write("- - PyCharm - Appprogramierung")
    st.write("- - Excel - Daten erfassung und Bereinigung")
    st.write("- - GoogleMaps API - API/Geocodierung")
    st.write("- Fernwärmenetz")
    st.write("- - PyCharm - Appprogramierung")
    st.write("- - Excel - Daten erfassung und Bereinigung")
    st.write("- - GoogleMaps API - API/Geocodierung")
    st.write("- - Bayern EnergieAtlas - Netzdaten")
    st.write("- - AGFW - Datenbeschaffung")
    st.write("- - Bundesverband Fernwärmeleitungen - Datenbeschaffung")
    st.write("- Fernwärmeversorger")
    st.write("- - PyCharm - Appprogramierung")
    st.write("- - Excel - Daten erfassung und Bereinigung")
    st.write("- - GoogleMaps API - API/Geocodierung")
    st.write("- - Bayern EnergieAtlas - Netzdaten")
    st.write("- - AGFW - Datenbeschaffung")
    st.write("- - Bundesverband Fernwärmeleitungen - Datenbeschaffung")

    # FAQ-Bereich
    st.header("FAQ - Häufig gestellte Fragen")
    st.write("- Hier könnten Sie Antworten auf häufig gestellte Fragen hinzufügen")
    st.write("- Beispiele für FAQs könnten sein: Wie funktioniert die Standortbestimmung?")

    # Kontaktinformationen und rechtliche Hinweise
    st.write("---")
    st.header("Kontakt und Impressum")
    st.write("© 2023 Student von DataCraft GmbH, Benjamin Binder, Brigitte Geiger")
    st.write("Im Auftrag der: nuuEnergy GmbH")
    st.write("Holzstrasse 28, 80469 München")
    st.write("Tel.: +49 171 5806157")
    st.write("Email: hello@nuuenergy.com")

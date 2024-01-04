"""
Streamlit App für nuuEnergy

Diese Streamlit-Anwendung dient als interaktives Dashboard für nuuEnergy, einer Plattform zur Standortanalyse.
Die App bietet verschiedene Funktionen und Ansichten, die es Benutzern ermöglichen, Informationen über Fernwärmenetze,
Fernwärmeversorger, Fachpartner und weitere relevante Inhalte zu erkunden.

Die Hauptfunktionen der App umfassen:
- Eine Hauptseite mit einer Begrüßungsnachricht und einem Einführungsvideo.
- Eine Informationsseite, die zusammenfassende Details und Hintergrundinformationen bietet.
- Eine Fachpartner-Seite für spezifische Informationen über Partnerunternehmen.
- Eine Seite, die sich auf Fernwärmenetze konzentriert, mit detaillierten Daten und Visualisierungen.
- Eine Seite für Fernwärmeversorger, die wichtige Informationen über diese Anbieter enthält.
- Eine Linksammlung mit nützlichen Ressourcen und weiterführenden Links.

Die Navigation zwischen diesen Seiten erfolgt über eine Seitenleiste, die eine einfache und intuitive Benutzerführung ermöglicht.
Der Wide Mode wird zu Beginn aktiviert, um den nutzbaren Bildschirmbereich zu maximieren und eine bessere Darstellung der Inhalte zu gewährleisten.

Die App ist modular aufgebaut, wobei jede Seite als separates Python-Modul implementiert ist.
Dies erleichtert die Wartung und Erweiterung der App.

Autor: Benjamin Binder
Version: 1.0.0
"""

# Importieren der erforderlichen Bibliotheken
import streamlit as st

# Aktivierung des Wide Mode für die gesamte Streamlit-Anwendung
st.set_page_config(layout="wide")

# Importieren der zusätzlichen Module für verschiedene Seiten der App
import fachpartner
import fernwaermeanbieter
import fernwaermenetz
import zusammenfassung
import linksammlung

# Definition der Hauptseite der App
def main_page():
    st.title("Willkommen bei nuuEnergy")
    st.write("Die App für ihre Standortanalyse.")

    # YouTube-Video Einbettung
    youtube_video_id = "Lt1cr1CqdW0"
    video_html = f"""
        <iframe width="800" height="450" src="https://www.youtube.com/embed/{youtube_video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    """
    st.markdown(video_html, unsafe_allow_html=True)

# Hauptfunktion der Streamlit-App
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Seiten", ["Hauptseite", "Information", "Fernwärmenetz", "Fernwärmeversorger", "Fachpartner", "Links"])

    # Anzeigen der ausgewählten Seite basierend auf Benutzerauswahl
    if page == "Hauptseite":
        main_page()
    elif page == "Information":
        zusammenfassung.show_info_page()
    elif page == "Fachpartner":
        fachpartner.main()
    elif page == "Fernwärmeversorger":
        fernwaermeanbieter.main()
    elif page == "Links":
        linksammlung.links_page()
    elif page == "Fernwärmenetz":
        fernwaermenetz.main()

if __name__ == "__main__":
    main()



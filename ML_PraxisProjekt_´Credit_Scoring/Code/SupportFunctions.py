import pandas as pd
import numpy as np


def annotate_bar_perc(plot, n_rows, text_size=14, text_pos=(0, 8), prec=2):
    """
    Funktion, die ein gestapeltes matplotlib Balkendiagramm mit Prozentlabels beschriftet.
    """

    # Annotiere die Balkendiagramme mit Kategorie-Prozent
    conts = plot.containers  # Hol Containers, für jede Klasse von Transported (True/False)

    for i in range(len(conts[0])):
        height = sum([cont[i].get_height() for cont in conts])  # Berechne Höhe der Säule
        text = f"{height / n_rows * 100:.{prec}f}%"  # Erstelle Annotation

        # Füge Text für jede große Säule hinzu
        plot.annotate(text,
                      (conts[0][i].get_x() + conts[0][i].get_width() / 2, height),  # Position xy
                      ha="center",  # Zentrierung
                      va="center",
                      size=text_size,
                      xytext=text_pos,  # Koordinaten des Textes, Koordinatensystem wird durch textcoords definiert
                      textcoords="offset points")  # Koordinatensystem (Also von der annotierten Position + xytext)
    return plot


def preprocess_PassengerId(data):
    """
    Preprozessiere die PassengerID. Gibt drei Spalten zurück:
        1. GroupID   - Eindeutige ID der Gruppe, zu der der Passagier gehört
        2. GroupPos  - Position in der Gruppe, die dem Passagier zugewiesen ist
        3. GroupSize - Neue Funktion, die jedem Passagier die Größe der Gruppe zuweist, zu der er gehört
    """

    new_ID = data.PassengerId.str.split("_", expand=True)
    new_ID.columns = ["GroupID", "GroupPos"]
    new_ID.GroupPos = new_ID.GroupPos.str.replace("0", "").astype(int)

    # Erhalte ein Wörterbuch von ID zu Gruppengröße (extrahiere max GroupPos aus Positionen in eindeutiger ID)
    group_size_dict = new_ID.groupby("GroupID").max().to_dict()["GroupPos"]

    # Weise jeder Zeile aus dem Wörterbuch die Gruppengröße zu
    new_ID["GroupSize"] = new_ID.apply(lambda row: group_size_dict[row["GroupID"]], axis=1)

    # Lösche vorangestellte 0en aus GroupID
    new_ID.GroupID = new_ID.GroupID.str.replace(pat=r"\b0+(?=\d)", repl="", regex=True).astype(int)

    return new_ID


def preprocess_Cabin(data):
    """
    Preprozessiere Cabin. Gibt drei Spalten zurück:
        1. Deck    - Buchstabe, der auf das Deck verweist, auf dem sich die Kabine befindet
        2. Number  - Kabinennummer
        3. Side    - Seite des Schiffs, entweder P für Backbord oder S für Steuerbord
    """

    new_cols = data.Cabin.str.split("/", expand=True)
    new_cols.columns = ["Deck", "CabinNum", "Side"]
    return new_cols


def preprosess_spaceship_titanic(df, log_transform_exp=False):
    """
    Funktion, die den DataFrame des Spaceship Titanic-Datensatzes entsprechend der im Notebook beschriebenen Prozesse vorverarbeitet.

    Gibt den vorverarbeiteten Datensatz zurück, der der Imputationsfunktion übergeben werden kann.

    Parameter:
    -----------

    df (pandas.DataFrame)   : Rohdaten-Pandas-DataFrame der Spaceship Titanic Challenge

    log_transform_exp (bool): Boolean zur Steuerung der Log-Transformation der Ausgaben


    Rückgabe:
    --------
    vorverarbeitet (pandas.DataFrame): Vorverarbeitetes Pandas DataFrame

    """

    # Kopiere den DataFrame
    vorverarbeitet = df.copy()

    # Konvertiere CryoSleep und VIP in bool
    vorverarbeitet[["CryoSleep", "VIP"]] = vorverarbeitet[["CryoSleep", "VIP"]].astype("bool")

    # Füge Spalte TotalExp hinzu
    vorverarbeitet["TotalExp"] = vorverarbeitet[["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]].sum(1)

    # Logarithmieren der Ausgaben (addiere eins, um -Inf zu vermeiden), wenn angegeben
    if log_transform_exp:
        vorverarbeitet[["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck", "TotalExp"]] = np.log(
            vorverarbeitet[["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck", "TotalExp"]] + 1)

    # Preprozessiere PassengerId
    vorverarbeitet = pd.concat([vorverarbeitet, preprocess_PassengerId(vorverarbeitet)], axis=1)

    # Preprozessiere Cabin
    vorverarbeitet = pd.concat([vorverarbeitet, preprocess_Cabin(vorverarbeitet)], axis=1)
    vorverarbeitet = vorverarbeitet.drop("Cabin", axis=1)

    return vorverarbeitet


def impute_group_category(group_categories, mode):
    """
    Funktion, die eine Serie kategorischer Merkmale einer Gruppe nimmt
    und den wahrscheinlichsten Wert zur Imputation findet.

    Der Modus (str) ist der Wert im Gesamtdatensatz, der am häufigsten vorkommt,
    und wird in Fällen verwendet, in denen keine Informationen aus den Gruppen vorliegen.
    """
    # Überprüfen, ob Gruppengröße > 1 ist
    if len(group_categories) > 1:

        # Erhalte eindeutige Planeten ohne NaN
        homes_count = group_categories.value_counts()

        if len(homes_count) == 1:  # Nur ein Planet in der Gruppe
            return homes_count.index[0]

        elif len(homes_count) == 0:  # Nur NaNs, ersetze durch Modus "Erde"
            return mode

        else:  # Mehr als ein Planet in der Gruppe

            if (homes_count == max(
                    homes_count)).sum() == 1:  # Wenn klare Entscheidung (max tritt nur einmal auf), übernehme sie
                return homes_count.idxmax()
            else:  # Es gibt zwei Planeten mit der gleichen maximalen Anzahl - wähle einen von ihnen zufällig aus, um Bias zu reduzieren
                np.random.seed(123)  # Setze den Zufallssamen für NumPy (wichtig für Reproduzierbarkeit)
                return np.random.choice(homes_count[homes_count == max(homes_count)].index)  # Wähle einen davon aus

    else:
        return mode


def impute_expenses(data, strategy):
    """
    Funktion, die den DataFrame nimmt und alle NaN-Ausgaben ersetzt
    gemäß der im vorherigen EDA beschriebenen Strategie.

    Gibt den DataFrame mit imputierten Ausgaben zurück.

    Parameter:
    -----------

    data (pandas.DataFrame): DataFrame mit NaN-Ausgaben

    strategy (str): String, der die Strategie zur Imputation von Ausgaben angibt.

                     Mögliche Werte sind:
                     - 'mean' für Mittelwert-Imputation
                     - 'median' für Median-Imputation
                     - 'group_mean' für Imputation basierend auf Gruppen
                     - 'group_median' für Imputation basierend auf Gruppen


    Rückgabe:
    --------

    expense_df (pandas.DataFrame): Imputierter Pandas DataFrame

    """

    # Kopiere df
    df = data.copy()

    if strategy == "median":
        # Jeder Index wird mit dem Wert in der Decken-Medianreihe gefüllt
        df = df.fillna({"RoomService": df.groupby("Deck")["RoomService"].transform("median"),
                        "FoodCourt": df.groupby("Deck")["FoodCourt"].transform("median"),
                        "Spa": df.groupby("Deck")["Spa"].transform("median"),
                        "VRDeck": df.groupby("Deck")["VRDeck"].transform("median"),
                        "ShoppingMall": df.groupby("Deck")["ShoppingMall"].transform("median")})

    elif strategy == "mean":
        # Jeder Index wird mit dem Wert in der Decken-Mittelwertreihe gefüllt
        df = df.fillna({"RoomService": df.groupby("Deck")["RoomService"].transform("mean"),
                        "FoodCourt": df.groupby("Deck")["FoodCourt"].transform("mean"),
                        "Spa": df.groupby("Deck")["Spa"].transform("mean"),
                        "VRDeck": df.groupby("Deck")["VRDeck"].transform("mean"),
                        "ShoppingMall": df.groupby("Deck")["ShoppingMall"].transform("mean")})

    elif strategy == "group_mean":
        # Jeder Index wird mit dem Mittelwert der Gruppe gefüllt, wenn die Gruppe größer als 1 ist (ansonsten Deckenmedian)
        df[df.GroupSize > 1] = df[df.GroupSize > 1].fillna(
            {"RoomService": df.groupby("GroupID")["RoomService"].transform("mean"),
             "FoodCourt": df.groupby("GroupID")["FoodCourt"].transform("mean"),
             "Spa": df.groupby("GroupID")["Spa"].transform("mean"),
             "VRDeck": df.groupby("GroupID")["VRDeck"].transform("mean"),
             "ShoppingMall": df.groupby("GroupID")["ShoppingMall"].transform("mean")})

        df[df.GroupSize == 1] = df[df.GroupSize == 1].fillna(
            {"RoomService": df.groupby("Deck")["RoomService"].transform("median"),
             "FoodCourt": df.groupby("Deck")["FoodCourt"].transform("median"),
             "Spa": df.groupby("Deck")["Spa"].transform("median"),
             "VRDeck": df.groupby("Deck")["VRDeck"].transform("median"),
             "ShoppingMall": df.groupby("Deck")["ShoppingMall"].transform("median")})

    elif strategy == "group_median":
        # Jeder Index wird mit dem Medianwert der Gruppe gefüllt, wenn die Gruppe größer als 1 ist (ansonsten Deckenmedian)
        df[df.GroupSize > 1] = df[df.GroupSize > 1].fillna(
            {"RoomService": df.groupby("GroupID")["RoomService"].transform("median"),
             "FoodCourt": df.groupby("GroupID")["FoodCourt"].transform("median"),
             "Spa": df.groupby("GroupID")["Spa"].transform("median"),
             "VRDeck": df.groupby("GroupID")["VRDeck"].transform("median"),
             "ShoppingMall": df.groupby("GroupID")["ShoppingMall"].transform("median")})

        df[df.GroupSize == 1] = df[df.GroupSize == 1].fillna(
            {"RoomService": df.groupby("Deck")["RoomService"].transform("median"),
             "FoodCourt": df.groupby("Deck")["FoodCourt"].transform("median"),
             "Spa": df.groupby("Deck")["Spa"].transform("median"),
             "VRDeck": df.groupby("Deck")["VRDeck"].transform("median"),
             "ShoppingMall": df.groupby("Deck")["ShoppingMall"].transform("median")})

    else:
        raise ValueError("Falscher Parameterwert angegeben.")

    return df


def impute_spaceship_titanic(vorbereiteter_df, wahrscheinlichkeits_imputation=True, ausgaben_strategie="group_mean", alters_strategie="group_mean", ausreißer_entfernen=False):
    """
    Funktion zur Imputation von Werten für den Spaceship Titanic-Datensatz basierend auf der vorherigen EDA.

    Gibt den Datensatz mit imputierten Werten zurück.

    Parameter:
    -----------

    vorbereiteter_df (pandas.DataFrame): Vorverarbeiteter DataFrame gemäß vorheriger EDA

    wahrscheinlichkeits_imputation (bool): Steuert, ob nur sichere Imputationen durchgeführt werden sollen oder ob
                                          auch wahrscheinlichkeitsbasierte Imputationen (basierend auf den in der EDA
                                          gefundenen Beziehungen) eingeschlossen werden sollen

    ausgaben_strategie (str): String, der die Strategie zur Imputation verschiedener Ausgabenkategorien angibt.

                             Mögliche Werte sind:
                             - 'mean' für die Mittelwert-Imputation
                             - 'median' für die Median-Imputation
                             - 'group_mean' für die Imputation basierend auf Gruppen
                             - 'group_median' für die Imputation basierend auf Gruppen

    alters_strategie (str): String, der die Strategie zur Imputation des Alters angibt.

                            Mögliche Werte sind:
                            - 'mean' für Mittelwert-Imputation
                            - 'median' für Median-Imputation
                            - 'group_mean' für die Imputation basierend auf Gruppen

    ausreißer_entfernen (bool): Legt fest, ob Ausreißer entfernt werden sollen


    Rückgabe:
    --------

    imputiert (pandas.DataFrame): Imputierter Pandas DataFrame

    """

    # DataFrame kopieren
    imputiert = vorbereiteter_df.copy()


    # Ausreißer/unplausible Datapoints im Schulungsszenario löschen:
    if ausreißer_entfernen:

        # Passagiere unter 12 Jahren, die alleine reisen, löschen
        imputiert = imputiert[~((imputiert.Alter<12) & (imputiert.GruppenGröße==1))]

        # Deck T verwerfen
        imputiert = imputiert[imputiert.Deck!="T"]



    # Beginne mit Imputationen, die während der EDA gefunden wurden und als 'sicher' gelten.

    # CryoSleep=True -> Alle Ausgaben sind 0
    ausgaben_spalten = ["Zimmerservice", "Food Court", "Einkaufszentrum", "Spa", "VR-Deck"]
    maske1 = imputiert.KryoSleep & imputiert.loc[:,ausgaben_spalten].isna().any(1)
    imputiert.loc[maske1, ausgaben_spalten] = imputiert.loc[maske1, ausgaben_spalten].fillna(0)

    # TotalExp > 0 -> CryoSleep=False
    imputiert[imputiert.GesamtAusgaben>0] = imputiert[imputiert.GesamtAusgaben>0].fillna({"KryoSleep":0})

    # CryoSleep=False aber Alter <= 12 -> Alle Ausgaben sind 0
    maske2 = ~imputiert.KryoSleep & imputiert.loc[:,ausgaben_spalten].isna().any(1)
    imputiert.loc[maske1, ausgaben_spalten] = imputiert.loc[maske1, ausgaben_spalten].fillna(0)

    # Deck=G -> VIP=False und Heimatplanet=Erde
    imputiert[imputiert.Deck=="G"] = imputiert[imputiert.Deck=="G"].fillna({"VIP":False, "Heimatplanet":"Erde"})

    # Deck A, B oder C -> Heimatplanet=Europa
    imputiert[imputiert.Deck.isin(["A", "B", "C"])] = imputiert[imputiert.Deck.isin(["A", "B", "C"])].fillna({"Heimatplanet":"Europa"})



    # Wenn angegeben, werden die probabilistischen Imputationen auch im folgenden Code ausgeführt.

    if wahrscheinlichkeits_imputation:

        # Fehlende VIPs auf False setzen (insgesamt nur 2,3% VIPs, also sehr wahrscheinlich)
        imputiert = imputiert.fillna({"VIP":False})

        # CryoSleep=NaN aber Alter<=12 -> CryoSleep=False (aus obiger Analyse)
        imputiert[imputiert.KryoSleep.isna() & (imputiert.Alter<=12)] = imputiert[imputiert.KryoSleep.isna() & (imputiert.Alter<=12)].fillna({"KryoSleep":False})

        # CryoSleep=NaN aber Alter>12 -> CryoSleep=True
        imputiert[imputiert.KryoSleep.isna() & (imputiert.Alter>12)] = imputiert[imputiert.KryoSleep.isna() & (imputiert.Alter>12)].fillna({"KryoSleep":True})

        # Imputiere Ziel mit Ziel aus der Gruppe, sonst mit dem wahrscheinlichsten: TRAPPIST-1e
        imputiert["Ziel"] = imputiert["Ziel"].fillna(imputiert.groupby("GruppenID")["Ziel"].transform(impute_group_category, mode="TRAPPIST-1e"))

        # Imputiere Heimatplanet mit Heimatplanet aus der Gruppe, sonst mit dem wahrscheinlichsten: Erde
        imputiert["Heimatplanet"] = imputiert["Heimatplanet"].fillna(imputiert.groupby("GruppenID")["Heimatplanet"].transform(impute_group_category, mode="Erde"))

        # Imputiere Deck mit Deck aus der Gruppe, sonst mit dem wahrscheinlichsten: F
        imputiert["Deck"] = imputiert["Deck"].fillna(imputiert.groupby("GruppenID")["Deck"].transform(impute_group_category, mode="F"))

        # Imputiere Seite mit Seite aus der Gruppe, sonst mit "Missing":
        imputiert["Seite"] = imputiert["Seite"].fillna(imputiert.groupby("GruppenID")["Seite"].transform(impute_group_category, mode="Missing"))

        # Imputiere Kabinennummer mit Kabinennummer aus der Gruppe, sonst mit "Missing":
        imputiert["KabinenNummer"] = imputiert["KabinenNummer"].fillna(imputiert.groupby("GruppenID")["KabinenNummer"].transform(impute_group_category, mode="Missing"))


        # Alle Ausgaben = 0 außer NaN-Werten -> andere Ausgaben auch mit hoher Wahrscheinlichkeit








def post_imputation_process_spaceship_titanic(imputierter_df, war_log_transformiert):
    """
    Funktion, die nach der Imputation angewendet wird, um TotalExp neu zu berechnen
    und boolesche Spalten für das Alleinreisen und das Ausgeben von nichts hinzuzufügen.

    Gibt den endgültigen DataFrame zurück.


    Parameter:
    -----------

    imputierter_df (pandas.DataFrame): DataFrame nach Vorverarbeitung und Imputation

    war_log_transformiert (bool): Boolean, der steuert, ob die Ausgaben log-transformiert wurden
                                  (wichtig für die Aktualisierung von TotalExp)


    Rückgabe:
    --------

    final (pandas.DataFrame): Endgültiger Pandas DataFrame

    """

    # DataFrame kopieren
    final = imputierter_df.copy()

    # Kleine Anzahl von verbleibenden NaNs imputieren
    final = final.fillna({"CryoSleep": False, "Alter":final.Alter.mean().round()})

    # Alter in Integer umwandeln
    final.Alter = final.Alter.astype(int)

    # TotalExp aktualisieren
    if war_log_transformiert: # Wenn sie log-transformiert waren, zurücktransformieren, neu berechnen, transformieren
        final[['Zimmerservice', 'Food Court', 'Einkaufszentrum', 'Spa', 'VR-Deck']] = np.exp(final[['Zimmerservice', 'Food Court', 'Einkaufszentrum', 'Spa', 'VR-Deck']])-1
        final["TotalExp"] = final[['Zimmerservice', 'Food Court', 'Einkaufszentrum', 'Spa', 'VR-Deck']].sum(1)

        # Erneut transformieren
        alle_ausgaben_spalten = ['Zimmerservice', 'Food Court', 'Einkaufszentrum', 'Spa', 'VR-Deck', 'TotalExp']
        final[alle_ausgaben_spalten] = np.log(final[alle_ausgaben_spalten]+1)

        # Ein Präfix hinzufügen, um als log-transformiert zu markieren
        final.columns = [f"Log{col}" if col in alle_ausgaben_spalten else col for col in final.columns]

    else: # Wenn die Ausgaben nicht log-transformiert waren
        final["TotalExp"] = final[['Zimmerservice', 'Food Court', 'Einkaufszentrum', 'Spa', 'VR-Deck']].sum(1)

    # Marker für 0 Ausgaben hinzufügen
    if war_log_transformiert:
        final["KeineAusgaben"] = (final.LogTotalExp == 0)
    else:
        final["KeineAusgaben"] = (final.TotalExp == 0)

    # Marker für das Alleinreisen hinzufügen
    final["Alleine"] = (final.GruppenGröße == 1)

    return final


def preprocess_impute_spaceship_titanic(df, **kwargs):

    """
    Funktion, die die gesamte Vorverarbeitungspipeline zusammenführt.

    Gibt den endgültigen DataFrame zurück.


    Parameter:
    -----------

    df (pandas.DataFrame): Rohdaten des Spaceship Titanic Pandas DataFrame

    kwargs               : Alle anderen Schlüsselwortargumente für andere Funktionen:
                           - log_transform_exp
                           - proba_imp
                           - expense_strat
                           - age_strat

    Weitere Informationen zu kwargs:

    proba_imp (bool)                  : Boolean, der steuert, ob nur sichere Imputationen durchgeführt werden sollen
                                        oder ob auch wahrscheinlichkeitsbasierte Imputationen (basierend auf den in
                                        der EDA gefundenen Beziehungen) eingeschlossen werden sollen

    expense_strat (str)               : String, der die Strategie zur Imputation verschiedener Ausgabenkategorien angibt.

                                        Mögliche Werte sind:
                                        - 'mean' für Mittelwert-Imputation
                                        - 'median' für Median-Imputation
                                        - 'group_mean' für die Imputation basierend auf Gruppen
                                        - 'group_median' für die Imputation basierend auf Gruppen

    age_strat (str)                   : String, der die Strategie zur Imputation des Alters angibt.

                                        Mögliche Werte sind:
                                        - 'mean' für Mittelwert-Imputation
                                        - 'median' für Median-Imputation
                                        - 'group_mean' für die Imputation basierend auf Gruppen


    Rückgabe:
    --------

    final_df (pandas.DataFrame): Endgültiger Pandas DataFrame nach Vorverarbeitungs-Pipeline

    """

    # Standardwerte für kwargs festlegen
    kwargs.setdefault('log_transform_exp', False)
    kwargs.setdefault('proba_imp', True)
    kwargs.setdefault('expense_strat', 'group_mean')
    kwargs.setdefault('age_strat', 'group_mean')
    kwargs.setdefault('drop_outliers', False)

    # DF vorverarbeiten
    vorverarbeiteter_df = preprosess_spaceship_titanic(df, log_transform_exp=kwargs['log_transform_exp'])

    # Fehlende Werte imputieren
    imputierter_df = impute_spaceship_titanic(vorverarbeiteter_df,
                                             proba_imp=kwargs['proba_imp'],
                                             expense_strat=kwargs['expense_strat'],
                                             age_strat=kwargs['age_strat'],
                                             drop_outliers=kwargs['drop_outliers'])

    # Vorverarbeitung abschließen
    final_df = post_imputation_process_spaceship_titanic(imputierter_df, war_log_transformiert=kwargs['log_transform_exp'])

    return final_df

import pandas as pd
import json # seulement pour l'affichage
import sys


dico_mois = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}


def main():
    if len(sys.argv) == 1:
        print("usage : colonne_dates fichier1 [fichier2 ...]")
        return 1
    noms_fichiers = sys.argv[1:]
    # noms_fichiers = ["Tableau_GC.csv"]
    for nom_fichier in noms_fichiers:
        df = pd.read_csv(nom_fichier, sep=";", header=0)
        df2 = df.copy()
        # for date in df.Date_publication:
        for indice_date in range(len(df.Date_publication)):
            date_publication = df.Date_publication[indice_date]
            mois, jour, annee = date_publication.split()
            if mois in dico_mois:
                # print(f"nouvelle date_publication : {dico_mois[mois]:02d}/{annee}")
                df2.Date_publication[indice_date] = f"{dico_mois[mois]:02d}/{annee}"
            else:
                print(f"[Erreur] mois non présent dans le dico : {mois}")
                sys.exit(1)
            date_experience = df.Date_experience[indice_date]
            try:
                liste_date = date_experience.split()
                # S'il y a le jour aussi
                if len(liste_date) > 2:
                    mois, jour, annee = liste_date
                else:
                    mois, annee = liste_date
                if mois in dico_mois:
                    # print(f"nouvelle date_experience : {dico_mois[mois]:02d}/{annee}")
                    df2.Date_experience[indice_date] = f"{dico_mois[mois]:02d}/{annee}"
                else:
                    print(f"[Erreur] mois non présent dans le dico : {mois}")
                    sys.exit(1)
            except Exception as e:
                # print(f"[Avertissement] date experience non valide : {df2.Date_experience[indice_date]}", e)
                df2.Date_experience[indice_date] = df2.Date_publication[indice_date]

        df2.to_csv("Tableaux_convertis/Converti_" + nom_fichier, sep=";", index=False)


if __name__ == "__main__":
    main()

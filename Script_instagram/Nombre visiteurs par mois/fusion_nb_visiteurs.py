import pandas as pd


nom_fichier_sortie = "nb_visiteurs_tripadvisor_SA.csv"

noms_fichiers = ["nb_visiteurs_tripadvisor_SA_Concepcion.csv",
                 "nb_visiteurs_tripadvisor_SA_Espada.csv",
                 "nb_visiteurs_tripadvisor_SA_San_Jose.csv",
                 "nb_visiteurs_tripadvisor_SA_San_Juan.csv"]

resultat = {}
for nom_fichier in noms_fichiers:
    print(f"[Avertissement] Analyse du fichier : {nom_fichier}")
    df = pd.read_csv(nom_fichier, sep=";", header=0)
    for i in range(len(df)):
        ligne = df.iloc[i]
        if ligne.mois not in resultat:
            resultat[ligne.mois] = 0
        resultat[ligne.mois] += ligne.nb_visiteurs
        # print(f"nouvelle ligne : {resultat[ligne.mois]=}")

# print("resultat :")
# print(resultat)
dico = [{"mois": mois, "nb_visiteurs": nb_visiteurs} for mois, nb_visiteurs in resultat.items()]
df = pd.DataFrame.from_records(dico) # attention : ne retourne pas les dates triées
# print(df)
df.to_csv(nom_fichier_sortie, sep=";", index=False)
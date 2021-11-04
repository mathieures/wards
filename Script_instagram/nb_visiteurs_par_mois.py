import pandas as pd
#import json # seulement pour l'affichage
import sys

def obtenir_visiteurs_csv(nom_fichier_csv, colonne_dates, parse=True, sep=","):
	resultat = {}
	print("nom fichier csv :", nom_fichier_csv)
	if parse:
		df = pd.read_csv(nom_fichier_csv, sep=sep, header=0, parse_dates=[colonne_dates])
		for date in df.date_publication:
			mois_et_annee = "/".join((f"{date.month:02d}", str(date.year)))
			if mois_et_annee not in resultat:
				resultat[mois_et_annee] = 0
			resultat[mois_et_annee] += 1
	else:
		df = pd.read_csv(nom_fichier_csv, sep=sep, header=0)
		# On accede a la colonne colonne_dates
		for mois_et_annee in df.iloc[:,colonne_dates]:
			if mois_et_annee not in resultat:
				resultat[mois_et_annee] = 0
			resultat[mois_et_annee] += 1
	return resultat

def main():
	if len(sys.argv) == 1:
		print("usage : [parse] [sep:<separateur>] colonne_dates fichier1 [fichier2 ...]")
		return 1
	if sys.argv[1] == "parse":
		print("[Avertissement] Parsage des dates activé.")
		parse = True
		sys.argv.pop(1)
	else:
		parse = False
	if sys.argv[1].startswith("sep:"):
		sep = sys.argv[1].split(":")[1]
		sys.argv.pop(1)
	else:
		sep = ";"
	colonne_dates, noms_fichiers = int(sys.argv[1]), sys.argv[2:]
	# noms_fichiers = ["donnees_insta_south_rim.csv", "donnees_insta_san_antonio.csv"]
	visiteurs = {}
	if noms_fichiers:
		for nom_fichier in noms_fichiers:
			nom_donnees = nom_fichier.split(".")[-2].strip("\\").strip("/")
			# visiteurs[nom_donnees] = obtenir_visiteurs_csv(nom_fichier, int(colonne_dates), parse=parse, sep=";")
			dico_nb_visiteurs = obtenir_visiteurs_csv(nom_fichier, int(colonne_dates), parse=parse, sep=sep)
			df = pd.DataFrame(["date", "nb_visiteurs"])
			print("dico :", dico_nb_visiteurs)
			print(f"nom csv : {'nb_visiteurs_' + nom_donnees + '.csv'}")
			donnees = [ (mois, nb) for mois, nb in dico_nb_visiteurs.items() ]
			df = pd.DataFrame.from_records(donnees, columns=['mois', 'nb_visiteurs'])
			# print(df)
			nom_nouveau_csv = "nb_visiteurs_" + nom_donnees + ".csv"
			print("On écrit dans :", nom_nouveau_csv)
			df.to_csv(nom_nouveau_csv, sep=";", index=False) # On separera toujours avec des points-virgules


		# print(json.dumps(visiteurs, indent=4))

if __name__ == "__main__":
	main()
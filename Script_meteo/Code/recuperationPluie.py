import requests
from bs4 import BeautifulSoup
import os

def recupMeteo(lieu,annee,fichierSource):

    listUrl = []

    i = ["01","02","03","04","05","06","07","08","09","10","11","12"]

    base = 'https://www.historique-meteo.net/amerique-du-nord/etats-unis/'

    if lieu == "san-antonio":
        lieu = "austin"  # Réécriture pour le site

    for j in range(12):
        
        listUrl.append(base+lieu+"/"+annee+"/"+i[j]+"/")


    f = open(fichierSource,"w")
    sep = ","

    for url in listUrl:

        #print(url)

        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")     # soup contient le code HTML de url


        tag = soup.find(class_= "table table-striped")    # recherche de la balise qui nous interesse

        try:  # Pour 2021 il n'y a pas les 12 mois dont ça plante (soup.find(...) renvoie NULL est NULL.tbody plante)
            tag = tag.tbody                                   # recherche de la balise qui nous interesse
        except:
            return

        list_tr = tag.find_all("tr")                      # recherche de la balise qui nous interesse

        for tr in list_tr:
            list_td = tr.find_all("td")
            td = list_td[2]
            list_b = td.find_all("b")
            b = list_b[1]
            texte = b.string[:-2]                         # On enleve 'mm' de la fin de la chaine
            f.write(texte)
            if not(tr == list_tr[-1]): # Pour pas avoir de séparateur a la fin
                f.write(sep)

        if not(url == listUrl):  # Pour pas avoir de retour a la ligne a la fin
            f.write("\n")

    f.close()


def main():
    lieu = ["san-antonio","grand-canyon"]  # austin pour San Antonio
    annee = ["2018","2019","2020","2021"]  
    base = "./DonnéesMeteo/USA/"

    for l in lieu:
        path = base + l + "/Pluie/"
        for a in annee:
            fichier = path + l + a + ".csv"
            recupMeteo(l,a,fichier)

def test():
    recupMeteo("austin","2021","./DonnéesMeteo/USA/austinTest/austin2021.csv")


if __name__ == "__main__":
    main()
    #test()
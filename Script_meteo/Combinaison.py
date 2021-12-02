import calendar
from datetime import datetime

from numpy.core.arrayprint import DatetimeFormat
from Code import recuperationTemp
from Code import recuperationPluie
import pandas
import re
import os

def _mkdir_recursive(path):   # Pris sur internet  Fait un mkdir recursif
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        _mkdir_recursive(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

"""def getDatetime(annee):  # Renvoie une liste de datetime de l'année
    l = []
    for m in range(1,13):
        _,nbJour = calendar.monthrange(annee,m)
        for j in range(1,nbJour+1):
            l.append(datetime(annee,m,j))    
    return l"""

def recupFichier(path):
    try:
        f = open(path,"r")
    except:

        if not(re.search(".*Pluie.*",path) == None):  # Si le chemin contient Pluie
            recuperationPluie.main()              # Signifie que les documents de Pluie ne sont pas créé
            f = open(path,"r")  # Devrait marcher maintenant

        elif not(re.search(".*Temp.*",path) == None):
            recuperationTemp.main()
            f = open(path,"r")

    lines = f.readlines()
    f.close()

    #print("fichier {} : Nombre de ligne (mois) : {}".format(path,len(lines)))

    donnees = []
    for line in lines:
        a = line.split(",")
        a[-1] = a[-1][:-1]        # En gros a[-1] est la derniere donnees de la ligne donc il y a un \n a[-1][:-1] l'enleve
        a = [float(i) for i in a] # Convertion
        moy = sum(a)/len(a)  # Moyenne par mois
        
        donnees.append(moy)

    mois = len(lines)  # Combien de ligne = nombre de mois
    return mois,donnees

def creationFichier(lieu,type,base):  # Pas fou mais bon ... Nan en vrai c'est cool
    os.chdir("/home/thomas/Documents/Cours/M1/Semestre 1/ProjetIntégré/CodeGit/wards/Script-meteo")   #A modifier pour le projet final
    for l in lieu:
        for t in type:
            path = base + l + "/" + t + "/"
            _mkdir_recursive(path)

def getDataFrame():
    lieu = ["san-antonio","grand-canyon"]
    type = ["Temp","Pluie"]
    annee = ["2018","2019","2020","2021"]
    base = "./DonnéesMeteo/USA/"

    creationFichier(lieu,type,base)

    liste = [] # Liste contenant les dico des lieux
    
    for l in lieu:
        dateListe = []
        tempListe = []
        pluieListe = []
        dico = {}              

        for a in annee:
            for t in type:
                path = base + l + "/" + t + "/"            

                newPath = path + l + a +".csv"
                mois,donnees = recupFichier(newPath)

                if t == "Temp": # Moche ...
                    tempListe.extend(donnees)
                else:
                    pluieListe.extend(donnees)

            date = [ (f"{m+1:02d}") + "/" + str(a) for m in range(mois) ]

            dateListe.extend(date)
  
        dico["Date"] = dateListe
        dico["Temp"] = tempListe
        dico["Pluie"] = pluieListe

        m = len(dico["Date"])                         # On récupere la taille des date
        dico["Temp"] = dico["Temp"][:m]               # Et on donne la meme taille au different dico en fonction de la taille de date
        dico["Pluie"] = dico["Pluie"][:m]

        liste.append(dico)

    dataframe = {}
        
    for i,d in enumerate(liste):
        df = pandas.DataFrame(d)
        dataframe[lieu[i]] = df

    return dataframe
def ecritDataFrame(dico):
    for k,v in dico.items():
        nomFichier = "meteo_" + k + ".csv"
        v.to_csv(nomFichier,sep=";",index=False)

    

if __name__ == "__main__":
    dicoDf = getDataFrame()
    ecritDataFrame(dicoDf)

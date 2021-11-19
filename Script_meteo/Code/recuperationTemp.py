import calendar
#https://meteostat.net/fr/place/2E2MPO?t=2018-01-01/2018-10-21

def stockageTemp(dossier,dossierArrive,annee,lieu):
    path = dossier + annee + ".csv"
    fIn = open(path,"r")
    lines = fIn.readlines()  # lines = liste avec toute les lignes
    fIn.close()

    newPath = dossierArrive + lieu + annee +  ".csv"
    fOut = open(newPath,"w")

    i = 1   # La premiere ligne est l'entete, on en a pas besoin
    m = 1   # Premier mois 
    while (i < len(lines)):
        premierJour,nbJour = calendar.monthrange(int(annee),m)

        l = [] 
        for j in range(nbJour):                                      #Boucle sur 1 mois
            temp = lines[i].split(",")
            if temp[1] == "": # On a rencontré des données vides
                if annee == '2021':
                    i = len(lines) # On arrete
                    break
                else:
                    l.append(l[-1])
            else:
                l.append(temp[1])       #La Temp est le deuxieme element de la ligne
            i += 1

        fOut.write(",".join(l))
        
        if not(i == len(lines)-1):
            fOut.write("\n")

        m += 1
        
    fOut.close()

def main():
    lieu = ["grand-canyon","san-antonio"]
    dossier = ["./Données/GrandCanyon/","./Données/SanAntonio/"]
    dossierArrive = ["./DonnéesMeteo/USA/grand-canyon/Temp/","./DonnéesMeteo/USA/san-antonio/Temp/"]
    annee = ["2018","2019","2020","2021"]
    
    for i in range(len(dossier)):
        for a in annee:
            l = lieu[i]
            stockageTemp(dossier[i],dossierArrive[i],a,l)


if __name__ == "__main__":
    main()
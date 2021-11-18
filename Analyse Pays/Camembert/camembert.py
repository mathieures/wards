import unidecode
import matplotlib.pyplot as plt



def getDico(nomFichier):
    try:
        fichier = open(nomFichier,"r")
    except:
        print(f"Erreur d'ouverture du fichier {nomFichier}")
        exit(1)
    
    lines = fichier.readlines()
    fichier.close()

    dico = {}

    lines = lines[1:] #On enleve l'entete
    for line in lines:
        l = []
        temp = line.split(',')
        l.append(temp[0])
        l.append((int)(temp[1].split(';')[0]))  # Format bizarre pour le fichier csv mdr

        #l[0] = l[0].replace(' ','+')
        #l[0] = unidecode.unidecode(l[0])
        dico[l[0]] = l[1]
    
    return dico

def nMax(dico, n):
    maxi = []
    index = list(dico.keys())

    while(n > 0):
        tmp = 0
        cle = index[tmp]
        val = dico[cle]
        while (cle in maxi):   # Pour debug
            tmp += 1
            cle = index[tmp]
            val = dico[cle]

        for i in range(len(dico)):
            cleTemp = index[i]
            if (dico[cleTemp] >= val):
                if(cleTemp not in maxi):
                    cle = cleTemp
                    val = dico[cleTemp]

        maxi.append(cle)
        n -= 1

    return maxi


    


def main():
    nomFichier = ["../../datas/pays_origine_GC.csv", "../../datas/pays_origine_SA.csv"]
    sortie = ["GC","SA"]

    for i,f in enumerate(nomFichier):
        dico = getDico(f)

        label = nMax(dico, 5)
        
        val = [dico[k] for k in label]
        acc = sum([dico[k] for k in label])  # Valeur totale de personne dans le top 5

        """val = []
        for lab in label:
            val.append(dico[lab]/acc)"""

        autre = sum([dico[k] for k in dico if k not in label])
        val.append(autre)

        plt.figure(figsize= (6,6))

        plt.pie(val,labels=label+["Autres"],
                      normalize=True,
                      autopct = lambda x: str(round(x, 2)) + '%')

        plt.savefig(f"Camembert_{sortie[i]}.png")

        
        


        

            




if __name__ == "__main__":
    main()

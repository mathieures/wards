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

        autre = sum([dico[k] for k in dico if k not in label])
        val.append(autre)

        plt.figure(figsize= (8,8))

        patches, texts, autotexts = plt.pie(val,
                labels=label+["Autres"],
                textprops={'fontsize': 13},
                normalize=True,
                autopct = lambda x: str(round(x, 2)) + '%',
                pctdistance=0.83)

        for k in autotexts:
            k.set_color('white')
            k.set_fontsize(16)

        plt.savefig(f"Camembert_{sortie[i]}.png")

        
        


        

            


def test():
    frac=[1.40 , 10.86 , 19.31 , 4.02 , 1.43 , 2.66 , 4.70 , 0.70 , 0.13 , 1.48, 32.96 , 1.11 , 13.30 , 5.86]
    labels=['HO0900344', 'HO0900331', 'HO0900332', 'HO0900354', 
            'HO0900358', 'HO0900374', 'HO0900372', 'HO0900373', 
            'HO0900371', 'HO0900370', 'HO0900369', 'HO0900356', 
            'HO0900353', 'HO0900343']

    colors=('b', 'g', 'r', 'c', 'm', 'y', 'burlywood', 'w')

    plt.figure(figsize=(8,8))
    patches, texts, autotexts = plt.pie(frac, colors=colors, labels=labels, autopct='%1.1f%%',textprops={'fontsize': 14})
    for i in autotexts:
        i.set_color('white')
        i.set_fontsize(30)
    #autotexts = map(lambda t: t.set_fontsize(30),autotexts)
    plt.show()

if __name__ == "__main__":
    main()
    #test()

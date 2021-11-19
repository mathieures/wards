import folium
from folium.plugins import MarkerCluster
from random import randrange
import urllib.request
import urllib.parse
#from urllib.error import HTTPError, URLError
import xmltodict
#from math import ceil, sqrt, log
import unidecode

#https://github.com/Guillaume-Fgt/Folium_Villes_Fleuries_Idf
#https://www.data.gouv.fr/fr/reuses/creation-dune-carte-interactive-en-utilisant-le-langage-python/
#https://ichi.pro/fr/visualisation-interactive-des-cartes-avec-folium-en-python-51218899373467

apiKey= 'UDWAHmYwAuMrAOIpg3u7Ccz66A2NjbDX'

def to_hex(n):
    return hex(n)[2:]

def to_color(triplet):
    return f"#{''.join(to_hex(entier) for entier in triplet)}"

def rand_color():
    return to_color([randrange(256) for _ in range(3)])

def getCountryAndCoord(place):
    url = 'https://api.tomtom.com/search/2/geocode/'+place+'.xml?language=fr-FR&limit=1&key='+apiKey
    data = urllib.request.urlopen(url)
    data = xmltodict.parse(data.read().decode('utf-8'))
    
    country=data["response"]["results"]["item"]["address"]["country"]

    lat=data["response"]["results"]["item"]["position"]["lat"]
    lon=data["response"]["results"]["item"]["position"]["lon"]
    #print("Pays : "+country+ "\nCoord: "+lon+", "+lat)
    return {
        "country":country,
        "lat":lat,
        "long":lon
        }

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

        l[0] = l[0].replace(' ','+')
        l[0] = unidecode.unidecode(l[0])
        dico[l[0]] = l[1]
    
    return dico


"""
def nMax(l, n):
    lcopy = l.copy()
    res = []
    for i in range(n):
        m = max(lcopy)
        lcopy.remove(m)
        res.append(m)
    
    return res
"""


def main():
    nomFichier = ["../../datas/pays_origine_GC.csv", "../../datas/pays_origine_SA.csv"]
    nomLieux = ["GC","SA"]

    memoire = {}

    for i,f in enumerate(nomFichier):
        dico = getDico(f)
        m = folium.Map(location=[0, 0],zoom_start= 2)
        marker_cluster = MarkerCluster().add_to(m)

        for k,v in dico.items():
            if k not in memoire.keys():
                pays = getCountryAndCoord(k)
                p = pays['country']
                lat = pays['lat']
                long = pays['long']
                memoire[k] = (p , (lat,long)) # tuple de la forme  (nomPays (latitude,longitude))
            else:
                pays = memoire[k]
                p = pays[0]
                lat = pays[1][0]
                long = pays[1][1]

            if (v/2 <= 10):
                r = 10
            else:
                r = min(100,v/2)

            folium.CircleMarker(
                location=(lat,long),
                tooltip= f"{p} : {v} visiteurs",
                radius= r,
                color= rand_color(),
                fill= True,
                fill_opacity= 0.75
            ).add_to(marker_cluster)

            m.save(f"{nomLieux[i]}.html")


if __name__ == "__main__":
    main()


    """s = "curaçao"
    dico = getCountryAndCoord(s)
    print(dico)"""
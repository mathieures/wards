import sys
import urllib.request
import json
import xmltodict
import plotly.express as px
import urllib.parse
from pandas_ods_reader import read_ods
import time
import pandas
from urllib.error import HTTPError, URLError
start_time = time.time()


apiKey= 'UDWAHmYwAuMrAOIpg3u7Ccz66A2NjbDX'

path= "Tableau_GC.ods"
df_GC=read_ods(path)
places=df_GC["Location"].tolist()
'''
path= "Tableau_SA_San_Juan.ods"
df_San_Juan=read_ods(path)
places=df_San_Juan["Location"].tolist()

path= "Tableau_SA_San_Jose.ods"
df_San_Jose=read_ods(path)
places.extend(df_San_Jose["Location"].tolist())

path= "Tableau_SA_Espada.ods"
df_Espada=read_ods(path)
places.extend(df_Espada["Location"].tolist())

path= "Tableau_SA_Concepcion.ods"
df_Concepcion=read_ods(path)
places.extend(df_Concepcion["Location"].tolist())
'''



def getCountryAndCoord(place):
    url = 'https://api.tomtom.com/search/2/geocode/'+place+'.xml?language=en-US&limit=1&key='+apiKey
    data = urllib.request.urlopen(url)
    data = xmltodict.parse(data.read().decode('utf-8'))
    
    country=data["response"]["results"]["item"]["address"]["country"]

    #lat=data["response"]["results"]["item"]["position"]["lat"]
    #lon=data["response"]["results"]["item"]["position"]["lon"]
    #print("Pays : "+country+ "\nCoord: "+lon+", "+lat)
    return {
        "country":country,
        #"lat":lat,
        #"long":lon
        }

countryCount = {}

 
for i in range (2001,len(places)-1):
    place=places[i]
    if place != "None":
        try:
            country=getCountryAndCoord(urllib.parse.quote_plus(place))["country"]
        except TypeError: 
            print("Problème : ",place)
        except HTTPError:
            print("Problème au tour ",i)
            time.sleep(10)
        except URLError:
            print("Problème au tour ",i)
            time.sleep(10)
        if country in countryCount: 
            countryCount[country] += 1
        else:
            countryCount[country] = 1
    
for country in countryCount:
    print(country, " : ",countryCount[country])
    
df_GC = pandas.DataFrame.from_dict(countryCount, orient="index", columns=["Nombre de visiteurs"])
print(df_GC)

df_GC.to_csv(path_or_buf="DF_GC3.csv")
    
print("--- %s seconds ---" % (time.time() - start_time))






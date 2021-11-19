import matplotlib.pyplot as plt, mpld3
import pandas as pd

#Grand Canyon
df_GC = pd.read_csv("datas/data_grand_canyon.csv", sep=";")
df_GC.drop(df_GC.columns[len(df_GC.columns)-1], axis=1, inplace=True)
df_GC.drop(df_GC.columns[len(df_GC.columns)-1], axis=1, inplace=True)

df_2018 = df_GC[df_GC["Date"].str.contains('18')]
df_2019 = df_GC[df_GC["Date"].str.contains('19')]
df_2020 = df_GC[df_GC["Date"].str.contains('20')]
df_2021 = df_GC[df_GC["Date"].str.contains('21')]

df_GC_mean = pd.read_csv("datas/mean_grand_canyon.csv", sep=";")

#San Antonio
df_SA = pd.read_csv("datas/data_san_antonio.csv", sep=";")
#df_SA.drop(df_SA.columns[len(df_GC.columns)-1], axis=1, inplace=True)
#df_SA.drop(df_SA.columns[len(df_GC.columns)-1], axis=1, inplace=True)

df_2018 = df_SA[df_GC["Date"].str.contains('18')]
df_2019 = df_SA[df_GC["Date"].str.contains('19')]
df_2020 = df_SA[df_GC["Date"].str.contains('20')]
df_2021 = df_SA[df_GC["Date"].str.contains('21')]

df_SA_mean = pd.read_csv("datas/mean_san_antonio.csv", sep=";")

#====================================================================#

xValues = ['jan', 'fév', 'mars', 'avr','mai','juin','juil','août','sep','oct','nov','déc'] 

#subplots
t = df_SA_mean["Date"]
data1 = df_SA_mean["Pluie"]
data2 = df_SA_mean["nb_visiteurs"]


fig, ax1 = plt.subplots()

color = 'cornflowerblue'
ax1.set_ylabel("Précipitation (mm)", color=color)
ax1.bar(t, data1, color=color)
ax1.set_ylim([0.0, 11])
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'black'
ax2.set_ylabel("Nombre de visiteurs", color=color)
ax2.plot(t, data2, color=color)
ax2.set_ylim([0, 100])
ax2.tick_params(axis='y', labelcolor=color)
plt.xticks([r for r in range(len(data1))],xValues)

fig.tight_layout()
plt.savefig('missions_moyenne_pluie.png')


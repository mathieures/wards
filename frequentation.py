import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from notes import months_names, notation_months
import mpld3

# On transforme le plot en html interactif
# source : https://www.freecodecamp.org/news/how-to-embed-interactive-python-visualizations-on-your-website-with-python-and-matplotlib
def fig_to_html(fig, nom_fichier_html):
    html_str = mpld3.fig_to_html(fig)
    html_file = open(nom_fichier_html, "w+")
    html_file.write(html_str)
    html_file.close()

def months():
    return ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "aoüt", "sept", "oct", "nov", "déc"]


def df_split_by_year(df):
    df2018 = df.iloc[0:12]
    df2018["Date"] = df2018["Date"].map(lambda x: months_names(x))
    df2019 = df.iloc[12:24]
    df2019["Date"] = df2019["Date"].map(lambda x: months_names(x))
    df2020 = df.iloc[24:36]
    df2020["Date"] = df2020["Date"].map(lambda x: months_names(x))
    df2021 = df.iloc[36:45]
    df2021["Date"] = df2021["Date"].map(lambda x: months_names(x))
    df2021.loc[46] = ["oct", 0, 0, 0, 0]
    df2021.loc[47] = ["nov", 0, 0, 0, 0]
    df2021.loc[48] = ["déc", 0, 0, 0, 0]
    df2019.reset_index(drop=True, inplace=True)
    df2020.reset_index(drop=True, inplace=True)
    df2021.reset_index(drop=True, inplace=True)
    return [df2018, df2019, df2020, df2021]


def df_barplot_annee(df1,df2,df3,df4, year, site):
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(1200*px, 500*px))
    line1 = df1["nb_visiteurs"]
    line2 = df2["nb_visiteurs"]
    line3 = df3["nb_visiteurs"]
    line4 = df4["nb_visiteurs"]
    plt.plot(months(), line1, "o-", color="r", label="2018")
    plt.plot(months(), line2, "o-", color="g", label="2019")
    plt.plot(months(), line3, "o-", color="b", label="2020")
    plt.plot(months(), line4, "o-", color="y", label="2021")
    plt.locator_params(axis="y", nbins=15)
    plt.ylabel("Visiteurs")
    plt.grid()
    plt.legend()
    name_save = "templates/frequentation/" + site + "/" + str(year) + ".html"
    fig_to_html(fig,name_save)


def df_barplots(dfs, years, column, site, label):
    colors = {"2018":"r",
              "2019":"g",
              "2020":"b",
              "2021":"y"}
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(1200*px, 500*px))
    for i in range(len(dfs)):
        df = dfs[i]
        line = df[column]
        plt.plot(line, "o-", color=colors[years[i]], label=years[i])
        plt.gca().get_xaxis().set_ticklabels(months())
        if site == "gc":
            plt.ylim(ymax=6000, ymin=0)
        else:
            plt.ylim(ymax=100, ymin=0)

    plt.locator_params(axis="y", nbins=15)
    plt.ylabel(label)
    plt.grid()
    plt.legend()

    name_save = "templates/frequentation/" + site + "/" + "_".join(years) + ".html"
    fig_to_html(fig,name_save)


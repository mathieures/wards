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
    df2018.loc[:, "Date"] = df2018["Date"].map(lambda x: months_names(x))
    df2019 = df.iloc[12:24]
    df2019.loc[:, "Date"] = df2019["Date"].map(lambda x: months_names(x))
    df2020 = df.iloc[24:36]
    df2020.loc[:, "Date"] = df2020["Date"].map(lambda x: months_names(x))
    df2021 = df.iloc[36:45]
    df2021.loc[:, "Date"] = df2021["Date"].map(lambda x: months_names(x))
    df2021.loc[46] = ["oct", 0, 0, 0, 0]
    df2021.loc[47] = ["nov", 0, 0, 0, 0]
    df2021.loc[48] = ["déc", 0, 0, 0, 0]
    df2019.reset_index(drop=True, inplace=True)
    df2020.reset_index(drop=True, inplace=True)
    df2021.reset_index(drop=True, inplace=True)
    return [df2018, df2019, df2020, df2021]


def df_barplots(dfs, years, column, site, label):
    colors = {"2018":"crimson",
              "2019":"cornflowerblue",
              "2020":"limegreen",
              "2021":"yellow"}
    """
    px = 1 / plt.rcParams['figure.dpi']
    fig = plt.figure(figsize=(850*px, 500*px))
    for i in range(len(dfs)):
        df = dfs[i]
        line = df[column]
        plt.plot(line, "o-", color=colors[years[i]], label=years[i])
        plt.fill_between(months(),line,color=colors[years[i]], alpha=0.3)

    plt.gca().get_xaxis().set_ticklabels(months())
    if site == "gc":
        plt.ylim(ymax=6000, ymin=0)
    else:
        plt.ylim(ymax=80, ymin=0)

    plt.locator_params(axis="y", nbins=15)
    plt.ylabel(label)
    plt.xlabel("Mois")
    #plt.grid()
    plt.legend(frameon=False, loc='upper right', ncol=4)

    name_save = "templates/frequentation/" + site + "/" + "_".join(years) + ".html"
    fig_to_html(fig,name_save)
    """



    px = 1 / plt.rcParams['figure.dpi']
    plt.figure(figsize=(860*px, 500*px))
    #barWidth = 0.2
    barWidth = 0.8 / len(dfs)
    for i in range(len(dfs)):
        df = dfs[i]
        line = df[column]
        r1 = np.arange(len(line))
        r1 = [x + barWidth*(i+1) - barWidth*(len(dfs)/2) for x in r1]
        plt.bar(r1, line, width=barWidth, edgecolor='black', capsize=7, color=colors[years[i]], label=years[i])
        plt.xticks([r + barWidth / 2 for r in range(len(line))], notation_months())
    if site == "gc":
        plt.ylim(ymax=6000, ymin=0)
    else:
        plt.ylim(ymax=80, ymin=0)
    plt.ylabel(label)
    #plt.xlabel("Mois")

    if len(years) == 1 :
        plt.title("Nombre de visiteurs (par mois) durant l'année : " + years[0])
    else:
        plt.title("Nombre de visiteurs (par mois) durant les années : " + ",".join(years))
    # plt.grid()
    plt.legend(frameon=False, loc='upper right', ncol=4)

    #name_save = "templates/frequentation/" + site + "/" + "_".join(years) + ".html"
    #fig_to_html(fig, name_save)
    name_save = "static/graphics/frequentation/" + site + "/" + "_".join(years) + ".png"
    plt.savefig(name_save)


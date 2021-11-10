import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from notes import months_names, notation_months

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


def df_barplot_annee(df, year, site):
    title = "Année " + str(year)

    bar = df["Temp"]
    bar2 = df["nb_visiteurs"]
    r1 = np.arange(len(bar))
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax1 = plt.subplots(figsize=(800 * px, 340 * px))
    ax2 = ax1.twinx()
    ax1.bar(r1, bar, width=0.6, color='orange')
    ax2.plot(bar2, color='g')
    ax2.set_ylabel('Nb visiteurs', color='g')
    ax1.set_ylabel('Température', color='orange')
    ax1.set_ylim(ymin=-2, ymax=35)

    if site == "sa":
        ax2.set_ylim(ymin=0, ymax=100)
    else:
        ax2.set_ylim(ymin=0, ymax=6000)

    ax1.axhline(y=0, color='k')
    plt.xticks([r for r in range(len(bar))], notation_months())
    plt.title(title)
    name_save = "static/graphics/temperature/" + site + "/" + str(year) + ".png"
    plt.savefig(name_save)

def barplot_moy_all(df, site):

    bar = df["Temp"]
    bar2 = df["nb_visiteurs"]
    r1 = np.arange(len(bar))
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax1 = plt.subplots(figsize=(800 * px, 340 * px))
    ax2 = ax1.twinx()
    ax1.bar(r1, bar, width=0.6, color='orange')
    ax2.plot(bar2, color='g')
    ax2.set_ylabel('Nb visiteurs', color='g')
    ax1.set_ylabel('Température', color='orange')
    ax1.set_ylim(ymin=-2, ymax=35)

    if site == "sa":
        ax2.set_ylim(ymin=0, ymax=100)
    else:
        ax2.set_ylim(ymin=0, ymax=6000)

    ax1.axhline(y=0, color='k')
    plt.xticks([r for r in range(len(bar))], notation_months())

    name_save = "static/graphics/temperature/" + site + "/" + "all.png"
    plt.savefig(name_save)

def barplot_all(list, site):
        begin = 2018
        for i in range(len(list)):
            df = list[i]
            df_barplot_annee(df, begin + i, site)

def mean_all(dfs):
    months = notation_months()
    df = pd.DataFrame(columns=["Date", "Temp", "nb_visiteurs"])
    for i in range(len(months)):
        sum_mean_temp = 0
        sum_mean_visit = 0
        for dataframe in dfs:
            sum_mean_temp = sum_mean_temp + dataframe["Temp"].loc[i]
            sum_mean_visit = sum_mean_visit + dataframe["nb_visiteurs"].loc[i]
        if i > 8:
            mean_of_means = sum_mean_temp / (len(dfs)-1)
            mean_of_means_visit = sum_mean_visit / (len(dfs)-1)

        else:
            mean_of_means = sum_mean_temp / len(dfs)
            mean_of_means_visit = sum_mean_visit / len(dfs)
        df = df.append({"Date": months[i], "Temp": round(mean_of_means, 2), "nb_visiteurs": round(mean_of_means_visit, 2)}, ignore_index=True)
    return df


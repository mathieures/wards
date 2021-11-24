import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from notes import months_names, notation_months
from scipy.stats import pearsonr

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
    bar = df["Pluie"]
    bar2 = df["nb_visiteurs"]
    r1 = np.arange(len(bar))
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax2 = plt.subplots(figsize=(860 * px, 340 * px))
    ax1 = ax2.twinx()
    ax2.bar(r1, bar2, width=0.6, color='Gainsboro')
    ax1.plot(bar, color='DeepSkyBlue')
    ax2.set_ylabel('Nombre de visiteurs', color='Gray')
    ax1.set_ylabel('Précipitation (en mm)', color='DeepSkyBlue')
    ax1.set_ylim(ymin=0, ymax=12)

    if site == "sa":
        ax2.set_ylim(ymin=0, ymax=80)
    else:
        ax2.set_ylim(ymin=0, ymax=6000)

    plt.xticks([r for r in range(len(bar))], notation_months())
    # plt.title("Année " + str(year))
    plt.title("Nombre de visiteurs et température (par mois) durant l'année : " + str(year))
    name_save = "static/graphics/precipitation/" + site + "/" + str(year) + ".png"
    plt.savefig(name_save)

def barplot_moy_all(df, site):
    bar = df["Pluie"]
    bar2 = df["nb_visiteurs"]
    r1 = np.arange(len(bar))
    px = 1 / plt.rcParams['figure.dpi']
    fig, ax2 = plt.subplots(figsize=(860 * px, 340 * px))
    ax1 = ax2.twinx()
    ax2.bar(r1, bar2, width=0.6, color='Gainsboro')
    ax1.plot(bar, color='DeepSkyBlue')
    ax2.set_ylabel('Nombre de visiteurs', color='Gray')
    ax1.set_ylabel('Précipitation (en mm)', color='DeepSkyBlue')
    ax1.set_ylim(ymin=0, ymax=12)

    if site == "sa":
        ax2.set_ylim(ymin=0, ymax=80)
    else:
        ax2.set_ylim(ymin=0, ymax=6000)
    plt.xticks([r for r in range(len(bar))], notation_months())

    plt.title("Nombre de visiteurs moyen et température moyenne (par mois)\ndurant les années : 2018, 2019, 2020, 2021")
    name_save = "static/graphics/precipitation/" + site + "/" + "all.png"
    plt.savefig(name_save)

def barplot_all(list, site):
        begin = 2018
        for i in range(len(list)):
            df = list[i]
            df_barplot_annee(df, begin + i, site)

def mean_all(dfs):
    months = notation_months()
    df = pd.DataFrame(columns=["Date", "Pluie", "nb_visiteurs"])
    for i in range(len(months)):
        sum_mean_prec = 0
        sum_mean_visit = 0
        for dataframe in dfs:
            sum_mean_prec = sum_mean_prec + dataframe["Pluie"].loc[i]
            sum_mean_visit = sum_mean_visit + dataframe["nb_visiteurs"].loc[i]
        if i > 8:
            mean_of_means = sum_mean_prec / (len(dfs)-1)
            mean_of_means_visit = sum_mean_visit / (len(dfs)-1)

        else:
            mean_of_means = sum_mean_prec / len(dfs)
            mean_of_means_visit = sum_mean_visit / len(dfs)
        df = df.append({"Date": months[i], "Pluie": round(mean_of_means, 2), "nb_visiteurs": round(mean_of_means_visit, 2)}, ignore_index=True)
    return df

def test_correlation(colonne1, colonne2):
    pearson_coeff,p_value = pearsonr(colonne1,colonne2)
    return '{:.3f}'.format(pearson_coeff),'{:.3f}'.format(p_value)

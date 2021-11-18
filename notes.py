# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def months_names(string):
    paire = string.split("-")
    return paire[0]

def notation_months():
    return ["janv", "févr", "mars", "avr", "mai", "juin", "juil", "août", "sept", "oct", "nov", "déc"]

def df_split_by_year(df):
    df['note_moyenne'] = df['note_moyenne'].fillna(0)
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
    df2018.reset_index(drop=True, inplace=True) # en vrai pas besoin ?
    df2019.reset_index(drop=True, inplace=True)
    df2020.reset_index(drop=True, inplace=True)
    df2021.reset_index(drop=True, inplace=True)
    return [df2018, df2019, df2020, df2021]

def barplot_one_year(df1, df2, year):
    px = 1 / plt.rcParams['figure.dpi']
    plt.subplots(figsize=(1250 * px, 500 * px))
    barWidth = 0.4
    title = "Année " + str(year)
    bars1 = df1["note_moyenne"]
    bars2 = df2["note_moyenne"]
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    plt.bar(r1, bars1, width=barWidth, color='mediumslateblue', edgecolor='white', capsize=7, label='Grand Canyon')
    plt.bar(r2, bars2, width=barWidth, color='gold', edgecolor='white', capsize=7, label='Missions')
    plt.xticks([r + barWidth / 2 for r in range(len(bars1))], notation_months())
    plt.ylabel('Note')
    #plt.legend(loc='upper center', bbox_to_anchor=(1.18, 1), ncol=1, fancybox=True, shadow=True)
    plt.title(title)
    name_save = "static/graphics/note/" + str(year) + ".png"
    plt.savefig(name_save)

def barplot_all_years(list1, list2):
    if len(list1) != len(list2):
        return
    else:
        begin = 2018
        for i in range(len(list1)):
            df1 = list1[i]
            df2 = list2[i]
            barplot_one_year(df1, df2, begin + i)

def barplot_mean_years(df1, df2):
    px = 1 / plt.rcParams['figure.dpi']
    plt.subplots(figsize=(1250 * px, 500 * px))
    barWidth = 0.4
    title = "De 2018 à 2021"
    bars1 = df1["note_moyenne"]
    bars2 = df2["note_moyenne"]
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    plt.bar(r1, bars1, width=barWidth, color='mediumslateblue', edgecolor='white', capsize=7, label='Grand Canyon')
    plt.bar(r2, bars2, width=barWidth, color='gold', edgecolor='white', capsize=7, label='Missions')
    plt.xticks([r + barWidth / 2 for r in range(len(bars1))], notation_months())
    plt.ylabel('Note moyenne')
    #plt.legend(loc='upper center', bbox_to_anchor=(1.23, 1), ncol=1, fancybox=True, shadow=True)
    plt.title(title)
    plt.savefig("static/graphics/note/all.png")

def mean_notes(dfs):
    months = notation_months()
    df = pd.DataFrame(columns=["Date", "note_moyenne"])
    for i in range(len(notation_months())):
        sum_mean_notes = 0
        nb = 0
        j = i
        for dataframe in dfs:
            visit = dataframe["nb_visiteurs"].loc[j]
            mean_note = dataframe["note_moyenne"].loc[i]
            if visit > 0 and mean_note > 0:
                # print(f"{months[i]} -> {dataframe['note_moyenne'][i]}")
                sum_mean_notes = sum_mean_notes + mean_note
                nb = nb + 1
        if nb > 0:
            mean_of_means = sum_mean_notes / nb
            # print(f"Sum = {sum_mean_notes}\tNb = {nb}\tMean = {mean_of_means}")
            df = df.append({"Date": months[i], "note_moyenne": round(mean_of_means, 2)}, ignore_index=True)
    return df

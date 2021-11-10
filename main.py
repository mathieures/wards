from flask import Flask, render_template
import pandas as pd
import notes, temperature

# ----- Lancement de l'app ----- #
app = Flask(__name__)

# Test d'ouverture des fichiers
def read_file(filename):
    try:
        return pd.read_csv(filename, sep=";", header=0).iloc[:, :5]
    except:
        print("Erreur lors de la lecture du fichier : " + filename)


# Chargement des fichiers en dataframe
df_gc = read_file('datas/data_grand_canyon.csv')
df_sa = read_file('datas/data_san_antonio.csv')
df_pays_gc = pd.read_csv('datas/pays_origine_GC.csv')
df_pays_sa = pd.read_csv('datas/pays_origine_SA.csv')

# Partie des notes
dfs_gc = notes.df_split_by_year(df_gc)
dfs_sa = notes.df_split_by_year(df_sa)
notes.barplot_all_years(dfs_gc, dfs_sa)
df_mean_gc = notes.mean_notes(dfs_gc)
df_mean_sa = notes.mean_notes(dfs_sa)
notes.barplot_mean_years(df_mean_gc, df_mean_sa)

# Partie météo
# Température
dfs_temp_gc = temperature.df_split_by_year(df_gc)
dfs_temp_sa = temperature.df_split_by_year(df_sa)
temperature.barplot_all(dfs_temp_gc,"gc")
temperature.barplot_all(dfs_temp_sa,"sa")

df_temp_mean_gc = temperature.mean_all(dfs_temp_gc)
df_temp_mean_sa = temperature.mean_all(dfs_temp_sa)
temperature.barplot_moy_all(df_temp_mean_gc, "gc")
temperature.barplot_moy_all(df_temp_mean_sa, "sa")



# @Routes
# Index
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Page des moyennes des notes par mois des années 2018 à 2021
@app.route('/note')
def note():
    mean_gc_2018 = str(round(sum(dfs_gc[0]["note_moyenne"]) / len(dfs_gc[0]), 2))
    mean_sa_2018 = str(round(sum(dfs_sa[0]["note_moyenne"]) / len(dfs_sa[0]), 2))
    mean_gc_2019 = str(round(sum(dfs_gc[1]["note_moyenne"]) / len(dfs_gc[1]), 2))
    mean_sa_2019 = str(round(sum(dfs_sa[1]["note_moyenne"]) / len(dfs_sa[1]), 2))
    mean_gc_2020 = str(round(sum(dfs_gc[2]["note_moyenne"]) / len(dfs_gc[2]), 2))
    mean_sa_2020 = str(round(sum(dfs_sa[2]["note_moyenne"]) / (len(dfs_sa[2])-3), 2))
    mean_gc_2021 = str(round(sum(dfs_gc[3]["note_moyenne"]) / (len(dfs_gc[3])-3), 2))
    mean_sa_2021 = str(round(sum(dfs_sa[3]["note_moyenne"]) / (len(dfs_sa[3])-3), 2))
    mean_gc_all = str(round(sum(df_mean_gc["note_moyenne"]) / len(df_mean_gc), 2))
    mean_sa_all = str(round(sum(df_mean_sa["note_moyenne"]) / len(df_mean_sa), 2))
    return render_template('note.html',
                           mean_gc_2018=mean_gc_2018,
                           mean_sa_2018=mean_sa_2018,
                           mean_gc_2019=mean_gc_2019,
                           mean_sa_2019=mean_sa_2019,
                           mean_gc_2020=mean_gc_2020,
                           mean_sa_2020=mean_sa_2020,
                           mean_gc_2021=mean_gc_2021,
                           mean_sa_2021=mean_sa_2021,
                           mean_gc_all=mean_gc_all,
                           mean_sa_all=mean_sa_all
                           )

# Page à propos
@app.route('/about')
def about():
    return render_template('about.html')




# Page météo (avec températures et précipitations)
@app.route('/meteo')
def meteo():

    # Température

    return render_template('meteo.html')


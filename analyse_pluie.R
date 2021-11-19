data_gc <- read.csv("datas/data_grand_canyon.csv", sep=";")
data_gc

shapiro.test(data_gc$nb_visiteurs)
shapiro.test(data_gc$Pluie)
cor.test(data_gc$Pluie, data_gc$nb_visiteurs, method="pearson")

data_sa <- read.csv("datas/data_san_antonio.csv", sep=";")
data_sa
cor.test(data_sa$nb_visiteurs,data_sa$Pluie, method="pearson")

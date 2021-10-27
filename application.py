from Script_meteo import Combinaison
from Script_instagram import donnees_insta_par_lieu
from Script_instagram import nb_visiteurs_par_mois


def main():
    Combinaison.main() # Lance le script de la meteo
    donnees_insta_par_lieu.main() # Lance le script instagram
    nb_visiteurs_par_mois.main()


if __name__ == "__main__":
    main()
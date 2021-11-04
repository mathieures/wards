from datetime import date, datetime
import csv
from time import sleep
from random import randint
import os.path
from sys import exit as sysexit

import json
import codecs
import os.path
import logging
import argparse
try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        ClientThrottledError,
        __version__ as client_version)
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        ClientThrottledError,
        __version__ as client_version)


def to_json(python_object):
    if isinstance(python_object, bytes):
        return {"__class__": "bytes",
                "__value__": codecs.encode(python_object, "base64").decode()}
    raise TypeError(repr(python_object) + " is not JSON serializable")


def from_json(json_object):
    if "__class__" in json_object and json_object["__class__"] == "bytes":
        return codecs.decode(json_object["__value__"].encode(), "base64")
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, "w") as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print("SAVED: {0!s}".format(new_settings_file))

### Fonctions personnalisees ###
def lieux_avec_nom(api, nom: str, count: int = 0):
    """
    Retourne une liste d'objets (dicos) contenant
    des informations concernant des localisations
    """
    if count > 0:
        lieux = api.location_search(0, 0, query=nom)["venues"][:count+1] # longitude, latitude, query
    else:
        lieux = api.location_search(0, 0, query=nom)["venues"] # longitude, latitude, query
    return lieux

def meilleur_lieu_avec_nom(api, nom: str):
    """Retourne le premier résultat : celui qui correspond le plus à la requête"""
    return lieux_avec_nom(api, nom, count=1)[0]

def nettoyer_resultats(results):
    """
    Retourne un tuple contenant les noms d'utilisateur et les dates de
    publications obtenus à partir des résultats passés en paramètre
    À modifier si on veut récupérer d'autres informations
    """
    donnees = []

    sections = results["sections"] # liste d'objets (dicos) { "layout_type": … }
    for layout in sections:
        # layout : liste d'objets (dicos) { "media": … } (c'est une ligne de 3 medias dans l'application)
        # layout["layout_content"]["medias"] : liste d'objets (dicos) { "media": … }
        for objet_media in layout["layout_content"]["medias"]:
            # objet_media : dico { "media": … }
            media = objet_media["media"] # dico { "taken_at": …, "…": …}

            # Nom d'utilisateur
            nom_utilisateur = media["user"]["username"]

            # Date de publication
            date_publication = date.fromtimestamp(media["taken_at"])

            donnees.append((nom_utilisateur, date_publication))

            # # Decription
            # if media["caption"] is not None:
            #     description = media["caption"]["text"]

    return donnees

def print_medias(results):
    """
    Affiche la date de prise de vue,
    la description et l'url des medias
    de la page de résultats passée en paramètre
    """
    sections = results["sections"] # liste d'objets (dicos) { "layout_type": … }
    for layout in sections:
        # layout : liste d'objets (dicos) { "media": … } (c'est une ligne de 3 medias dans l'application)
        # layout["layout_content"]["medias"] : liste d'objets (dicos) { "media": … }
        for objet_media in layout["layout_content"]["medias"]:
            # objet_media : dico { "media": … }
            media = objet_media["media"] # dico { "taken_at": …, "…": …}
            
            # Nom d'utilisateur
            nom_utilisateur = media["user"]["username"]
            print(f"{nom_utilisateur=}")
            
            # Date de prise de vue
            date_publication = date.fromtimestamp(media["taken_at"])
            print(f"{date_publication=}")
            
            # Decription
            if media["caption"] is not None:
                description = media["caption"]["text"]
                print(f"{description=}")
            else:
                print("[pas de description]")
            
            # Photos/Videos
            # Si c'est un carousel
            if "carousel_media" in media:
                print("[c'est un carousel]")
                carousel_media = media["carousel_media"] # liste d'objets (dicos) { "id": …, "media_type": …, …}
            else:
                carousel_media = [media]
                print("[[qu'un seul element]]")
            for el in carousel_media:
                if len(el["image_versions2"]["candidates"]) > 1:
                    # Si on peut prendre la version compressee
                    photo = el["image_versions2"]["candidates"][1] # le 2e el est moins lourd
                else:
                    photo = el["image_versions2"]["candidates"][0] 
                url_photo = photo["url"]
                print(f"{url_photo=}")

            print()
            print("    #### media suivant ####")
        print("  #### layout suivant ####")
    print("################# PAGE TERMINÉE #################")

def obtenir_precedent_next_max_id(nom_fichier_next_max_id):
    ancien_next_max_id = ""
    # On essaie d'acceder au fichier contenant les next_max_id precedents
    try:
        with open(nom_fichier_next_max_id, "r") as max_id_file:
            lignes = max_id_file.readlines()
            if len(lignes):
                ancien_next_max_id = lignes[-1].rstrip()[12:].strip("'")
    except FileNotFoundError:
        # On cree le fichier s'il n'existe pas
        print(f"[Avertissement] Le fichier {nom_fichier_next_max_id} n'existait pas")
        with open(nom_fichier_next_max_id, "w") as max_id_file:
            pass
    finally:
        return ancien_next_max_id

def ecrire_next_max_id_dans_txt(next_max_id, nom_fichier_next_max_id):
    with open(nom_fichier_next_max_id, "a") as max_id_file:
        max_id_file.write(f"{next_max_id=}\n")

def ecrire_donnees_dans_csv(donnees_a_ecrire, nom_fichier, noms_colonnes):
    noms_colonnes = ["nom_utilisateur", "date_publication"] # A modifier si on veut d'autres informations
    if os.path.exists(nom_fichier):
        mode = "a"
    else:
        mode = "w"
    print(f"Ecriture dans le fichier ({mode=})")
    with open(nom_fichier, mode, newline="") as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=noms_colonnes)
        if mode == "w":
            writer.writeheader()
        for nuplet in donnees_a_ecrire:
            writer.writerow({noms_colonnes[i]: nuplet[i] for i in range(len(noms_colonnes))})

def main():
    logging.basicConfig()
    logger = logging.getLogger("instagram_private_api")
    logger.setLevel(logging.WARNING)

    # Example command:
    # python examples/savesettings_logincallback.py -u "yyy" -p "zzz" -settings "test_credentials.json"
    parser = argparse.ArgumentParser(description="Récolte de données instagram sur un lieu décrit")
    parser.add_argument("-settings", "--settings", dest="settings_file_path", type=str, required=True)
    parser.add_argument("-data", "--data", dest="data_file_path", type=str, required=True)
    parser.add_argument("-query", "--query", dest="location_query", type=str, required=True)
    parser.add_argument("-pages", "--pages", dest="nb_pages_max", type=int, default=2)
    # parser.add_argument("-u", "--username", dest="username", type=str, required=True)
    # parser.add_argument("-p", "--password", dest="password", type=str, required=True)
    parser.add_argument("-debug", "--debug", action="store_true")

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    print("Client version: {0!s}".format(client_version))

    device_id = None
    try:
        settings_file = args.settings_file_path
        if not os.path.isfile(settings_file):
            # settings file does not exist
            print("Unable to find file: {0!s}".format(settings_file))

            # login new
            api = Client(
                # args.username, args.password,
                "projetintegre2021", "J'aime Thomas%69",
                on_login=lambda x: onlogin_callback(x, args.settings_file_path))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            print("Reusing settings: {0!s}".format(settings_file))

            device_id = cached_settings.get("device_id")
            # reuse auth settings
            api = Client(
                # args.username, args.password,
                "projetintegre2021", "J'aime Thomas%69",
                settings=cached_settings)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print("ClientCookieExpiredError/ClientLoginRequiredError: {0!s}".format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        api = Client(
            # args.username, args.password,
            "projetintegre2021", "J'aime Thomas%69",
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, args.settings_file_path))

    except ClientLoginError as e:
        print("ClientLoginError {0!s}".format(e))
        exit(9)
    except ClientError as e:
        print("ClientError {0!s} (Code: {1:d}, Response: {2!s})".format(e.msg, e.code, e.error_response))
        exit(9)
    except Exception as e:
        print("Unexpected Exception: {0!s}".format(e))
        exit(99)

    # Montre la date d'expiration du cookie de connexion
    date_expiration_cookie = datetime.fromtimestamp(api.cookie_jar.auth_expires).strftime('le %d/%m/%Y, à %H:%M:%S')
    print("Date d'expiration du cookie de connexion :", date_expiration_cookie)

    # Recherche de la localisation
    resultat_recherche_lieu = meilleur_lieu_avec_nom(api, args.location_query)
    # print("resultat_recherche_lieu :", resultat_recherche_lieu)
    id_lieu = resultat_recherche_lieu["external_id"] # Un entier (115814651804946 pour South Rim of the Grand Canyon)
    print(f"{id_lieu=}")

    # Pagination
    nb_pages = 0
    rank_token = api.generate_uuid() # Necessaire pour la pagination

    # Collecte des donnees
    # On recupere la ou on s'etait arrete pour ce lieu
    nom_fichier_next_max_id = str(id_lieu) + ".txt"
    ancien_next_max_id = obtenir_precedent_next_max_id(nom_fichier_next_max_id)
    print(f"{ancien_next_max_id=}")

    # On retente le premier essai jusqu'a ce que ca fonctionne (sinon on n'a rien)
    premier_essai_echoue = True
    while premier_essai_echoue:
        try:
            # results = api.location_section(id_lieu, rank_token, tab="recent", max_id=next_max_id)
            if ancien_next_max_id:
                # Si on avait un next_max_id
                results = api.location_section(id_lieu, rank_token, tab="recent", max_id=ancien_next_max_id)
            else:
                # Sinon
                results = api.location_section(id_lieu, rank_token, tab="recent")
        except Exception as e:
            print(f"[Erreur dès la première requête] : {e}, à {datetime.now()} ({nb_pages=})")
            # Pas besoin d'ecrire de donnees, on n'en a aucune
            attente = randint(60, 600) # On attend entre 1min et 10min
            print(f"[Avertissement] On réessaiera dans : {attente}s")
            sleep(attente)
        else:
            premier_essai_echoue = False

    # Nettoyage des donnees a ecrire
    donnees_recoltees = nettoyer_resultats(results) # liste de tuples (nom_utilisateur, date_publication)

    # On ecrit le next_max_id dans un fichier pour reprendre au meme endroit la prochaine fois
    next_max_id = results.get("next_max_id")
    print(f"{next_max_id=}")
    ecrire_next_max_id_dans_txt(next_max_id, nom_fichier_next_max_id)

    # Ecriture des donnees dans un fichier
    noms_colonnes = ["nom_utilisateur", "date_publication"] # A modifier si on veut d'autres informations
    nom_fichier_csv = args.data_file_path
    ecrire_donnees_dans_csv(donnees_recoltees, nom_fichier_csv, noms_colonnes)

    nb_pages += 1
    sleep(randint(1, 9))

    while (next_max_id is not None) and (nb_pages < args.nb_pages_max):
        try:
            results = api.location_section(id_lieu, rank_token, tab="recent", max_id=next_max_id)
        except Exception as e:
            # On considere toutes les exceptions, pour la print a coup sur
            print(f"[Erreur] : {e}, à {datetime.now()} ({nb_pages=})")
            break
        else:
            # donnees_recoltees.extend(nettoyer_resultats(results))
            donnees_recoltees = nettoyer_resultats(results)

            # On ecrit le next_max_id dans un fichier pour reprendre au meme endroit la prochaine fois
            next_max_id = results.get("next_max_id")
            print(f"{next_max_id=}")
            ecrire_next_max_id_dans_txt(next_max_id, nom_fichier_next_max_id)

            # On ecrit a chaque tour, comme ca on est surs d'avoir les donnees meme en cas d'erreur
            ecrire_donnees_dans_csv(donnees_recoltees, nom_fichier_csv, noms_colonnes)
            
            nb_pages += 1
            sleep(randint(1, 9))

    print("[Info] Fin de la collecte")

if __name__ == "__main__":
    main()
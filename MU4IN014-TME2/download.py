# Fichier download pour les questions 1 des exercices 2, 3 et 5

from requests import *
from bs4 import BeautifulSoup as bs
from pathlib import *

def stream_download(source_url, dest):
    print('Downloading at', source_url)
    r = get(source_url, stream=True)
    dest = Path(dest)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

# Exercice 2, q1
stream_download("https://www.w3schools.com/xml/cd_catalog.xml", "cd_catalog.xml")

# Exercice 2, q1
stream_download("https://opendata.paris.fr/explore/dataset/lieux-de-tournage-a-paris/download/?format=json&timezone=Europe/Berlin&lang=fr", "lieux-de-tournage-a-paris.json")

# Exercice 2, q1
stream_download("https://opendata.paris.fr/explore/dataset/les-titres-les-plus-pretes/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B", "les-titres-les-plus-pretes.csv")
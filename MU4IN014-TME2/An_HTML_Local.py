# Exercice 4

from requests import *
from bs4 import BeautifulSoup as bs
from re import *
from urllib.parse import unquote
from pathlib import *

# Les fonctions stream_download et country_download sont utilisées pour télécharger le contenu HTML de wikipédia dans le dossier dest_file
dest_file = 'links'

def stream_download(source_url, dest):
    print('Downloading at', source_url)
    r = get(source_url, stream=True)
    dest = Path(dest)
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

def country_download(link):
    """
    Fonction qui enregistre le contenu html de wikipédia dans un fichier.
    """
    r = get(link)
    soup = bs(r.text, features='lxml')
    
    list_country = get_country()
    list_infos = []
    if len(list_country):
        table = soup.find('table', {'class':'wikitable sortable'})
        for data in table.find_all('tr'):
            try:
                for c in list_country:
                    if c in data.text:
                        try:
                            value = (data('td')[-1].text).strip('\n').replace(',','.') #Récupère la valeur correspondant à la densité
                            if u'\xa0' in value: #Remplace les espaces dans la valeur
                                value = value.replace(u'\xa0', u'')
                            if not any(c in country for country in list_infos): #Vérifie si le pays est présent dans la liste
                                for link in data('a'):
                                    l_name = unquote(link.get('href'), errors='strict').replace('_', ' ')
                                    c_name = sub(r" \([^)]*\)", '', c) #Retire les parenthèses qui suivent le nom d'un pays, par exemple : Grenade (pays) => Grenade
                                    if c_name in l_name and 'Flag' not in l_name and c_name:
                                        stream_download('https://fr.wikipedia.org'+l_name, dest_file+l_name)
                                        list_infos.append((float(value), c_name))
                                    elif 'Guernesey' in l_name and 'Flag' not in l_name: #Cas particulier pour Guernesey
                                        if (float(value), 'Guernesey') not in list_infos:
                                            stream_download('https://fr.wikipedia.org'+l_name, dest_file+l_name)
                                            list_infos.append((float(value), 'Guernesey'))
                                    elif 'Jersey' in l_name and 'Flag' not in l_name: #Cas particulier pour Jersey
                                        if (float(value), 'Jersey') not in list_infos:
                                            stream_download('https://fr.wikipedia.org'+l_name, dest_file+l_name)
                                            list_infos.append((float(value), 'Jersey'))
                        except Exception as exc:
                            print("Conversion failed & getting data failed", exc)
            except KeyError as exc:
                print(exc)
    else:
        print("No countries available")

def get_country():
    """
    Fonction qui retourne la liste des pays de link.
    """
    try:
        f = open(dest_file+'/list_country', 'rb')
        soup = bs(f.read(), features='lxml')
        list_country = []
        table = soup.find('table', {'class':'wikitable sortable'})
        for data in table.find_all('td', {'align':'left'}):
                if data.text and 'Drapeau' not in data.text and data.text not in list_country:
                    list_country.append(sub('\[.]$', '', (data.text).strip(' \n')))
        f.close()
        return list_country
    except Exception as exc:
        print("Data not available :", exc)

def get_infos():
    """
    Fonction qui retourne le rang, la densité, la population et la superficie des pays.
    Cette fonction fait appel à get_infos_from_link pour obtenir la population et la superficie.
    """
    try:
        f = open(dest_file+'/list_country', 'rb')
        soup = bs(f.read(), features='lxml')
        
        list_country = get_country()
        list_infos = []
        if len(list_country):
            table = soup.find('table', {'class':'wikitable sortable'})
            try:
                for data in table.find_all('tr'):
                    for c in list_country:
                        if c in data.text:
                            try:
                                value = (data('td')[-1].text).strip('\n').replace(',','.') #Récupère la valeur correspondant à la densité
                                if u'\xa0' in value: #Remplace les espaces dans la valeur
                                    value = value.replace(u'\xa0', u'')
                                if not any(c in country for country in list_infos): #Vérifie si le pays est présent dans la liste
                                    for link in data('a'):
                                        l_name = unquote(link.get('href'), errors='strict').replace('_', ' ')
                                        c_name = sub(r" \([^)]*\)", '', c) #Retire les parenthèses qui suivent le nom d'un pays, par exemple : Grenade (pays) => Grenade
                                        if c_name in l_name and 'Flag' not in l_name and c_name:
                                            infos = get_infos_from_link(l_name)
                                            list_infos.append((float(value), c_name, infos[0], infos[1]))
                                        elif 'Guernesey' in l_name and 'Flag' not in l_name: #Cas particulier pour Guernesey
                                            infos = get_infos_from_link(l_name)
                                            if (float(value), 'Guernesey', infos[0], infos[1]) not in list_infos:
                                                list_infos.append((float(value), 'Guernesey', infos[0], infos[1]))
                                        elif 'Jersey' in l_name and 'Flag' not in l_name: #Cas particulier pour Jersey
                                            infos = get_infos_from_link(l_name)
                                            if (float(value), 'Jersey', infos[0], infos[1]) not in list_infos:
                                                list_infos.append((float(value), 'Jersey', infos[0], infos[1]))
                            except Exception as exc:
                                print("Conversion failed & getting data failed", exc)
            except KeyError as exc:
                print(exc)
        else:
            print("No countries available")
    except Exception as exc:
        print("Opening file failed\n", exc)
    
    # Classe les villes et créé des dictionnaires dans la liste
    rang = 0
    equal = False
    list_ranked = []
    for n in sorted(list_infos, reverse=True):
        if not equal:
            rang += 1
        if 'Guernesey' in n[1] or 'Jersey' in n[1]: #Guernesey et Jersey ont le même Rang
            if not equal:
                equal = True
            else:
                equal = False
        list_ranked.append({'Rang': rang, 'Pays':n[1], 'Densité': n[0], 'Population':n[2], 'Superficie':n[3]})
    return list_ranked

def get_infos_from_link(link):
    """
    Fonction récupère les informations sur la population et la superficie des pays.
    Elle retourne un tuple (pop,sup) :
        pop est le nombre d'habitants
        sup est la superficie en km²
    """
    try:
        print('Gathering information :', link)
        f = open(dest_file+link, 'rb')
        soup = bs(f.read(), features='lxml')
        
        pop_found = False
        sup_found = False
        pop = ''
        sup = ''
        
        table = soup.find('div')
        for data in table.select("table"):
            for value in data.find_all('tr'):
                if not pop_found and 'Population' in value.text and 'hab' in value.text:
                    if 'Ukraine' not in link:
                        pop = sub('hab.+', '', sub('\[.+', '', split('\n', (value.text).replace(u'\xa0', u''))[3])).strip(' ')
                    else:
                        pop = sub('[^\d]', '', sub('hab.+', '', sub('\[.]', '', split('\n', (value.text).replace(u'\xa0', u''))[3]))).strip(' ')
                    pop_found = True
                elif not sup_found and 'Superficie' in value.text and 'km2' in value.text and ('Superficie(km2)' not in value.text and 'Superficie (km2)' not in value.text):
                    if 'Ukraine' not in link:
                        sub_element = ['environ ', 'km.+', '\[.+', '.+ha=', ' ']
                    else:
                        sub_element = ['km.+', '\[.]', '[^\d]']
                    sup = split('\n', (value.text).replace(u'\xa0', u''))[3]
                    for s in sub_element:
                        sup = sub(s, '', sup)
                    sup = sup.replace(',','.')
                    sup_found = True
                if pop_found and sup_found:
                    break
        return (pop,sup)
    except Exception as exc:
        print(f"Infos from link not available for {link} : ", exc)

def user_request(link):
    """
    Fonction permettant à un utilisateur de récupérer les informations d'un pays s'il existe.
    """
    print('Please wait for data, It may take some time to load unfortunately:(')
    country_infos = get_infos()
    print("Country available :\n")
    for ci in country_infos:
        print(ci)
    
    while True:
        try:
            user_prompt = input("Please enter a country\n")
            if user_prompt == 'exit':
                break
            print(f'You entered {user_prompt}, checking...')
            for i in range(0,len(country_infos)):
                if country_infos[i].get('Pays') == user_prompt :
                    print('Here is what you\'re looking for !\n', country_infos[i])
                    break
                if i == len(country_infos)-1:
                    print(f'{user_prompt} not found! Retry...')
        except KeyboardInterrupt as ki:
            Print("Leaving now...")
            break
        except Exception as exc:
            print("An error occcured during user request\n", exc)

# Téléchargement à réaliser si votre dossier links est vide

stream_download("https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population", dest_file+'/list_country')
country_download("https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population")

# Question 2
list_country = get_country()

for c in list_country:
    print(c)
print("Nombre de pays:", len(list_country))

# Question 3 et 4(le résultat). La valeur de la densité proviennent de l'année 2018
list_infos = get_infos()

for i in list_infos:
    print(i)

# Question 5
user_request("https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population")
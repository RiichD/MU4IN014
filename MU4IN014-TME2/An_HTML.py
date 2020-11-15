# Exercice 4

from requests import *
from bs4 import BeautifulSoup as bs
from re import *
from urllib.parse import unquote

def get_country(link):
    """
    Fonction qui retourne la liste des pays de link.
    """
    try:
        r = get(link)
        soup = bs(r.text, features='lxml')
        
        list_country = []
        table = soup.find('table', {'class':'wikitable sortable'})
        for data in table.find_all('td', {'align':'left'}):
            if data.text and 'Drapeau' not in data.text and data.text not in list_country:
                list_country.append(sub('\[.]$', '', (data.text).strip(' \n')))
        return list_country
    except KeyError as exc:
        print("Data not available :", exc)

def get_infos(link):
    """
    Fonction qui retourne le rang, la densité, la population et la superficie des pays.
    Cette fonction fait appel à get_infos_from_link pour obtenir la population et la superficie.
    """
    try:
        r = get(link)
        soup = bs(r.text, features='lxml')
        
        list_country = get_country(link)
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
        print("Data not available :", exc)
    
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
        if 'https://fr.wikipedia.org' not in link:
            l = 'https://fr.wikipedia.org'+link
        else:
            l = link
        
        print('LIEN:', l)
        r = get(l)
        soup = bs(r.text, features='lxml')
        
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
        print(f"Information from link not available for {link} : ", exc)

def user_request(link):
    """
    Fonction permettant à un utilisateur de récupérer les informations d'un pays s'il existe.
    """
    print('Please wait for data, It may take some time to load unfortunately :(')
    country_infos = get_infos(link)
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

# Question 2
list_country = get_country("https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population")

for c in list_country:
    print(c)
print("Nombre de pays:", len(list_country))

# Question 3 et 4(le résultat). La valeur de la densité proviennent de l'année 2018
list_infos = get_infos("https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population")

for i in list_infos:
    print(i)

# Question 5
user_request("https://fr.wikipedia.org/wiki/Liste_des_pays_par_densit%C3%A9_de_population")
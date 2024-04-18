import requests
import time
import os
#html5lib
from bs4 import BeautifulSoup
import pandas as pd
h_debut = time.time()

nom_fichier = "resultats_ligue1.xlsx"
path = 'C:/Users/Ibrahima SAGNO/Documents/tuto_scraping/resultats_ligue1.xlsx'

debut = 2021
fin = 2022
urls = []

equipes_dict = {"saisons":[],
                "journée":[],
                              "equipe_dom":[],
                             "score":[],
                             "equipe_ext":[]}

while debut <= fin:
    day = 1  # Réinitialiser day à 1 à chaque itération de la boucle externe
    while day <= 38:
        saison = str(debut) + "-" + str(debut + 1)
        url = "https://www.ligue1.fr/calendrier-resultats?seasonId=" + saison + "&matchDay=" + str(day) + "&StatsActiveTab=0"
        urls.append(url)
        day += 1
    debut += 1  # Incrementer debut à l'exterieur de la boucle interne
      

#------------------------------

for url in urls:

 response = requests.get(url)
 response.encoding = response.apparent_encoding #"utf-8"

 if response.status_code == 200:
    html = response.text
    #print(html)
    f=open("ligue1.html","w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html,'html.parser')

       
# Trouver tous les éléments HTML correspondant aux équipes à domicile
    saison = soup.find("div",{"class":"CustomSelect"})
    journee = soup.find("a",class_ = lambda x: x and x.endswith('journeyItem'),href=url.replace("https://www.ligue1.fr",""))
#print(saison.text)
    equipes_domicile = soup.find_all("div", {"class": "club home"})
    equipes_exterieure = soup.find_all("div", {"class": "club away"})
    score_domicile = soup.find_all("div",class_="Calendar-clubResult result")

# Ajouter les noms des équipes à domicile dans le dictionnaire
    for i in (equipes_domicile):
        nom_equipe = i.find("span")
        if nom_equipe:
            equipe_dom = nom_equipe.text.strip()
            equipes_dict["equipe_dom"].append(equipe_dom)
            equipes_dict["saisons"].append(saison.text)
            equipes_dict["journée"].append(journee.text.strip())

#Ajouter Equipe à l'éxterieur dans le dictionnaire
    for equi_ex in (equipes_exterieure):
        nom_equipe_ex = equi_ex.find("span")
        if nom_equipe_ex:
            equipe_ext = nom_equipe_ex.text.strip()
            equipes_dict["equipe_ext"].append(equipe_ext)

#Ajouter le score dans le dictionnaire
    for score in (score_domicile):
        score_id = score.find_next_sibling("span", id=lambda x: x and x.endswith('_homeScore'))
        score_d = score.find("span",class_=score_id)
        if score_d:
            score_dom = score_d.text.strip()
            equipes_dict["score"].append(score_dom)
    df = pd.DataFrame(equipes_dict)
        

# Afficher le dictionnaire des équipes à domicile
    if os.path.exists(path):
        data = pd.read_excel("resultats_ligue1.xlsx")
        data = pd.concat([df,data],ignore_index=True)
        data=data.drop_duplicates()
        data.to_excel(nom_fichier, index=False)
    else:
        df.to_excel(nom_fichier, index=False)

h_fin = time.time()
print('temps d execution',h_fin-h_debut,'secondes')
print(data.shape)







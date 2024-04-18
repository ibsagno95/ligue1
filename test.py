import os
import requests
#html5lib
from bs4 import BeautifulSoup
import pandas as pd

nom_fichier = "resultats_ligue1.xlsx"
path = 'C:/Users/Ibrahima SAGNO/Documents/tuto_scraping/resultats_ligue1.xlsx'
url = "https://www.ligue1.fr/calendrier-resultats?seasonId=2022-2023&matchDay=36&StatsActiveTab=0"

def get_text_if_not_none(e):
    if e:
        return e.text.strip() # enlever les espaces avec strip
    return None

response = requests.get(url)
response.encoding = response.apparent_encoding #"utf-8"

if response.status_code == 200:
    html = response.text
    #print(html)
    f=open("ligue1.html","w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html,'html.parser')

        #equipe à domicile


equipes_dict = {"saisons":[],
                "journee":[],
                              "equipe_dom":[],
                             "score_dom":[],
                             "equipe_ext":[]}


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
        equipes_dict["journee"].append(journee.text.strip())

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
        equipes_dict["score_dom"].append(score_dom)
df = pd.DataFrame(equipes_dict)


        

# Afficher le dictionnaire des équipes à domicile
#print(equipes_domicile_dict)

#df=pd.DataFrame(equipes_dict)

if os.path.exists(path):
    data = pd.read_excel("resultats_ligue1.xlsx")
    data = pd.concat([df,data],ignore_index=True)
    data=data.drop_duplicates()
    data.to_excel(nom_fichier, index=False)
else:
    df.to_excel(nom_fichier, index=False)

print(data.describe)










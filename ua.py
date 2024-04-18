import requests
#html5lib
from bs4 import BeautifulSoup

url = "https://codeavecjonathan.com/scraping/recette_ua/"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

def get_text_if_not_none(e):
    if e:
        return e.text.strip() # enlever les espaces avec strip
    return None

response = requests.get(url,headers=HEADERS)
response.encoding = response.apparent_encoding #"utf-8"

if response.status_code == 200:
    html = response.text
    #print(html)
    f=open("recette.html","w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html,'html.parser')
    titre=soup.find("h1").text #retourne le premier element trouvé
    print(titre)

    description = get_text_if_not_none(soup.find("p", class_ ="description")) #class avec underscore
    print(description)

    #ingredients
    div_ingredients = soup.find("div",class_='ingredients')
    e_ingredients = div_ingredients.find_all("p")
    for e_ingredient in e_ingredients:
        print("ENGREDIENTS",e_ingredient.text)

    #etapes preparation

    td_etape = soup.find("table",class_ = "preparation")
    e_etapes = td_etape.find_all("td",class_ = "preparation_etape")
    for e_etape in e_etapes:
        print("ETAPES",e_etape.text)


else:
    print("ERREUR:",response.status_code)

print("FIN")
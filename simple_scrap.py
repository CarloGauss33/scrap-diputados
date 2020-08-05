import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup



def scrap_web(link, project_id):
    pure_html = urlopen(link)
    soup_html = BeautifulSoup(pure_html, 'html.parser')
    results_dict = dict()

    meta = soup_html.find(id="info-ficha").find_all('div', {'class':'dato'})
    metatags = [i.string.lstrip("\r\n").rstrip("\r\n").strip().replace(":", "") for i in meta]
    meta = soup_html.find(id="info-ficha").find_all('strong')
    metadata = [i.string.lstrip("\r\n").rstrip("\r\n").strip() for i in meta]

    meta = dict()
    for k in range(len(metatags)):
        meta.update({metatags[k]:metadata[k]})
    
    # Ahora votaciones individuales
    data = dict()
    divs = soup_html.find_all('section', {'class':'section group'})
    del divs[3]
    for div in divs:
        name = div.find('h3', {'class':'colTitle'}).string.strip()
        diputados = [i.string.strip() for i in div.find_all('a')]

        data.update({name: diputados})



    return True, data, meta
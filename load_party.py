import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def cargar_diputados(filepath):
    datos = dict()
    pure_html = urlopen('https://www.camara.cl/diputados/diputados.aspx')
    soup_html = BeautifulSoup(pure_html, 'html.parser')

    diputados = soup_html.find_all('article', {'class': 'grid-2'})

    for diputado in diputados:
        datos_diputado = dict()
        name =  diputado.find('h4').find('a').string
        distr_nd_party = diputado.find_all('p')
        for k in distr_nd_party:
            raw_data = k.string.split(':')
            datos_diputado.update({raw_data[0]:raw_data[1]})
        
        mail = diputado.find('a', {'class':'contacto'})
        mail = mail.get('href').replace('mailto:', '').replace('?subject=Consulta', '')

        datos_diputado.update({'Correo': mail})
        datos.update({name: datos_diputado})

    with open(filepath, 'w', encoding='utf-8') as outfile:
        json.dump(datos, outfile, indent=4, ensure_ascii=False)

    return True


if __name__ == "__main__":
    cargar_diputados('results/diputados.json')
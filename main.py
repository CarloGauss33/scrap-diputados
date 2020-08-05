import load_party
import argparse
import full_scrapper
import sys

parser = argparse.ArgumentParser(description='Scraping de la camara de diputados de Chile')

parser.add_argument('-p','--proyectos', default='30', type=int, help='Cantidad de proyectos a scrapear')
parser.add_argument('-i','--id', default='0', type=int, help='id del proyecto inicial para scrapear (opcional)')
parser.add_argument('-d','--diputados', help='Actualiza la informacion de los diputados', const=True, default=False, nargs='?')
parser.add_argument('-f','--folder', default='./results',type=str ,help='path donde guardar los datos')
parser.add_argument('-v', help='mostrar progreso', const=True, default=False, nargs='?')
args = parser.parse_args()

if args.diputados:
    load_party.cargar_diputados(f'{args.folder}/diputados.json')
if args.id == 0:
    init_id = full_scrapper.get_last_id()
else:
    init_id = args.id
print()
print("SCRAPPING IN PROGRESS  \n")

full_scrapper.full_scrap(init_id, args.proyectos, f'{args.folder}/proyectos.json', args.v)

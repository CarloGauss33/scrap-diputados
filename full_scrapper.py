import sys
import simple_scrap
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import json
import os


def get_last_id():
    pure_html = urlopen("https://www.camara.cl/legislacion/sala_sesiones/votaciones.aspx")
    soup_html = BeautifulSoup(pure_html, 'html.parser')


    #opening the results table
    tbody = soup_html.find(id="ContentPlaceHolder1_ContentPlaceHolder1_PaginaContent_pnlVotaciones")
    #getting the last votation
    vot_lin = tbody.find_all("a")
    last_vot = vot_lin[0].get("href").split("=")[1]

    return int(last_vot)



def full_scrap(start_id ,wanted_results, filepath, verbose):
    new_data = []
    if verbose:
        toolbar_width = wanted_results

        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))


    if wanted_results > 30:
        times = wanted_results//30
        
        for i in range(0, times):
            full_scrap(start_id - 30*i, 30, filepath)
        
        full_scrap(start_id +30*times, wanted_results%30, filepath)

        return True

    n_of_projects = wanted_results
    last_project = start_id
    for project_n in range(last_project, last_project - n_of_projects, -1):
        try:
            link = f"https://www.camara.cl/legislacion/sala_sesiones/votacion_detalle.aspx?prmIdVotacion={project_n}"
            status, project_results, meta = simple_scrap.scrap_web(link, project_n)

            project_dict = dict()
            if status:
                meta.update({"votaciones": project_results})
                new_data.append(meta)
        except urllib.error.HTTPError:
            pass
        
        if verbose:
            sys.stdout.write("-")
            sys.stdout.flush()
    if verbose:
        sys.stdout.write("]\n") 

    old_data = []
    if os.path.isfile(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            old_data = json.load(f)
    
    with open(filepath, 'w+', encoding='utf-8') as outfile:
        json.dump(old_data + new_data, outfile, indent=4, ensure_ascii=False)

    return True
if __name__ == "__main__":
    full_scrap(get_last_id(), 10, "./results/data.json")

# importing the required libraries
import gspread
import csv
import json
import config

#HEADER for covid_qc_cas, covid_qc_cas_total, covid_qc_deaths
COLUMNS = ["Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec", "Estrie", "Montréal", "Outaouais", "Abitibi-Témiscamingue", "Côte-Nord", "Nord-du-Québec", "Gaspésie – Îles-de-la-Madeleine", "Chaudière-Appalaches", "Laval", "Lanaudière", "Laurentides", "Montérégie", "Nunavik", "Terres-Cries-de-la-Baie-James", "Hors Québec", "Région à déterminer", "Total", "date"]
#columns indexes for covid_qc_cas, covid_qc_cas_total, covid_qc_deaths
columns_dict = {"Bas-Saint-Laurent": 0, "Saguenay – Lac-Saint-Jean": 1, "Capitale-Nationale": 2, "Mauricie-et-Centre-du-Québec": 3, "Estrie": 4, "Montréal": 5, "Outaouais": 6, "Abitibi-Témiscamingue": 7, "Côte-Nord": 8, "Nord-du-Québec": 9, "Gaspésie – Îles-de-la-Madeleine": 10, "Chaudière-Appalaches": 11, "Laval": 12, "Lanaudière": 13, "Laurentides": 14, "Montérégie": 15, "Nunavik": 16, "Terres-Cries-de-la-Baie-James": 17, "Hors Québec": 18, "Région à déterminer": 19, "Total": 20, "date": 21}

#HEADER and column indexes for covid_qc_vaccin
COLUMNS_VAC = ["Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec", "Estrie", "Montréal", "Outaouais", "Abitibi-Témiscamingue", "Côte-Nord", "Nord-du-Québec", "Gaspésie – Îles-de-la-Madeleine", "Chaudière-Appalaches", "Laval", "Lanaudière", "Laurentides", "Montérégie", "Nunavik", "Terres-Cries-de-la-Baie-James", "Opitciwan", "Wemotaci", "Manawan", "Inconnu", "Total", "date"]
columns_dict_vac = {"Bas-Saint-Laurent": 0, "Saguenay – Lac-Saint-Jean": 1, "Capitale-Nationale": 2, "Mauricie-et-Centre-du-Québec": 3, "Estrie": 4, "Montréal": 5, "Outaouais": 6, "Abitibi-Témiscamingue": 7, "Côte-Nord": 8, "Nord-du-Québec": 9, "Gaspésie – Îles-de-la-Madeleine": 10, "Chaudière-Appalaches": 11, "Laval": 12, "Lanaudière": 13, "Laurentides": 14, "Montérégie": 15, "Nunavik": 16, "Terres-Cries-de-la-Baie-James": 17, "Opitciwan": 18, "Wemotaci":19, "Manawan":20, "Inconnue": 21, "Total": 22, "date": 23}

#HEADER and column indexes for covid_qc_investigations
COLUMNS_INV = ['Prélèvements effectués', 'Analyses réalisées', 'Cas négatifs', 'Cas confirmés', 'date']
columns_dict_inv = {'Prélèvements effectués': 0, 'Analyses réalisées': 1, 'Cas négatifs': 2, 'Cas confirmés': 3, 'date': 4}

def gs_update(gs_key, data_dict, columns_dict, json_filename=config.gs_json_config):
	gs = gspread.service_account(filename=json_filename)
	sh = gs.open_by_key(gs_key)
	worksheet = sh.get_worksheet(0)
	data_list = dict_to_list(data_dict, columns_dict)
	worksheet.append_row(data_list)

def dict_to_list(data_dict, columns_dict):
	data_list = [None]*(len(columns_dict)+1)
	for key in data_dict:
		if key != "Madeleine":
			if key not in data_dict:
				data_list[columns_dict[key]] = 'NA'
			data_list[columns_dict[key]] = data_dict[key]
		else:
			data_list[10] = data_dict[key]
	return data_list

def txt_to_gs(file_txt, gs_key, columns_dict):
	with open(file_txt, 'r') as file:
		for line in file:
			line_1 = line.replace("'Inconnu'", "'Inconnue'").replace("'", '"').replace("Saguenay - Lac", "Saguenay – Lac").replace("Gaspésie - Îles", "Gaspésie – Îles").replace("Mauricie et Centre", "Mauricie-et-Centre")
			line_dict = json.loads(line_1)
			gs_update(gs_key, line_dict, columns_dict)

def post_header(gs_key, header, json_filename=config.gs_json_config):
	gc = gspread.service_account(filename=json_filename)
	sh = gc.open_by_key(gs_key)
	worksheet = sh.get_worksheet(0)
	worksheet.append_row(header)

#post_header(gs_key = config.gs_key_vaccin, header = COLUMNS_VAC, json_filename=config.gs_json_config)
txt_to_gs(file_txt='vaccin.txt', gs_key=config.gs_key_vaccin, columns_dict=columns_dict_vac)
#txt_to_gs(file_txt='deaths_qc.txt', gs_key=config.gs_key_deaths)
#txt_to_gs(file_txt='investigations.txt', gs_key=config.gs_key_investigations, columns_dict=columns_dict_inv)
#txt_to_gs(file_txt='covid_qc_total.txt', gs_key=config.gs_key_cas_total, columns_dict=columns_dict)
import requests
import re
from bs4 import BeautifulSoup

url_situation = "https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/"
url_vaccination = "https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/donnees-sur-la-vaccination-covid-19/"

url_cas_region = "https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/cas-region.csv"
url_cas_region_7jours = "https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/cas-region-7jours.csv"
url_deaths = "https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/deces-region.csv"
url_vaccin = "https://cdn-contenu.quebec.ca/cdn-contenu/sante/documents/Problemes_de_sante/covid-19/csv/doses-vaccins.csv"

id_div_deaths_date = "c63043"
id_div_vaccin_date = "c81603"

list_of_months = ['ja', 'f', 'mar', 'avr', 'mai', 'juin', 'juil', 'ao', 'sep', 'oct', 'nov', 'd']
dict_of_months = {'ja': 'janvier', 'f': 'février', 'mar': 'mars', 'avr': 'avril', 'mai': 'mai', 'juin': 'juin', 'juil': 'juillet', 'ao': 'août', 'sep': 'septembre', 'oct': 'octobre', 'nov': 'novembre', 'd': 'décembre'}
dict_of_months_numeric = {'01': 'janvier', '02': 'février', '03': 'mars', '04': 'avril', '05': 'mai', '06': 'juin', '07': 'juillet', '08': 'août', '09': 'septembre', '10': 'octobre', '11': 'novembre', '12': 'décembre'}


def get_soup(url):
	result = requests.get(url)
	src = result.content
	soup = BeautifulSoup(src, "html.parser")
	return soup

def get_data_list(url):
	src = requests.get(url)
	src.encoding = "utf-8"
	data_list = src.text.replace("\xa0", " ").split("\n")
	return data_list

def get_one_column_data(data_list):
	data_dict = {}
	for data in data_list:
		row_data_list = data.split(";")
		region_string = row_data_list[0]
		m = re.search("[A-Z]+", region_string)
		region_name =region_string[m.start():]
		data_init = row_data_list[1].replace("\r", "")
		data = int(data_init.replace(" ", ""))
		data_dict[region_name] = data
	return data_dict

def get_cas_region(url):
	"""pattern:
	﻿Régions sociosanitaires;10 janvier;11 janvier;12 janvier;13 janvier;14 janvier;15 janvier;Total des cas confirmés depuis le début de la pandémie
	01 - Bas-Saint-Laurent;7;2;4;4;7;10;1 429
	"""
	cas_data_list = get_data_list(url)
	row_of_dates = cas_data_list[0]
	list_of_dates = extract_date(row_of_dates)
	key_total = "Total des cas confirmés depuis le début de la pandémie"
	region_data = cas_data_list[1:-1]
	number_case_dict = {}
	number_total_dict = {}
	for index, date in enumerate(list_of_dates):
		if index != (len(list_of_dates)-1):
			number_case_dict["date"] = date
			for region in region_data:
				row_data_list = region.split(";")
				region_string = row_data_list[0]
				m = re.search("[A-Z]+", region_string)
				if m is not None:
					region_name = region_string[m.start(0):]
					# preciser try et except!
					try:
						number_of_cases = int(row_data_list[index+1].replace("\r", "").replace(" ", ""))
					except:
						number_of_cases = row_data_list[index+1]
					number_case_dict[region_name] = number_of_cases
			# print(number_case_dict)
			update_data_file("covid_qc_decembre.txt", number_case_dict)
		else:
			number_case_dict["date"] = date
			number_total_dict["date"] = date
			for region in region_data:
				row_data_list = region.split(";")
				region_string = row_data_list[0]
				m = re.search("[A-Z]+", region_string)
				if m is not None:
					region_name = region_string[m.start(0):]
					# preciser try et except!
					try:
						number_of_cases = int(row_data_list[index+1].replace("\r", "").replace(" ", ""))
						number_total = int(row_data_list[index+2].replace("\r", "").replace(" ", ""))
					except:
						number_of_cases = row_data_list[index+1]
					number_case_dict[region_name] = number_of_cases
					number_total_dict[region_name] = number_total
					print(number_case_dict)
					# print(number_total_dict)
	return number_case_dict, number_total_dict

def get_deaths_data(url_deaths, soup, id_div_deaths_date):
	deaths_data_list = get_data_list(url_deaths)[1:-1]
	number_deaths_dict = get_one_column_data(deaths_data_list)
	div_deaths_date = soup.find(id=id_div_deaths_date).p.text
	deaths_date = div_deaths_date.split(",")[2].strip().replace("\xa0", " ")
	number_deaths_dict["date"] = deaths_date
	return number_deaths_dict

def get_vaccin_data(url_vaccin, soup, id_div_vaccin_date):
	vaccin_data_list = get_data_list(url_vaccin)[1:-1]
	number_vaccin_dict = get_one_column_data(vaccin_data_list)
	div_vaccin_date = soup.find(id=id_div_vaccin_date).p.text
	vaccin_date = div_vaccin_date.split(",")[1].strip().replace("\xa0", " ")
	number_vaccin_dict["date"] = vaccin_date
	return number_vaccin_dict

def update_data_file(filename, dict_of_data):
    with open(filename, "r", encoding = "utf-8") as f:
        if dict_of_data["date"] not in f.read():
            with open(filename, "a", encoding = "utf-8") as f:
                f.write(str(dict_of_data))
                f.write("\n")

def extract_date(date_string):
    list_of_extracted_dates = []
    list_of_dates = date_string.split(";")[1:-1]
    for date_item in list_of_dates:
        if not '2021-' in date_item:
            number = extract_number(date_item)
            month = extract_month(date_item)
            extracted_date = '{} {} 2021'.format(number, month)
        else:
            date_list = date_item.split('-')
            month = dict_of_months_numeric[date_list[1]]
            if date_list[2].startswith('0'):
                number = date_list[2][1:]
            else:
                number = date_list[2]
            extracted_date = '{} {} 2021'.format(number, month)
        list_of_extracted_dates.append(extracted_date)
    return list_of_extracted_dates

def extract_number(date_item):
    number = re.search('[0-3]?[0-9]', date_item)
    if number.group(0).startswith('0'):
        number_without_zero = number.group(0)[1:]
    else:
        number_without_zero = number.group(0)
    return number_without_zero

def extract_month(date_item):
    for month_name in list_of_months:
        if month_name in date_item:
            month = dict_of_months[month_name]
            break
    return month 

soup = get_soup(url_situation)
soup_vaccination = get_soup(url_vaccination)

number_case_dict_7jours, number_semaine_7jours = get_cas_region(url_cas_region_7jours)
update_data_file("covid_qc_decembre.txt", number_case_dict_7jours)

number_case_dict, number_total_dict = get_cas_region(url_cas_region)
update_data_file("covid_qc_decembre.txt", number_case_dict)
update_data_file("covid_qc_total.txt", number_total_dict)

number_deaths_dict =  get_deaths_data(url_deaths, soup, id_div_deaths_date)
update_data_file("deaths_qc.txt", number_deaths_dict)

number_vaccin_dict =  get_vaccin_data(url_vaccin, soup_vaccination, id_div_vaccin_date)
update_data_file("vaccin.txt", number_vaccin_dict)

div_investigations = soup.find(id="c50212")

investigations = div_investigations.ul.find_all('li')
number_investigations_dict = {}
for li_item in investigations:
	data_list_inv = li_item.text.split(":")
	dict_key = " ".join(data_list_inv[0].split()[0:2])
	if dict_key[-1].isnumeric():
		dict_key = dict_key[:-1]
	number_investigations_dict[dict_key] = int(data_list_inv[-1].strip().replace(" ", "").replace("\xa0", ""))

date_investigation = " ".join(investigations[0].text.split(":")[0].split()[3:])	
number_investigations_dict["date"] = date_investigation
#print(number_investigations_dict)
update_data_file("investigations.txt", number_investigations_dict)

div_hospitalisations = soup.find(id="c50210")
hospitalisations = div_hospitalisations.ul.find_all('li')
number_hospitalisations_dict = {}
for li_item in hospitalisations:
	data_list = li_item.text.split(":")
	dict_key = data_list[0].strip()
	if dict_key[-1].isnumeric():
		dict_key = dict_key[:-1]
	number_hospitalisations_dict[dict_key] = int(data_list[-1].strip().replace(" ", "").replace("\xa0", ""))
hosp_string = div_hospitalisations.p.text
result  = re.search("[0-2]?[0-9].{4,11}202.", hosp_string)
date_hospitalisation = result.group(0).replace("\xa0", " ")
number_hospitalisations_dict["date"] = date_hospitalisation
#print(number_hospitalisations_dict)
update_data_file("hospitalisations.txt", number_hospitalisations_dict)

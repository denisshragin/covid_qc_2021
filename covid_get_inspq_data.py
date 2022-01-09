import pandas as pd
import gspread

COVID_AGES_SEX_HEADER = ['Nb_Cas_Cumulatif', 'Nb_Deces_Cumulatif_Total']
REGIONS=['Date', '01 - Bas-Saint-Laurent', '02 - Saguenay - Lac-Saint-Jean', '03 - Capitale-Nationale', '04 - Mauricie et Centre-du-Québec', '05 - Estrie', '06 - Montréal', '07 - Outaouais', '08 - Abitibi-Témiscamingue', '09 - Côte-Nord', '10 - Nord-du-Québec', '11 - Gaspésie - Îles-de-la-Madeleine', '12 - Chaudière-Appalaches', '13 - Laval', '14 - Lanaudière', '15 - Laurentides', '16 - Montérégie', '17 - Nunavik', '18 - Terres-Cries-de-la-Baie-James', 'Région inconnue', 'Hors Québec', 'Ensemble du Québec']
AGES = ['Date', '0-9 ans', '10-19 ans', '20-29 ans', '30-39 ans', '40-49 ans', '50-59 ans', '60-69 ans', '70-79 ans', '80-89 ans', '90 ans et plus', 'Âge inconnu']
SEX = ['Date', 'Masculin', 'Féminin', 'Sexe inconnu']
INCONNU = ['Date', 'Inconnu']


URL_COVID19_QC_RAPPORT_INSPQ = "https://msss.gouv.qc.ca/professionnels/statistiques/documents/covid19/COVID19_Qc_RapportINSPQ_VigieCategories.csv"

gs_covid_regions_inspq_url= "https://docs.google.com/spreadsheets/d/1lyEW2HlZApsqQnDMS8xDPs6bwJF4wrYa3Ir6rXgGk_U/edit#gid=0"

gs_ages_inspq_url = "https://docs.google.com/spreadsheets/d/1q0j-neZzVe8RxvcDTSAN6i0WYFRA_0vIdkNyfpegWjM/edit#gid=0"

gs_sex_inspq_url = "https://docs.google.com/spreadsheets/d/1XuIp7rYf2rXHajUwuE4km1Cja53M_-GeapqVkJpIBlI/edit#gid=0"


gc = gspread.service_account(filename='covid-qc-2021-eb330fb1e2f3.json')

df = pd.read_csv(URL_COVID19_QC_RAPPORT_INSPQ)

covid_inspq_df_header = list(df)[2:]
today_date=df.iloc[0,0]

# update spreadsheets with today's region's data
wb_regions=gc.open_by_url(gs_covid_regions_inspq_url)

for header in covid_inspq_df_header:
    worksheet_regions=wb_regions.worksheet(header)
    data_dict={}
    data_dict['Date'] = today_date
    data_regions = {}
    for index, row in df.iterrows():
        data_dict[row['Categorie']]=row[header]
    for key in data_dict:
        if key in REGIONS:
            data_regions[key]=data_dict[key]

    data_regions_list=list(data_regions.values())
    worksheet_regions.append_row(data_regions_list)

# # update spreadsheets with today's ages and sex data
wb_ages=gc.open_by_url(gs_ages_inspq_url)
wb_sex=gc.open_by_url(gs_sex_inspq_url)

for header in COVID_AGES_SEX_HEADER:
    worksheet_ages=wb_ages.worksheet(header)
    worksheet_sex=wb_sex.worksheet(header)
    data_dict={}
    data_dict['Date'] = today_date
    data_ages = {}
    data_sex = {}
    for index, row in df.iterrows():
        data_dict[row['Categorie']]=row[header]
    for key in data_dict:
        if key in  AGES:
            data_ages[key]=data_dict[key]
        if key in SEX:
            data_sex[key] = data_dict[key]
    data_ages_list=list(data_ages.values())
# 	print(data_ages)

    data_sex_list=list(data_sex.values())
# 	print(data_sex)

    worksheet_ages.append_row(data_ages_list)
    worksheet_sex.append_row(data_sex_list)
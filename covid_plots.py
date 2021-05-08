import chart_studio.plotly as plt
import plotly.offline as offline
import plotly.graph_objects as go
import pandas as pd
from pandas import *
from plotly.subplots import make_subplots
import gspread
import csv
import json
import config

#dataframe = pd.DataFrame(worksheet.get_all_records())

REGIONS = ["Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec", "Estrie", "Montréal", "Outaouais", "Abitibi-Témiscamingue", "Côte-Nord", "Nord-du-Québec", "Gaspésie-Îles-de-la-Madeleine", "Chaudière-Appalaches", "Laval", "Lanaudière", "Laurentides", "Montérégie", "Nunavik", "Terres-Cries-de-la-Baie-James", "Hors Québec", "Région à déterminer"]


def get_df_from_gs(gs_key, json_filename=config.gs_json_config):
	gs = gspread.service_account(filename=json_filename)
	sh = gs.open_by_key(gs_key)
	worksheet = sh.get_worksheet(0)
	dataframe = pd.DataFrame(worksheet.get_all_records())
	df_date = dataframe['date'].values.tolist()
	del dataframe['date']
	dataframe.dropna(inplace=True)
	return dataframe.astype('int64'), df_date

df_cas, df_date_cas = get_df_from_gs(gs_key=config.gs_key_cas, json_filename=config.gs_json_config)

df_cas_mean3 = df_cas.rolling(3).mean()
list_of_dict_cas = df_cas_mean3.to_dict('list')

df_cas_total, df_date_cas_total = get_df_from_gs(gs_key=config.gs_key_cas_total, json_filename=config.gs_json_config)

df_cas_total_mean3 = df_cas_total.rolling(3).mean()
list_of_dict_cas_total = df_cas_total_mean3.to_dict('list')

df_vaccin, df_date_vaccin = get_df_from_gs(gs_key=config.gs_key_vaccin, json_filename=config.gs_json_config)
list_of_dict_vaccin = df_vaccin.to_dict('list')

gs = gspread.service_account(filename=config.gs_json_config)
sh = gs.open_by_key(config.gs_key_population)
worksheet = sh.get_worksheet(0)
df_population = pd.DataFrame(worksheet.get_all_records())

df_cas_rel = df_cas_mean3.div(df_population.iloc[0], axis='columns')
df_cas_rel_percent = df_cas_rel.mul(100000)
list_of_dict_cas_rel = df_cas_rel_percent.to_dict('list')

df_vaccin_rel = df_vaccin.div(df_population.iloc[0], axis='columns')
df_vaccin_rel_percent = df_vaccin_rel.mul(100)
list_of_dict_vaccin_percent = df_vaccin_rel_percent.to_dict('list')



# def df_diff(df):
#     df_diff = df.diff()
#     return df_diff

# xls = ExcelFile('covid_qc.xlsx')
# df = xls.parse(xls.sheet_names[0])
# df_date = df['date'].values.tolist()
# del df['date']
# df_mean3 = df.rolling(3).mean()
# dict_initial = df_mean3.to_dict('list')
# print(dict_initial)

# dif = df_diff(df_mean3)
# line = DataFrame({'Bas-Saint-Laurent': 0, "Saguenay – Lac-Saint-Jean": 0,'Capitale-Nationale': 0, 'Mauricie-et-Centre-du-Québec': 0, 'Estrie': 0, 'Montréal': 0, 'Outaouais': 0, 'Abitibi-Témiscamingue': 0, 'Côte-Nord': 0, 'Nord-du-Québec': 0, 'Gaspésie-Îles-de-la-Madeleine': 0, 'Chaudière-Appalaches': 0, 'Laval': 0, 'Lanaudière': 0, 'Laurentides': 0, 'Montérégie': 0, 'Nunavik': 0, 'Terres-Cries-de-la-Baie-James': 0, "Hors Québec": 0, "Région à déterminer": 0, "total": 0}, index=[0])
# df_mean3.loc[-1] = [0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,]  # adding a row
# df_mean3.index = df_mean3.index + 1  # shifting index
# df_mean3 = df_mean3.sort_index()  # sorting by index
# df_result = dif.div(df_mean3)*100

# dict_initial_percent = df_result.to_dict('list')

# dict_speed_initial = {}
# for key in dict_initial:
#     speed_data = []
#     for counter, data in enumerate(dict_initial[key]):
#         if counter!= 0:
#             delta = (data) - dict_initial[key][(counter-1)]
#             speed_data.append(delta)
#             #print(key, counter, data, delta)
#         dict_speed_initial[key] = speed_data
# #print(dict_speed_initial)

''' Fig_1 "Cumulative Confirmed Cases", Fig_2 "Daily confirmed new cases", "Propagation dynamics", "Incidence Rate" '''

# fig_1 = go.Figure()

def create_figure(list_of_dict, df_x_axis, layout_title, xaxis_title, yaxis_title, svg_name):
	
	fig = go.Figure()
	# Add traces
	for key in list_of_dict:
	    if key != 'Région à déterminer':
	        if key != 'Hors Québec':
	            fig.add_trace(go.Scatter(x=df_x_axis, y=list_of_dict[key],
	            mode = 'lines+markers',
	            name = key))

	fig.update_layout(title=layout_title,
	                   xaxis_title=xaxis_title,
	                   yaxis_title=yaxis_title)
	fig.show()
	fig.write_html(svg_name)

create_figure(list_of_dict=list_of_dict_cas, df_x_axis=df_date_cas, layout_title='Cumulative Confirmed Cases in Québec', 
				xaxis_title='Date', yaxis_title='Cumulative Confirmed Cases', svg_name="Cumulative Confirmed Cases in Québec.svg")

create_figure(list_of_dict=list_of_dict_cas_rel, df_x_axis=df_date_cas, layout_title='Confirmed Cases in Québec on 100 000', 
				xaxis_title='Date', yaxis_title='Confirmed Cases on 100000', svg_name="Confirmed Cases in Québec on 100000.svg")

create_figure(list_of_dict=list_of_dict_cas_total, df_x_axis=df_date_cas_total, layout_title='Total Confirmed Cases in Québec', 
				xaxis_title='Date', yaxis_title='Total Confirmed Cases', svg_name="Total Confirmed Cases in Québec.svg")

# create_figure(list_of_dict=list_of_dict_vaccin, df_x_axis=df_date_vaccin, layout_title='Vaccins administrated in Québec', 
# 				xaxis_title='Date', yaxis_title='Total vaccins administrated', svg_name="Vaccins administrated in Québec.svg")

create_figure(list_of_dict=list_of_dict_vaccin_percent, df_x_axis=df_date_vaccin, layout_title='Vaccins administrated in Québec, % pop', 
				xaxis_title='Date', yaxis_title='Total vaccins administrated, % pop', svg_name="Vaccins administrated in Québec.svg")

# fig_2 = go.Figure()
# for key in dict_speed_initial:
#     if key != 'Région à déterminer':
#         if key != 'Hors Québec':
#             fig_2.add_trace(go.Scatter(x=df_date, y=dict_speed_initial[key],
#             mode = 'lines+markers',
#             name = key))
# fig_2.update_layout(title='Daily confirmed new cases au Québec',
#                    xaxis_title='Date',
#                    yaxis_title='Daily confirmed new cases')
# fig_2.show()
# fig_2.write_html("Daily confirmed new cases in Québec.svg")

# fig_3 = go.Figure()
# for key in dict_initial_percent:
#     if key != 'Région à déterminer':
#         if key != 'Hors Québec':
#             fig_3.add_trace(go.Scatter(x=df_date, y=dict_initial_percent[key],
#             mode = 'lines+markers',
#             name = key))
# fig_3.update_layout(title='Propagation dynamics in Québec',
#                    xaxis_title='Date',
#                    yaxis_title='New cases, % per day')
# fig_3.show()
# fig_3.write_html("Propagation dynamics in Québec.svg")
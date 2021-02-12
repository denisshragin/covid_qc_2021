import csv
import pandas as pd
import chart_studio.plotly as plt
import plotly.offline as offline
import plotly.graph_objects as go
from pandas import *
from plotly.subplots import make_subplots
import pygal 
""" f = open("sample.csv", "w")
writer = csv.DictWriter(
    f, fieldnames=["fruit", "count"])
writer.writeheader()
writer.writerows(
    [{"fruit": "apple", "count": "1"},
    {"fruit": "banana", "count": "2"}])
f.close()
OUTPUT
sample.csv
fruit,count
apple,1
banana,2 """


# df = pd.read_csv('/PathToFile.txt', sep = ',')

filename_hosp_txt = "hospitalisations.txt"
filename_hosp_csv = "hospitalisations.csv"
header_hosp = ("Nombre d’hospitalisations régulières", "Nombre en soins intensifs", "Nombre total d’hospitalisations", "date")

filename_deaths_txt = "deaths_qc.txt"
filename_deaths_csv = "deaths_qc.csv"
header_deaths = ("Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec", "Estrie", "Montréal", "Outaouais", "Abitibi-Témiscamingue", "Côte-Nord", "Nord-du-Québec", "Gaspésie – Îles-de-la-Madeleine", "Chaudière-Appalaches", "Laval", "Lanaudière", "Laurentides", "Montérégie", "Nunavik", "Terres-Cries-de-la-Baie-James", "Hors Québec", "Région à déterminer", "Total", "date")

filename_cas_txt = "covid_qc_decembre.txt"
filename_cas_csv = "covid_qc_decembre.csv"
header_cas= ("Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec", "Estrie", "Montréal", "Outaouais", "Abitibi-Témiscamingue", "Côte-Nord", "Nord-du-Québec", "Gaspésie – Îles-de-la-Madeleine", "Chaudière-Appalaches", "Laval", "Lanaudière", "Laurentides", "Montérégie", "Nunavik", "Terres-Cries-de-la-Baie-James", "Hors Québec", "Région à déterminer", "Total", "date")


def get_csv(filename_txt, filename_csv, header):
	with open(filename_txt, "r", encoding = "utf-8") as f:
		list_of_dict_data= []
		for line in f:
			line_d = dict(item.strip().split(':') for item in line.replace("\'", "").replace("{", "").replace("}", "").split(","))
			list_of_dict_data.append(line_d)
		#print(list_of_dict_data)

	with open(filename_csv, "w", encoding = "utf-8") as f:
		writer = csv.DictWriter(f, fieldnames = header)
		writer.writeheader()
		writer.writerows(list_of_dict_data)

	df = pd.read_csv(filename_csv, sep = ',')
	return df

df_hosp = get_csv(filename_hosp_txt, filename_hosp_csv, header_hosp)
#print(df_hosp)

df_deaths = get_csv(filename_deaths_txt, filename_deaths_csv, header_deaths)
#print(df_deaths)

df_cas = get_csv(filename_cas_txt, filename_cas_csv, header_cas)
#print(df_cas)

REGIONS = ["Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec", "Estrie", "Montréal", "Outaouais", "Abitibi-Témiscamingue", "Côte-Nord", "Nord-du-Québec", "Gaspésie – Îles-de-la-Madeleine", "Chaudière-Appalaches", "Laval", "Lanaudière", "Laurentides", "Montérégie", "Nunavik", "Terres-Cries-de-la-Baie-James", "Hors Québec", "Région à déterminer", "Total"]

df_cas_date = df_cas['date'].values.tolist()
del df_cas['date']
print(df_cas_date)

print(df_cas.dtypes)

for column in REGIONS:
	df_cas[column] = pd.to_numeric(df_cas[column], errors='coerce')

df_cas.fillna(0)

df_mean3 = df_cas.rolling(3).mean()
#dict_initial = df_cas.to_dict('list')
print(df_cas.dtypes)


# Add traces
fig_2 = go.Figure()
for region in REGIONS:
    # if key != 'Région à déterminer':
    #     if key != 'Hors Québec':
    fig_2.add_trace(go.Scatter(x=df_cas_date, y=df_mean3[region].values.tolist(),
    mode = 'lines+markers',
    name = region,
    connectgaps = True))
fig_2.update_layout(title='Daily confirmed new cases in Québec',
                   xaxis_title='Date',
                   yaxis_title='Daily confirmed new cases')
fig_2.show()
fig_2.write_html("Daily confirmed new cases in Québec.svg")




# del df_cas['date']
# #df_mean3 = df_cas.rolling(3).mean()
# dict_initial = df_cas.to_dict('list')
# print(dict_initial)

# a = []
# b = []
# c = []
# d = []

# line_chart = pygal.Line()
# # naming the title
# line_chart.title = 'Daily confirmed new cases in Québec'
# # adding range of months from 1 to 12
# line_chart.x_labels = df_cas_date#.to_string()
# for index,row in df_cas.iterrows():
#     a.append(row["Bas-Saint-Laurent"])
#     b.append(row["Saguenay – Lac-Saint-Jean"])
#     c.append(row["Capitale-Nationale"])
#     d.append(row["Mauricie-et-Centre-du-Québec"])
#    # "Bas-Saint-Laurent", "Saguenay – Lac-Saint-Jean", "Capitale-Nationale", "Mauricie-et-Centre-du-Québec"
# # adding the     
# line_chart.add('Bas-Saint-Laurent', a)
# line_chart.add('Saguenay – Lac-Saint-Jean', b)
# line_chart.add('Capitale-Nationale', c)
# line_chart.add('Mauricie-et-Centre-du-Québec', d)
# # rendering  the file
# line_chart.render_to_file("line_chart.svg")









# # Add traces
# fig_2 = go.Figure()
# for key in dict_initial:
#     if key != 'Région à déterminer':
#         if key != 'Hors Québec':
#             fig_2.add_trace(go.Scatter(x=df_cas_date, y=dict_initial[key],
#             mode = 'lines+markers',
#             name = key))
# fig_2.update_layout(title='Daily confirmed new cases in Québec',
#                    xaxis_title='Date',
#                    yaxis_title='Daily confirmed new cases')
# fig_2.show()
# fig_2.write_html("Daily confirmed new cases in Québec.svg")



#print(type(line_d))
		# for item in line_d.items():
		# 	print(item)

		# # for items in line_d:
		# 	new_value = value.strip()
		# 	if new_value.isdigit():
		# 		new_value = int(new_value)
		# 	line_d[key] = new_value
		# print(line_d)
		# print(type(line_d))


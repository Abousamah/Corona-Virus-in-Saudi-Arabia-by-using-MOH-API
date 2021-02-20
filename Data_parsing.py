from nvd3 import multiBarChart,multiBarHorizontalChart
import json 
import requests
import gmplot

# Cumulated="https://services6.arcgis.com/bKYAIlQgwHslVRaK/arcgis/rest/services/Cumulative_Date_Grouped_ViewLayer/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
# RdataCumulated= requests.get(Cumulated).json()
# CumulatedJson = json.dumps(RdataCumulated, sort_keys=True, indent=4) # Beautify the JSON

DailyCases="https://services6.arcgis.com/bKYAIlQgwHslVRaK/arcgis/rest/services/VWPlacesCasesHostedView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
RdataDaily = requests.get(DailyCases).json()
DailyJson  = json.dumps(RdataDaily, sort_keys=True, indent=4) # Beautify the JSON

# Add all the cases togethor 
def Total():
	All_city= []
	All_Geo_x= []
	All_Geo_y= [] 
	for city in range(len(RdataDaily['features'])):

		Name_Eng = RdataDaily['features'][city]['attributes']["Name_Eng"]
		GEOx = RdataDaily['features'][city]['geometry']['x']
		GEOy = RdataDaily['features'][city]['geometry']['y']

		if Name_Eng not in All_city:
			All_city.append(Name_Eng)
			All_Geo_x.append(GEOx)
			All_Geo_y.append(GEOy)

	# print(len(All_city)) # print the length
	All_confirmed= []
	All_Deaths= []
	All_Tested= []
	All_Recovered= []

	for city in range(len(All_city)):
		
		Confirmed = 0
		Deaths = 0
		Tested = 0 
		Recovered = 0 
		date2 = []

		# Check for the last date
		for cases in range(len(RdataDaily['features'])) :
			date = RdataDaily['features'][cases]['attributes']["Reportdt"]
			if date not in date2:
				date2.append(date)
		date_now = max(date2)

		# Check for Confimed Cases
		for cases in range(len(RdataDaily['features'])) :
			check = RdataDaily['features'][cases]['attributes']["Name_Eng"]
			date = RdataDaily['features'][cases]['attributes']["Reportdt"]
			if All_city[city]  == check and date == date_now:
				Deaths    += RdataDaily['features'][cases]['attributes']["Deaths"]
				Recovered += RdataDaily['features'][cases]['attributes']["Recovered"]
				Confirmed += RdataDaily['features'][cases]['attributes']["Confirmed"]

		All_confirmed.append(Confirmed)
		All_Deaths.append(Deaths)
		All_Recovered.append(Recovered)

	rec = 0
	deaths = 0
	conf = 0

	Total_file=open('Total.json','w+')

	All_info2 = []
	for cases in range(len(All_city)):
		a={"city":All_city[cases],
		"Deaths":All_Deaths[cases],
		"Recovered":All_Recovered[cases],
		"Confirmed":All_confirmed[cases]}

		All_info2.append(dict(a))

		conf   += All_confirmed[cases]
		rec	   += All_Recovered[cases]
		deaths += All_Deaths[cases]

	print(f"Total Confirmed: {str(conf)}")
	print(f"Total Recovered: {str(rec)}")
	print(f"Total Deaths: 	 {str(deaths)}")

	Total_file.write(json.dumps(All_info2))
	Total_file.close()

	New_Geo_x= []
	New_Geo_y= []
	for Infected in range(len(All_info2)):
		infction = All_info2[Infected]['Confirmed']

		if infction != 0:
			New_Geo_x.append(All_Geo_x[Infected])
			New_Geo_y.append(All_Geo_y[Infected])


	random=[]
	for i in range(len(New_Geo_x)):
		random.append(0.009)

	gmap5 = gmplot.GoogleMapPlotter(23.68363, 45.76787, 6 ) 
	gmap5.heatmap(New_Geo_y,New_Geo_x,radius=20 , gradient=[(0, 0, 255, 0), (0, 255, 0, 0.9), (255, 0, 0, 1)] )
	gmap5.draw('map.html')

	Chart_all = open('Visiual.html','w+')

	chart = multiBarChart(width=3000, height=1000, x_axis_format=None)
	chart.add_serie(name="Recovered 1", y=All_Recovered, x=All_city)
	chart.add_serie(name="Infected 2", y=All_confirmed, x=All_city)
	chart.buildhtml()
	Chart_all.write(chart.htmlcontent)
	Chart_all.close()

Total()

# flask --app data_server run
from flask import Flask
from flask import request
from flask import render_template
import json


app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close() 

    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = "2020" 
    
    countries = list(data.keys())
    requested_data = {}
    for country in countries:
        requested_data[country] = data[country][requested_year]
    all_years = sorted(list(data[countries[0]].keys()))

    US_datapoints = ""
    Canada_datapoints = ""
    Mexico_datapoints = ""
    US_total = 0
    M_total = 0
    C_total = 0
    for year in all_years:
        for country in countries:
            x_value = 100 + (int(year)-1960)*5
            age = data[country][year]
            y_value = 400-(age-40)*5
            if country == "Canada":
                Canada_datapoints += str(x_value)
                Canada_datapoints += " "
                Canada_datapoints += str(y_value)
                Canada_datapoints += " "
                C_total += age
                # CX=x_value
                # CY=y_value
            if country == "United States":
                US_datapoints += str(x_value)
                US_datapoints += " "
                US_datapoints += str(y_value)
                US_datapoints += " "
                US_total += age
                # USX=x_value
                # USY=y_value
            if country == "Mexico":
                Mexico_datapoints += str(x_value)
                Mexico_datapoints += " "
                Mexico_datapoints += str(y_value)
                Mexico_datapoints += " "
                M_total += age
                # MX=x_value
                # MY=y_value
        # Average_datapoints += str((CX+USX+MX)/3)
        # Average_datapoints += str((CY+USY+MY)/3)
    # don't do it this way
    # US_average = US_total/61
    # M_average = M_total/61
    # C_average = C_total/61  
    # Total_Average = (US_average+M_average+C_average)/3

    # calculate average this way
    Total_Average = (US_total+M_total+C_total)/183
    Y_coordinate_total_Av = 400-(Total_Average-40)*5
    Average_datapoint = str(Y_coordinate_total_Av)

    x_axis_increments = [1960,1970,1980,1990,2000,2010,2020]
    y_axis_increments = [40,50,60,70,80,90,100]
    
    return render_template('index.html', Total_Average= Total_Average,
                           Average_datapoint=Average_datapoint, 
                           Canada_datapoints=Canada_datapoints, 
                           US_datapoints = US_datapoints,
                           Mexico_datapoints=Mexico_datapoints,
                            y_axis_increments=y_axis_increments, 
                            x_axis_increments=x_axis_increments, 
                            year=requested_year, all_years=all_years,data=requested_data)
     
    # countries = list(data.keys())
    # requested_data = {}

    # for country in data:
    #     requested_data[country] = data[country][requested_year]                    
                       #    years = sorted(data["Canada"].keys())) #, data=requested_data)
    # potentially add above ^^countries=sorted(data.keys)

@app.route('/year')
def year():
    f = open("data/life_expectancy.json", "r")
    data = json.load(f)
    f.close()  
    
    # age_range = [
    #     (-float("inf"), 54), (54, 57), (57, 60), (60, 63), (63, 65), (65, 68), (68, 70), (70, 73), (73, 76), (76, 79), (79, 82), (82, float("inf"))
    # ]

    age_range = [
        (-float("inf"), 57), (57, 60), (60, 63), (63, 65), (65, 68), (68, 70), (70, 73), (73, 76), (76, 79), (79, float("inf"))
    ]
    legend_increments = []
    for lo, hi in age_range: 
        if lo == -float("inf"):
            label = f"<{hi}"
        elif hi == float("inf"):
            label = f">{lo}"
        else:
            label = f"{lo}-{hi - 1}"
        legend_increments.append(label)

    legend_color = []
    for i, _ in enumerate(legend_increments):
        color_saturation = f"hsl(240,{int(100 / len(legend_increments) * (i + 1))}%,{100-int(100 / len(legend_increments) * (i + 1))}%)"
        legend_color.append(color_saturation)
    # ["MidnightBlue","MediumBlue","RoyalBlue","CornflowerBlue","DeepSkyBlue","LightSky","red","orange","yellow","green"]
    
    requested_year = request.args.get('year')
    if requested_year == None:
        requested_year = "2020"

    countries = list(data.keys())
    requested_data = {}
    for country in countries:
        requested_data[country] = data[country][requested_year]

    country_color = {}
    min, max = None, None
    min_country, max_country = None, None
    average = 73.29
    qualitative_analysis = []

    for country in requested_data:
        #getting qualitative analysis statistics
        life_exp = requested_data[country]
        if max is None or life_exp > max:
            max, max_country = life_exp, country
        if min is None or life_exp < min:
            min, min_country = life_exp, country
        if life_exp > average:
            analysis = f"{country} had a greater life expectancy than the average"
            qualitative_analysis.append(analysis) 
        if life_exp < average:
            analysis = f"{country} had a lower life expectancy than the average"
            qualitative_analysis.append(analysis)
        if life_exp == average:
            analysis = f"{country} had a life expectancy equal to the average"
            qualitative_analysis.append(analysis)
        # matching age to color range
        for i, (lower, upper) in enumerate(age_range):
            if lower <= requested_data[country] <= upper:
                country_color[country] = legend_color[i]

    print("loaded")
    return render_template(
        'year.html',
        qualitative_analysis=qualitative_analysis,
        max_country=max_country,
        min_country=min_country, 
        US_color=country_color["United States"], 
        CA_color=country_color["Canada"], 
        MX_color=country_color["Mexico"], 
        legend_color=legend_color,
        year=requested_year,  
        legend_increments=legend_increments
    )

app.run(debug=True, port = 12434)

#Imports
import pandas as pd
import folium
from IPython.display import display, HTML
import requests
from ipywidgets import interact_manual
import json

#Loading JSON file
with open('world-cities_json.json') as f:
    data = json.load(f)

#Creating sorted country list
country_list = []
for country in data:
    if country['country'] not in country_list:
        country_list.append(country['country'])
        country_list.sort()

#Drop down menu for countries, region, then city.
@interact_manual(Country = country_list)
def main(Country):
    with open('world-cities_json.json') as f:
        data = json.load(f)
        region_list = []
        for regions in data:
            if regions['country'] == Country and regions['subcountry'] not in region_list:
                region_list.append(regions['subcountry'])
                region_list.sort()
    @interact_manual(Region = region_list)
    def main2(Region):
        with open('world-cities_json.json') as f:
            data = json.load(f)
            city_list = [] 
            for cities in data:
                if cities['subcountry'] == Region and cities['name'] not in city_list:
                    city_list.append(cities['name'])
        @interact_manual(City = city_list)
        def main3(City):
            with open('world-cities_json.json') as f:
                data = json.load(f)
                City = City.strip()
                #diplay for City, Country
                display(HTML(f"<h1>{City, Country}</h1>"))
       

                #Small Description
                url = "https://wiki-briefs.p.rapidapi.com/search"
                querystring = {"q": f"{City, Country}","topk":"3"}
                headers = {
                            "X-RapidAPI-Key": "c26fa924d4mshf7d3c182f9cda2bp1c5e61jsn58e0d2666577",
                            "X-RapidAPI-Host": "wiki-briefs.p.rapidapi.com"
                                                                                                        }
                response = requests.request("GET", url, headers=headers, params=querystring)
                desc = response.json()
                summ = 'Summary'
                display(HTML(f"<b1><b>{summ}</b></b1>"))

                print(desc['summary'])

                #News About Place
                url2 = ('https://newsapi.org/v2/everything?'
                       f'q={City, Country}&'
                       'from=2022-12-05&'
                       'sortBy=popularity&'
                       'apiKey=c375f9d5d3cd4e1c8282dafc404bb78c')
                response2 = requests.get(url2)
                news = response2.json()
                
                print('-----------------------------------------------------------------------------')
                title1 = 'News'
                #Print top three news stories, if 3 can't be found a message will display.
                try:
                    display(HTML(f"<b1><b>{title1}</b></b1>"))
                    print(news['articles'][0]['title'])
                    print(news['articles'][0]['url'])

                    print(news['articles'][1]['title'])
                    print(news['articles'][1]['url'])

                    print(news['articles'][2]['title'])
                    print(news['articles'][2]['url'])
                except IndexError:
                    print('Cannot produce 3 news articles, not enough going on here.')
                #Get Coords
                def get_coordinates(search):
                    url = 'https://nominatim.openstreetmap.org/search'  # base URL without paramters after the "?"
                    options = { 'q' : search, 'format' : 'json'}
                    response = requests.get(url, params = options)            
                    geodata = response.json()
                    coords = { 'lat' : float(geodata[0]['lat']), 'lng' : float(geodata[0]['lon']) }
                    return coords

                coords = get_coordinates(City)
                lat = coords['lat']
                lng = coords['lng']
                print('-----------------------------------------------------------------------------')
                title3 = 'Airports nearby'
                display(HTML(f"<b1><b>{title3}</b></b1>"))
                url4 = f"https://aerodatabox.p.rapidapi.com/airports/search/location/{lat}/{lng}/km/100/16"

                querystring = {"withFlightInfoOnly":"true"}

                headers = {
                    "X-RapidAPI-Key": "c26fa924d4mshf7d3c182f9cda2bp1c5e61jsn58e0d2666577",
                    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
                }

                response4 = requests.request("GET", url4, headers=headers, params=querystring)
                try:
                    fl = response4.json()
                    print(fl['items'][0]['name'])
                    print(fl['items'][0]['iata'])
                    print(fl['items'][1]['name'])
                    print(fl['items'][1]['iata'])
                    print(fl['items'][2]['name'])
                    print(fl['items'][2]['iata'])
                except IndexError:
                    print('Not 3 Airports within 100km')
                #Weather
                url3 = "https://weather-by-api-ninjas.p.rapidapi.com/v1/weather"
                querystring = {"lat":lat,"lon":lng}
                headers = {
                    "X-RapidAPI-Key": "c26fa924d4mshf7d3c182f9cda2bp1c5e61jsn58e0d2666577",
                    "X-RapidAPI-Host": "weather-by-api-ninjas.p.rapidapi.com"
                }
                response3 = requests.request("GET", url3, headers=headers, params=querystring)
                title2 = 'Weather'
                print('-----------------------------------------------------------------------------')
                display(HTML(f"<b1><b>{title2}</b></b1>"))
                unit_options = ['Imperial', 'Metric']
                @interact_manual(Unit = unit_options)
                def main4(Unit):
                    wdata = response3.json()
                    if wdata['wind_degrees'] < 90:
                        wind_dirc = 'North'
                    elif wdata['wind_degrees'] > 90:
                        wind_dirc = 'East'
                    elif wdata['wind_degrees'] > 180:
                        wind_dirc = 'South'
                    elif wdata['wind_degrees'] > 270:
                        wind_dirc = 'West'
                    if Unit == 'Metric':
                        print(f"Temputure: {wdata['temp']} °C")
                        print(f"Feels like: {wdata['feels_like']} °C")
                        print(f"Humidity: {wdata['humidity']} %")
                        print(f"Wind Speed: {wdata['wind_speed']:.2f} kph from the {wind_dirc} ")
                    else:
                        print(f"Temputure: {(wdata['temp']*(9/5)+32):.2f} °F")
                        print(f"Feels like: {(wdata['feels_like']*(9/5)+32):.2f} °F")
                        print(f"Humidity: {wdata['humidity']} %")
                        print(f"Wind Speed: {(wdata['wind_speed']/1.609):.2f} mph from the {wind_dirc}")
                title4 = 'Air Quality'
                print('-----------------------------------------------------------------------------')
                display(HTML(f"<b1><b>{title4}</b></b1>"))
                url5 = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"

                querystring = {"lat":f"{lat}","lon":f"{lng}"}

                headers = {
                    "X-RapidAPI-Key": "c26fa924d4mshf7d3c182f9cda2bp1c5e61jsn58e0d2666577",
                    "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
                }

                response5 = requests.request("GET", url5, headers=headers, params=querystring)
                
                air_data = response5.json()
                print(f"The overall AQI is {air_data['overall_aqi']}")
                if air_data['overall_aqi'] < 50:
                    print('Air quality is satisfactory, and air pollution poses little or no risk.')
                elif air_data['overall_aqi'] < 100:
                    print('Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution.')
                elif air_data['overall_aqi'] < 150:
                    print('Members of sensitive groups may experience health effects. The general public is less likely to be affected.')
                elif air_data['overall_aqi'] < 200:
                    print('Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.')
                elif air_data['overall_aqi'] < 250:
                    print('Health alert: The risk of health effects is increased for everyone.')
                elif air_data['overall_aqi'] < 300:
                    print('Health warning of emergency conditions: everyone is more likely to be affected.')
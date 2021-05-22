#83.165.3.23

# importing the requests library
import requests
import json
import pandas as pd 
import sqlite3
import pandas.io.sql as sql



#def main():
#ip = "83.165.3.23"
#ip = "23.20.191.46"
#url1 = "https://api.ipgeolocationapi.com/geolocate/" + ip

def ipgeo(ip):

    url1 = "https://sys.airtel.lv/ip2country/" + ip + "/?full=true" #por ahora iremos usando esta

    #url1 = "http://api.ipstack.com/" + ip + "?access_key=fa3ea559085abe8f4a3eebbebd35695a"

    r = requests.get(url1)
    data = r.json()

    #json_formatted_str = json.dumps(data, indent=2)

    dataframe = {'network': ip, 'lat': data['lat'], 'lon': data['lon']}

    print(dataframe)

    #dataframe = pd.DataFrame.from_dict(data, orient="index")

    #print(dataframe)

    #print(json_formatted_str)

    #latitude = data['latitude']
    #longitude = data['longitude']
    #print("latitude " + str(latitude) + "\n")
    #print("longitude " + str(longitude) + "\n")

    #latitude = dataframe['lat']
    #longitude = dataframe['lon']
    #print("latitude " + str(latitude) + "\n")
    #print("longitude " + str(longitude) + "\n")

    #df = pd.json_normalize(dataframe['lat'])

    return dataframe






import glob
import os
import cPickle
from net_trainer import process_data
import csv
import numpy as np
import json

def analyze_data_on_stadium(filename, year, average_weather_dict):
    average_weather = average_weather_dict[os.path.splitext(filename)[0]]
    ann = load_ann("nets/" + filename)
    hr_dict = {}
    yearly_data = process_data("data/clean_data/batting_data/" + year + ".csv", average_weather[:-1])
    for i in yearly_data:
        player = i[1]
        result = np.argmax(ann.feedforward(i[0]))
        if result==1:
            if player not in hr_dict.keys():
                hr_dict[player] = 1
            else:
                hr_dict[player] += 1
    display_leaders(hr_dict, year, filename)

def display_leaders(hr_dict, year, stadium):
    hr_leaders = []
    for i in hr_dict.keys():
        hr_leaders.append([i, hr_dict[i]])
    hr_leaders = sorted(hr_leaders, key=lambda x: x[1], reverse=True)
    print year + " data on " + stadium
    print hr_leaders[0]
    print hr_leaders[1]
    print hr_leaders[2]
    print hr_leaders[3]
    print hr_leaders[4]
    print "-----------------------------"

def process_data(file_path, average_weather):
    data = []
    players = []
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            players.append(row.pop())
            data.append(row + average_weather)
    data = np.array(data, dtype=np.float64)
    data = [np.reshape(x, (8, 1)) for x in data]
    players = np.array(players)
    return zip(data, players)

def load_ann(path):
    with open(path, "rb") as file:
        ann = cPickle.load(file)
    return ann

wind_direction_dict = {
    "N": 0,
    "NNE": 22.5,
    "NE": 45,
    "ENE": 67.5,
    "E": 90,
    "ESE": 112.5,
    "SE": 135,
    "SSE": 157.5,
    "S": 180,
    "SSW": -157.5,
    "SW": -135,
    "WSW": -112.5,
    "W": -90,
    "WNW": -67.5,
    "NW": -45,
    "NNW": -22.5
}

def make_average_weather_dict():
    average_weather_dict = {}
    path = "data/raw_data/box_scores/"
    for filename in os.listdir(path):
        with open(path + filename) as file:
            daily_box_scores = json.load(file)
            games = daily_box_scores["league"]["games"]
            for i in games:
                game = i["game"]
                key = game["home"]["abbr"]
                if "weather" in game.keys():
                    game_weather = game["weather"]
                    game_weather = game_weather["current_conditions"] if "current_conditions" in game_weather.keys() else game_weather["forecast"]
                else:
                    continue
                temp = game_weather["temp_f"]
                humidity = game_weather["humidity"]
                wind_speed = game_weather["wind"]["speed_mph"]
                wind_direction = wind_direction_dict[game_weather["wind"]["direction"]]
                if key not in average_weather_dict.keys():
                    average_weather_dict[key] = [0,0,0,0,0]
                average_weather_dict[key][0] += temp/113.0
                average_weather_dict[key][1] += humidity/100.0
                average_weather_dict[key][2] += wind_speed/40.0
                average_weather_dict[key][3] += wind_direction/180.0
                average_weather_dict[key][4] += 1
    for key in average_weather_dict.keys():
        for i in range(0,4):
            average_weather_dict[key][i] = average_weather_dict[key][i]/float(average_weather_dict[key][4])
    return average_weather_dict

average_weather_dict = make_average_weather_dict()
for year in ["2018", "2019"]:
    for filename in os.listdir("nets/"):
        analyze_data_on_stadium(filename, year, average_weather_dict)

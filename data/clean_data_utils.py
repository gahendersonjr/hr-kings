from enum import Enum
import csv
import random
import os
import json
import math

class RawInputs(Enum):
    LAUNCH_SPEED = 53
    LAUNCH_ANGLE = 54
    LAUNCH_SPEED_ANGLE = 75

class RawInputDenominators(Enum):
    LAUNCH_SPEED = 121.7
    LAUNCH_ANGLE = 72.5
    LAUNCH_SPEED_ANGLE = 6.0

class RawInputsInfo(Enum):
    HC_X = 37
    HC_Y = 38
    DATE = 1
    PLAYER_NAME = 5
    RESULT = 8
    PLAY_DESCRIPTION = 15
    HOME_TEAM = 19
    AWAY_TEAM = 20

def write_to_file(path, clean_data):
    random.shuffle(clean_data)
    with open(path, "wb") as outfile:
      wr = csv.writer(outfile, delimiter=",")
      for clean_row in clean_data:
          wr.writerow(clean_row)

def get_normalization_denominator(raw_data_enum_name):
    name_as_string = str(raw_data_enum_name)
    enum_name = name_as_string[name_as_string.find('.')+1:]
    return RawInputDenominators[enum_name].value

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

def make_weather_dict():
    weather_dict = {}
    path = "raw_data/box_scores/"
    for filename in os.listdir(path):
        with open(path + filename) as file:
            daily_box_scores = json.load(file)
            games = daily_box_scores["league"]["games"]
            for i in games:
                game = i["game"]
                key = os.path.splitext(filename)[0] + game["home"]["abbr"] + game["away"]["abbr"]
                if "weather" in game.keys():
                    game_weather = game["weather"]
                    game_weather = game_weather["current_conditions"] if "current_conditions" in game_weather.keys() else game_weather["forecast"]
                else:
                    continue
                temp = game_weather["temp_f"]
                humidity = game_weather["humidity"]
                wind_speed = game_weather["wind"]["speed_mph"]
                wind_direction = wind_direction_dict[game_weather["wind"]["direction"]]
                weather_dict[key] = [temp/113.0, humidity/100.0, wind_speed/40.0, wind_direction/180.0]
    return weather_dict

def find_avg_horizontal_angle():
    averages = {}
    keys = ["right center field","left center field", "left field", "right field","center field"]
    for key in keys:
        averages[key] = [0,0]
    for year in ["2018", "2019"]:
        clean_rows = []
        with open("raw_data/batting_data/" + year + ".csv") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
              # In rare occasions some hits do not have hit coordinate values or games don't have weather data so they are excluded from training data
              if row[RawInputsInfo.HC_Y.value] == "null" or row[RawInputsInfo.HC_X.value] == "null":
                  continue
              for key in keys:
                  if key in row[RawInputsInfo.PLAY_DESCRIPTION.value].lower():
                      averages[key][0] += math.tan((float(row[RawInputsInfo.HC_X.value])-128.0)/(208.0-float(row[RawInputsInfo.HC_Y.value])))*180.0/math.pi*.75
                      averages[key][1] += 1
    for key in keys:
      averages[key][0] = float(averages[key][0])/float(averages[key][1])
      print key
      print averages[key][0]

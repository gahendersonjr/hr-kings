import json
import os

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
    for filename in os.listdir("C:/Users/Alan/Desktop/finalproject/hr-kings/data/box_scores/"):
        with open("data/box_scores/" + filename) as file:
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

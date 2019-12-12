from __future__ import division
import csv
import os
from clean_data_utils import RawInputs, RawInputDenominators, RawInputsInfo, write_to_file, get_normalization_denominator, make_weather_dict
import math

def cleanup_stadium_data_for_training():
    home_runs = []
    other_hits = []
    hr_dict = {}
    other_dict = {}
    weather_dict = make_weather_dict()
    path = "raw_data/batting_data/"
    # take all data points and put them in map based on home stadium
    for filename in os.listdir(path):
        with open(path + filename) as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
              key = row[RawInputsInfo.DATE.value]+row[RawInputsInfo.HOME_TEAM.value]+row[RawInputsInfo.AWAY_TEAM.value]
              # no hit coordinate data, skipping
              if row[RawInputsInfo.HC_Y.value] == "null" or row[RawInputsInfo.HC_X.value] == "null":
                  continue
              # no weather data, skipping
              if key not in weather_dict.keys():
                  continue
              # game in retractable stadium or dome, skipping
              if row[RawInputsInfo.HOME_TEAM.value] in ["TB", "SEA", "TOR", "HOU", "MIL", "MIA", "ARI"]:
                  continue
              clean_row = [float(row[i.value])/get_normalization_denominator(i) for i in RawInputs]
              # converting hit coordinate to horizantal angle. i borrowed this guys technique https://github.com/BillPetti/Statcast-Modeling/blob/master/statcast.battedball.woba.R
              horizontal_angle = math.tan((float(row[RawInputsInfo.HC_X.value])-128.0)/(208.0-float(row[RawInputsInfo.HC_Y.value])))*180.0/math.pi*.75
              clean_row.append(horizontal_angle/90.0)
              clean_row += weather_dict[key]
              if row[RawInputsInfo.HOME_TEAM.value] not in hr_dict.keys():
                  hr_dict[row[RawInputsInfo.HOME_TEAM.value]] = []
                  other_dict[row[RawInputsInfo.HOME_TEAM.value]] = []
              # Not counting inside the park home runs as they are rare and unpredictable from the data I am using.
              if row[RawInputsInfo.RESULT.value] == "home_run" and "inside-the-park" not in row[RawInputsInfo.PLAY_DESCRIPTION.value]:
                  hr_dict[row[RawInputsInfo.HOME_TEAM.value]].append(clean_row + [1])
              else:
                  other_dict[row[RawInputsInfo.HOME_TEAM.value]].append(clean_row + [0])
    # for each stadium in map, create a training, testing, validation set
    for key in hr_dict.keys():
        home_runs = hr_dict[key]
        other_hits = other_dict[key]
        train = home_runs[:int(len(home_runs)*.7)] + other_hits[:int(len(other_hits)*.7)]
        test = home_runs[int(len(home_runs)*.7):int(len(home_runs)*.85)] + other_hits[int(len(other_hits)*.7):int(len(other_hits)*.85)]
        valid = home_runs[int(len(home_runs)*.85):] + other_hits[int(len(other_hits)*.85):]
        write_to_file("clean_data/stadiums/train/" + key + ".csv", train)
        write_to_file("clean_data/stadiums/test/" + key + ".csv", test)
        write_to_file("clean_data/stadiums/valid/" + key + ".csv", valid)

cleanup_stadium_data_for_training()

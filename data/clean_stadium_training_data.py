from __future__ import division
import csv
import os
from parse_weather_data import make_weather_dict
from clean_data_utils import RawInputs, RawInputDenominators, RawInputsInfo, write_to_file, get_normalization_denominator

def cleanup_stadium_data_for_training():
    home_runs = []
    other_hits = []
    hr_dict = {}
    other_dict = {}
    path = "C:/Users/Alan/Desktop/finalproject/hr-kings/data/raw_data/batting_data/"
    # take all data points and put them in map based on home stadium
    for filename in os.listdir(path):
        with open(path + filename) as file:
            weather_dict = make_weather_dict()
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
              key = row[RawInputsInfo.DATE.value]+row[RawInputsInfo.HOME_TEAM.value]+row[RawInputsInfo.AWAY_TEAM.value]
              # In rare occasions some hits do not have hit coordinate values or games don't have weather data so they are excluded from training data
              if row[RawInputs.HC_Y.value] == "null" or row[RawInputs.HC_X.value] == "null" or key not in weather_dict.keys():
                  continue
              clean_row = [float(row[i.value])/get_normalization_denominator(i) for i in RawInputs] + weather_dict[key]
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
        train_hr = home_runs[:int(len(home_runs)*.8)]
        train_other = other_hits[:int(len(other_hits)*.8)]
        train_hr = train_hr * int(len(train_other)/len(train_hr)) # oversampling hr data for training
        train = train_hr + train_other
        test = home_runs[int(len(home_runs)*.8):int(len(home_runs)*.9)] + other_hits[int(len(other_hits)*.8):int(len(other_hits)*.9)]
        valid = home_runs[int(len(home_runs)*.9):] + other_hits[int(len(other_hits)*.9):]
        write_to_file("clean_data/stadiums/train/" + key + ".csv", train)
        write_to_file("clean_data/stadiums/test/" + key + ".csv", test)
        write_to_file("clean_data/stadiums/valid/" + key + ".csv", valid)

cleanup_stadium_data_for_training()

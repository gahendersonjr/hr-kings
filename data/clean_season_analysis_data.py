from __future__ import division
import csv
import os
from parse_weather_data import make_weather_dict
from clean_data_utils import RawInputs, RawInputDenominators, RawInputsInfo, write_to_file, get_normalization_denominator

def cleanup_stadium_data_for_training():
    clean_rows = []
    missing_data = {}
    for year in ["2018", "2019"]:
        with open("raw_data/batting_data/" + year + ".csv") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
              # In rare occasions some hits do not have hit coordinate values or games don't have weather data so they are excluded from training data
              if row[RawInputs.HC_Y.value] == "null" or row[RawInputs.HC_X.value] == "null":
                  if row[RawInputsInfo.PLAYER_NAME.value] not in missing_data.keys():
                      missing_data[row[RawInputsInfo.PLAYER_NAME.value]] = [0, 0]
                  if row[RawInputsInfo.RESULT.value] == "home_run" and "inside-the-park" not in row[RawInputsInfo.PLAY_DESCRIPTION.value]:
                      missing_data[row[RawInputsInfo.PLAYER_NAME.value]][0]+=1
                  else:
                      missing_data[row[RawInputsInfo.PLAYER_NAME.value]][1]+=1
                  continue
              clean_row = [float(row[i.value])/get_normalization_denominator(i) for i in RawInputs] + [70.0, 0.0, 0.0, 0.0, row[RawInputsInfo.PLAYER_NAME.value]]
              clean_rows.append(clean_row)
        write_to_file("clean_data/batting_data/" + year + ".csv", clean_rows)
        for name in missing_data.keys():
            print name + ": " + str(missing_data[name][0]) + " HRs, " + str(missing_data[name][1]) + " others"

cleanup_stadium_data_for_training()

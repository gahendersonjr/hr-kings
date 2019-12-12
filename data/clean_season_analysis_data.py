from __future__ import division
import csv
from clean_data_utils import RawInputs, RawInputDenominators, RawInputsInfo, write_to_file, get_normalization_denominator
import math

def cleanup_stadium_data_for_training():
    for year in ["2018", "2019"]:
        clean_rows = []
        with open("raw_data/batting_data/" + year + ".csv") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
              clean_row = [float(row[i.value])/get_normalization_denominator(i) for i in RawInputs]
              if row[RawInputsInfo.HC_Y.value] != "null" and row[RawInputsInfo.HC_X.value] != "null":
                  # converting hit coordinate to horizantal angle. i borrowed this guys technique https://github.com/BillPetti/Statcast-Modeling/blob/master/statcast.battedball.woba.R
                  horizontal_angle = math.tan((float(row[RawInputsInfo.HC_X.value])-128.0)/(208.0-float(row[RawInputsInfo.HC_Y.value])))*180.0/math.pi*.75
              # if no hc data available, use average from general direction in description
              elif "right center field" in row[RawInputsInfo.PLAY_DESCRIPTION.value].lower():
                  horizontal_angle = 18.0408820129
              elif "left center field" in row[RawInputsInfo.PLAY_DESCRIPTION.value].lower():
                  horizontal_angle = -18.9866998936
              elif "center field" in row[RawInputsInfo.PLAY_DESCRIPTION.value].lower():
                  horizontal_angle = -0.539864568793
              elif "left field" in row[RawInputsInfo.PLAY_DESCRIPTION.value].lower():
                  horizontal_angle = -28.7741302744
              elif "right field" in row[RawInputsInfo.PLAY_DESCRIPTION.value].lower():
                  horizontal_angle = 26.7126108734
              clean_row.append(horizontal_angle/90.0)
              clean_row = clean_row + [row[RawInputsInfo.PLAYER_NAME.value]]
              clean_rows.append(clean_row)
        write_to_file("clean_data/batting_data/" + year + ".csv", clean_rows)

cleanup_stadium_data_for_training()

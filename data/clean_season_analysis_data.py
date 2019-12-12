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
              # In rare occasions some hits do not have hit coordinate values or games don't have weather data so they are excluded from training data
              if row[RawInputsInfo.HC_Y.value] == "null" or row[RawInputsInfo.HC_X.value] == "null":
                  continue
              clean_row = [float(row[i.value])/get_normalization_denominator(i) for i in RawInputs]
              horizontal_angle = math.tan((float(row[RawInputsInfo.HC_X.value])-128.0)/(208.0-float(row[RawInputsInfo.HC_Y.value])))*180.0/math.pi*.75
              clean_row.append(horizontal_angle/90.0)
              clean_row = clean_row + [row[RawInputsInfo.PLAYER_NAME.value]]
              clean_rows.append(clean_row)
        write_to_file("clean_data/batting_data/" + year + ".csv", clean_rows)

cleanup_stadium_data_for_training()

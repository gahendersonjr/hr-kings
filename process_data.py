import csv
import numpy as np
from enum import Enum

class RawInputs(Enum):
    HC_X = 37
    HC_Y = 38
    HIT_DISTANCE = 52
    LAUNCH_SPEED = 53
    LAUNCH_ANGLE = 54
    ESTIMATED_BA = 69
    ESTIMATED_WOBA = 70
    LAUNCH_SPEED_ANGLE = 75

class Info(Enum):
    DATE = 1
    PLAYER_NAME = 5
    RESULT = 8
    PLAY_DESCRIPTION = 15

# TODO: after calling process_data, split into two arrays by classification.
#       then take proportionate number from each for training, testing and valid data.
#       then puth them together and shuffle.
def process_data(path):
    data = []
    classifications = []
    raw_input_indices = [i.value for i in RawInputs]
    total_cnt = 0
    missing_hc_cnt = 0
    with open(path) as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for row in reader:
            total_cnt +=1
            # In rare occasions some hits do not have hit coordinate values so they are excluded from training data
            if row[RawInputs.HC_Y.value] == "null" or row[RawInputs.HC_X.value] == "null":
                missing_hc_cnt += 1
                continue
            data.append([float(row[i]) for i in raw_input_indices])
            # Not counting inside the park home runs as they are rare and unpredictable from the data I am using.
            if row[Info.RESULT.value] == "home_run" and "inside-the-park" not in row[Info.PLAY_DESCRIPTION.value]:
                classifications.append(1)
            else:
                classifications.append(0)
        #TODO: when analyzing data on trained nets, figure out way to approximate hc_x and hc_y
        print str(missing_hc_cnt) + "/" + str(total_cnt) + " contain missing hit coordinate data and were ommitted."
    data = np.array(data)
    inputs = [np.reshape(x, (len(raw_input_indices), 1)) for x in data]
    classifications = np.array(classifications)
    classifications = [vectorized_result(y) for y in classifications]
    return zip(inputs, classifications)

def vectorized_result(result):
    results = np.zeros((2, 1))
    results[result] = 1.0
    return results

test = process_data("data/stadiums/coors_field_2016-2019.csv")

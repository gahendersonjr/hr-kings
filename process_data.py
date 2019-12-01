import csv
import numpy as np
from enum import Enum
from network2 import vectorized_result

class Info(Enum):
    DATE = 1
    PLAYER_NAME = 5
    RESULT = 8
    PLAY_DESCRIPTION = 15

class RawInputs(Enum):
    HC_X = 37
    HC_Y = 38
    HIT_DISTANCE = 52
    LAUNCH_SPEED = 53
    LAUNCH_ANGLE = 54
    # ESTIMATED_BA = 69 #TODO: it seems to get better results without estimated BA, experiment more with this
    ESTIMATED_WOBA = 70
    LAUNCH_SPEED_ANGLE = 75

class RawInputDenominators(Enum):
    HC_X = 248.0
    HC_Y = 207.46
    HIT_DISTANCE = 505.0
    LAUNCH_SPEED = 121.7
    LAUNCH_ANGLE = 72.5
    ESTIMATED_BA = 1.0
    ESTIMATED_WOBA = 2.016
    LAUNCH_SPEED_ANGLE = 6.0

# TODO: after calling process_data, split into two arrays by classification.
#       then take proportionate number from each for training, testing and valid data.
#       then puth them together and shuffle.
def process_data(path):
    data = []
    classifications = []
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
            data.append([float(row[i.value])/get_normalization_denominator(i) for i in RawInputs])
            # Not counting inside the park home runs as they are rare and unpredictable from the data I am using.
            if row[Info.RESULT.value] == "home_run" and "inside-the-park" not in row[Info.PLAY_DESCRIPTION.value]:
                classifications.append(1)
            else:
                classifications.append(0)
        #TODO: when analyzing data on trained nets, figure out way to approximate hc_x and hc_y
        print str(missing_hc_cnt) + "/" + str(total_cnt) + " contain missing hit coordinate data and were ommitted."
    data = np.array(data)
    inputs = [np.reshape(x, (len(RawInputs), 1)) for x in data]
    classifications = np.array(classifications)
    classifications = [vectorized_result(y) for y in classifications]
    return zip(inputs, classifications)

def get_normalization_denominator(raw_data_enum_name):
    name_as_string = str(raw_data_enum_name)
    enum_name = name_as_string[name_as_string.find('.')+1:]
    return RawInputDenominators[enum_name].value

from enum import Enum
import csv
import random

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

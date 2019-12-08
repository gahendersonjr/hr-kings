import os
from enum import Enum
import csv

class RawInputs(Enum):
    HC_X = 37
    HC_Y = 38
    LAUNCH_SPEED = 53
    LAUNCH_ANGLE = 54
    ESTIMATED_WOBA = 70
    LAUNCH_SPEED_ANGLE = 75

dict = {}

for i in RawInputs:
    dict[i] = 0.0

for filename in os.listdir("C:/Users/Alan/Desktop/finalproject/hr-kings/data/batting_stats"):
    with open("data/batting_stats/" + filename) as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for row in reader:
            for i in RawInputs:
                if row[i.value] != "null" and float(row[i.value]) > dict[i]:
                    dict[i] = float(row[i.value])

print dict

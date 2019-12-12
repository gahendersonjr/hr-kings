import glob
import os
import cPickle
from net_trainer import process_data
import csv
import numpy as np

def analyze_data_on_stadium(stadium):
    ann = load_ann("nets/" + stadium + ".pck")
    for file_path in glob.glob("data/clean_data/batting_data/*.csv"):
        hr_dict = {}
        year = os.path.splitext(os.path.basename(file_path))[0]
        yearly_data = process_data(file_path)
        for i in yearly_data:
            player = i[1]
            result = np.argmax(ann.feedforward(i[0]))
            if result==1:
                if player not in hr_dict.keys():
                    hr_dict[player] = 1
                else:
                    hr_dict[player] += 1
        display_leaders(hr_dict, year, stadium)

def display_leaders(hr_dict, year, stadium):
    hr_leaders = []
    for i in hr_dict.keys():
        hr_leaders.append([i, hr_dict[i]])
    hr_leaders = sorted(hr_leaders, key=lambda x: x[1], reverse=True)
    print "HR leaders in " + year + " if all games were played in " + stadium + " with normalized weather"
    print hr_leaders[0]
    print hr_leaders[1]
    print hr_leaders[2]
    print hr_leaders[3]
    print hr_leaders[4]

def process_data(file_path, vectorize=False):
    data = []
    players = []
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            players.append(row.pop())
            data.append(row + [70.0/113.0, 0.0, 0.0, 0.0])
    data = np.array(data, dtype=np.float64)
    data = [np.reshape(x, (8, 1)) for x in data]
    players = np.array(players)
    return zip(data, players)

def load_ann(path):
    with open(path, "rb") as file:
        ann = cPickle.load(file)
    return ann

analyze_data_on_stadium("COL")
# sort_batters(dict)

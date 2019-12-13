#!/usr/bin/python
import os
import numpy as np
import cPickle
import random
from math import sqrt
import time
import csv
from network2 import Network, vectorized_result

#this file trains all the stadium ANNs

ANN_DIMENSIONS = [8,6,4,2]
NUM_EPOCHS = 1000
MINI_BATCH_SIZE = 1
ETA = 0.01

def train_all_stadium_anns():
    for filename in os.listdir("data/clean_data/stadiums/train/"):
        train_ann(os.path.splitext(filename)[0])

def train_ann(team):
    train_data = process_data(team, "train", vectorize=True)
    test_data = process_data(team, "test")
    print team + "..."
    ann = Network(ANN_DIMENSIONS)
    start = time.time()
    ann.SGD(train_data, NUM_EPOCHS, MINI_BATCH_SIZE, ETA, evaluation_data=test_data)
    end = time.time()
    print "--------------------------"
    save(ann, team)

def save(ann, team):
    file = open("nets/" + team + ".pck","wb")
    cPickle.dump(ann, file)
    file.close()

def process_data(team, subpath, vectorize=False):
    data = []
    classifications = []
    with open("data/clean_data/stadiums/" + subpath + "/" + team + ".csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            classifications.append(row.pop())
            data.append(row)
    data = np.array(data, dtype=np.float64)
    data = [np.reshape(x, (8, 1)) for x in data]
    classifications = np.array(classifications, dtype=np.int32)
    if vectorize:
        classifications = [vectorized_result(y) for y in classifications]
    return zip(data, classifications)

if __name__== "__main__":
    train_all_stadium_anns()

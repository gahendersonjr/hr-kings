#!/usr/bin/python

import numpy as np
import cPickle
import random
from math import sqrt
import time
from process_data import process_data
from network2 import Network, vectorized_result

ANN_DIMENSIONS = [10,8,6,4,2]
NUM_EPOCHS = 100
MINI_BATCH_SIZE = 1
ETA = 0.1

def train_ann(data_path, save_to_path):
    train_data = process_data(data_path)
    print "Training ANN..."
    ann = Network(ANN_DIMENSIONS)
    start = time.time()
    ann.SGD(train_data, NUM_EPOCHS, MINI_BATCH_SIZE, ETA, evaluation_data=None, monitor_training_cost=True, monitor_training_accuracy=True)
    end = time.time()
    print "ANN trained with test data in " + str(end-start) + " seconds"
    save(ann, save_to_path)
    print "ANN saved to " + save_to_path

def save(ann, file_path):
    file = open(file_path,"wb")
    cPickle.dump(ann, file)
    file.close()

if __name__== "__main__":
    train_ann("data/stadiums/oakland_coliseum.csv", "nets/coliseum.pck") #TODO: make this accept one parameter and name the pickle file after the csv file

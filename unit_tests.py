import cPickle
import os
from network2 import Network, vectorized_result
from net_trainer import process_data

def test_anns():
    for filename in os.listdir("nets/"):
        ann = load_ann("nets/" + filename)
        valid_data = process_data(os.path.splitext(filename)[0], "valid")
        print "Testing " + filename + "....."
        test_ann(ann, valid_data)


def test_ann(ann, valid_data):
    print "    " + str(float(ann.accuracy(valid_data))/float(len(valid_data))*100.0) + "% accurate \n"

def load_ann(path):
    with open(path, "rb") as file:
        ann = cPickle.load(file)
    return ann

test_anns()

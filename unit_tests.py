import cPickle
import os
from network2 import Network, vectorized_result
from net_trainer import process_data

#My unit test simply runs all 23 of my ANNs against the validation set and produces the % correct.
def test_anns():
    for filename in os.listdir("nets/"):
        ann = load_ann("nets/" + filename)
        valid_data = process_data(os.path.splitext(filename)[0], "valid")
        print "Testing " + filename + "....."
        test_ann(ann, valid_data)


def test_ann(ann, valid_data):
    correct = ann.accuracy(valid_data)
    n = len(valid_data)
    print "    " + str(correct) + " / " + str(n) + " (" + str(round(float(correct)/float(n), 2)) + ")"
    print "------------------------------------"
def load_ann(path):
    with open(path, "rb") as file:
        ann = cPickle.load(file)
    return ann

test_anns()

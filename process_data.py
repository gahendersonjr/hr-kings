import csv
import numpy as np

# TODO: after calling process_data, split into two arrays by classification.
#       then take proportionate number from each for training, testing and valid data.
#       then puth them together and shuffle.
def process_data(path):
    data = []
    classifications = []
    with open(path) as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            # the first three columns are not going to be fed into the NN because
            # they include data used for classification.
            data.append(row[4:])
            # inside the park home runs are a rare occurence and are not predictable
            # by the metrics I am using so I don't include them.
            # my goal is to track home runs that left the ballpark.
            if row[2] == "home_run" and "inside-the-park" not in row[3]:
                classifications.append(1)
            else:
                classifications.append(0)
        data = np.array(data)
        inputs = [np.reshape(x, (6, 1)) for x in data]
        classifications = np.array(classifications)
        return zip(inputs, classifications)

process_data("coors/coors_field_16-19_clean.csv")

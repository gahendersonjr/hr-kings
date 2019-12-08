import httplib
import os
import csv
import time

# To run this, you will need to register for an api key through sportradar.
# The trial key allows you to make 1000 calls, which is sufficient for this project.
API_KEY = "" # copy api key here
DATE_INDEX = 1
dict = {}

def get_all_daily_box_scores_json_files():
    #populate dict with already collected data to reduce calls since limited api calls are allowed with trial api key
    for filename in os.listdir("C:/Users/Alan/Desktop/finalproject/hr-kings/data/box_scores/"):
        dict[os.path.splitext(filename)[0]] = True
    print str(len(dict)) + " daily box scores previously collected."
    #iterate through batting stats data and save all json for dates not already collected
    for filename in os.listdir("C:/Users/Alan/Desktop/finalproject/hr-kings/data/batting_stats/"):
        with open("data/batting_stats/" + filename) as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
                if row[DATE_INDEX] not in dict:
                    get_daily_box_scores_json_file(row[DATE_INDEX])
    print "All daily box scores collected succesfully"

def get_daily_box_scores_json_file(date):
    time.sleep(1.1) #trial api has limit of 1 call per second, sleeping for 1.1 seconds to be safe
    try:
        conn = httplib.HTTPSConnection("api.sportradar.us")
        url = "/mlb/trial/v6.6/en/games/" + date.replace("-", "/") + "/boxscore.json?api_key=" + API_KEY
        conn.request("GET", url)
        res = conn.getresponse()
        with open('C:/Users/Alan/Desktop/finalproject/hr-kings/data/box_scores/' + date + '.json', 'w') as outfile:
            outfile.write(res.read())
        dict[date] = True
        print str(len(dict)) + " daily box scores collected."
    except Exception:
        print "http request for " + date + " threw exception."

get_all_daily_box_scores_json_files()

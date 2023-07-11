import csv
import json
import pandas as pd
import logging
from pathlib import Path
from validation import connection_validator
import os

class RunList:
    jsonfile = 'data/quotes.json'
    def __init__(self, parent, csv_location, log_location):
        self.parent = parent
        self.csv_location = csv_location

    def runit(self):
        if self.csv_location.startswith("http://") or \
            self.csv_location.startswith("https://"):
            working_csv = os.path.join(self.parent,'data/cached.csv')
            if connection_validator(self.csv_location) == 200:
                df = pd.read_csv(self.csv_location)
                df.to_csv(working_csv,index=False,header=True)
            else:
                logging.info("""Issue connecting to CSV URL: {}. Falling back by default
                to cached CSV file if it exists.""".\
                    format(connection_validator(self.csv_location)))
            with open(working_csv, 'r') as c:
                reader = csv.DictReader(c)
                json_list = []
                for row in reader:
                    json_list.append(row)
#TODO: add error handling so it falls back to cached file in event webpage is down

        else:
            working_csv = self.csv_location
         
            with open(working_csv, 'r') as c:
                reader = csv.DictReader(c)
                json_list = []
                for row in reader:
                    json_list.append(row)

        working_json = os.path.join(self.parent, self.jsonfile)
        file = open(working_json, 'w')
        file.write(json.dumps(json_list, indent=4))
        file.close

if __name__ == "__main__":
    RunList('/home/jason/python/twitterbot/', '/home/jason/quotes.csv','data/twitterbot.log').runit()

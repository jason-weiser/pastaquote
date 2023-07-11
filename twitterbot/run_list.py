import csv
import json
import pandas
from pathlib import Path
import os

class RunList:
    jsonfile = 'data/quotes.json'
    def __init__(self, parent, csv_location):
        self.parent = parent
        self.csv_location = csv_location

    def runit(self):
        if self.csv_location.startswith("http://") or \
            self.csv_location.startswith("https://"):
            working_csv = pandas.read(self.csv_location)
        else:
            working_csv = self.csv_location
        
        working_json = os.path.join(self.parent, self.jsonfile)
        with open(working_csv, 'r') as c:
            reader = csv.DictReader(c)

            json_list = []
            for row in reader:
                json_list.append(row)

        file = open(working_json, 'w')
        file.write(json.dumps(json_list, indent=4))
        file.close

if __name__ == "__main__":
    RunList('/home/jason/python/twitterbot/', '/home/jason/quotes.csv').runit()

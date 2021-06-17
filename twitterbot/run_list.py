import csv
import json
from pathlib import Path
import os

class RunList:
    csvfile = 'data/quotes.csv'
    jsonfile = 'data/quotes.json'

    def __init__(self, parent):
        self.parent = parent

    def runit(self):
        working_csv = os.path.join(self.parent, self.csvfile)
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
    runlist = RunList('/home/jason/python/twitterbot/')
    runlist.runit()
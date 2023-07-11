import csv
import json
import codecs
from urllib.request import urlopen
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
            response = urlopen(self.csv_location)
            working_csv = csv.reader(codecs.iterdecode(response, "utf-8"))
            json_list = []
            for row in working_csv:
                json_list.append(row)

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
    RunList('/home/jason/python/twitterbot/', 'https://assets.jasonweiser.com/files/data/dune_quotes.csv').runit()

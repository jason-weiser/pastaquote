import csv
import json

class RunList:
    csvfile = 'files/quotes.csv'
    jsonfile = 'files/quotes.json'

    def runit(self):
        with open(self.csvfile, encoding='utf-8') as c:
            reader = csv.DictReader(c)

            json_list = []
            for row in reader:
                json_list.append(row)

        file = open(self.jsonfile, 'w', encoding="UTF-8")
        file.write(json.dumps(json_list))
        file.close

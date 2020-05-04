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

#with open(jsonfile, 'w') as j:
#    json.dumps(rows)

#finally:
#    c_file.close()
#    j_file.close()

#with open(jsonfile, 'r') as f:
#    data = f.read().replace('\n','')
#    j_out = json.loads(str('data'))

#   print(data)

runlist = RunList()
runlist.runit()

number = 2
with open('files/quotes.json') as json_file:
    data = json.load(json_file)
    print(f"{data[number]['quote']}\n--{data[number]['author']}")

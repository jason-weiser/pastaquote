import csv

file = 'files/quotes.csv'
#open the csv file
f = open(file, 'rt')
number = 1

try:
    reader = csv.reader(f)
#    row = reader[number]
#    print(row)
    list = []
    for row in reader:
        list.append(row)
    print(f"{list[number][0]}\n--{list[number][1]}")

finally:
    f.close()

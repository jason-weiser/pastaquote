import csv
import json
import pandas as pd
import logging
from pathlib import Path
from useful_resources import connection_validator
from useful_resources import log_this
from useful_resources import pull_config
import os

class RunList:
    jsonfile = 'data/quotes.json'
    def __init__(self, parent, csv_location):
        self.parent = parent
        self.csv_location = csv_location

    def validate_char(self, platform, text_row):
        text_row = text_row['quote']
        if len(text_row) > pull_config(platform)["CHARACTER_LIMIT"] \
            and pull_config(platform)["ENABLE_PLATFORM"]:
            warning = "\"{}\"\nExceeds the character limit of {} set for {} by {}".format(\
                text_row,pull_config(platform)["CHARACTER_LIMIT"],platform,\
                    len(text_row) - pull_config(platform)["CHARACTER_LIMIT"])
            log_this(warning)
            print(warning)
            return 1
        else:
            return 0

    def csv_to_json(self, csv_list):
        total_exceeded = 0
        with open(csv_list, 'r') as c:
            reader = csv.DictReader(c)
            working_json_list = []
            for row in reader:
                working_json_list.append(row)
                total_exceeded += self.validate_char("TWITTER",row)
                total_exceeded += self.validate_char("MASTODON",row)
        if total_exceeded > 0:
            exceeded_msg = """{} posts/tweets exceeded the pre-defined character limit.
They were still processed. No action has been taken.
Please see the log for further details.""".format(total_exceeded)
            print(exceeded_msg)
            log_this(exceeded_msg)
        return working_json_list

    def runit(self):
        if self.csv_location.startswith("http://") or \
            self.csv_location.startswith("https://"):
            working_csv = os.path.join(self.parent,'data/cached.csv')
            if connection_validator(self.csv_location) == 200:
                df = pd.read_csv(self.csv_location)
                df.to_csv(working_csv,index=False,header=True)
            else:
                log_this("""Issue connecting to CSV URL: {}. Falling back by default
                to cached CSV file if it exists.""".\
                    format(connection_validator(self.csv_location)))
            json_list = self.csv_to_json(working_csv)
        else:
            working_csv = self.csv_location 
            json_list = self.csv_to_json(working_csv)

        working_json = os.path.join(self.parent, self.jsonfile)
        file = open(working_json, 'w')
        file.write(json.dumps(json_list, indent=4))
        file.close

if __name__ == "__main__":
    runThatList = RunList("/home/jason/python/twitterbot/","/home/jason/quotes.csv")
    runThatList.runit()

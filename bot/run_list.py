import json
import urllib.request
import logging
import urllib.request
from pathlib import Path
from useful_resources import connection_validator
from useful_resources import log_this
from useful_resources import pull_config
import os

class RunList:
    jsonfile = 'data/quotes.json'
    def __init__(self, parent, list_location):
        self.parent = parent
        self.list_location = list_location

    def validate_char(self, platform, text_row):
        if len(text_row) > pull_config(platform)["CHARACTER_LIMIT"] \
            and pull_config(platform)["ENABLE_PLATFORM"]:
            warning = "\"{}\"\nExceeds the character limit of {} set for {} by {}".format(\
                text_row,pull_config(platform)["CHARACTER_LIMIT"],platform,\
                    len(text_row) - pull_config(platform)["CHARACTER_LIMIT"])
            log_this(warning)
            return 1
        else:
            return 0

    def list_to_json(self, post_list):
        total_exceeded = 0
        with open(post_list, 'r') as c:
            working_json_list = []
            for row in c:
                working_json_list.append(row.strip('\n'))
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
        if self.list_location.startswith("http://") or \
            self.list_location.startswith("https://"):
            working_list = os.path.join(self.parent,'data/cached.txt')
            if connection_validator(self.list_location) == 200:
                with open(working_list, 'w') as f:
                    for line in urllib.request.urlopen(self.list_location):
                        f.write(line.decode('utf-8'))
            else:
                log_this("""Issue connecting to list URL: {}. Falling back by default
                to cached list file if it exists.""".\
                    format(connection_validator(self.list_location)))
            json_list = self.list_to_json(working_list)
        else:
            working_list = self.list_location 
            json_list = self.list_to_json(working_list)

        working_json = os.path.join(self.parent, self.jsonfile)
        file = open(working_json, 'w')
        file.write(json.dumps(json_list, indent=4))
        file.close

if __name__ == "__main__":
    pass

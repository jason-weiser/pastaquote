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
    jsonfile = '../data/quotes.json'
    def __init__(self, list_location):
        self.list_location = list_location
        self.cached_list = '../data/cached.txt'

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
                working_json_list.append(row.rstrip('\n'))
                total_exceeded += self.validate_char("TWITTER",row)
                total_exceeded += self.validate_char("MASTODON",row)
        if total_exceeded > 0:
            exceeded_msg = """{} posts/tweets exceeded the pre-defined character limit.
They were still processed. No action has been taken.
Please see the log for further details.""".format(total_exceeded)
            print(exceeded_msg)
            log_this(exceeded_msg)
        return working_json_list

    def write_to_cache(self,input_list,cache_list):
        if input_list.startswith("http://") or \
            input_list.startswith("https://"):
            working_list = self.cached_list
            if connection_validator(self.list_location) == 200:
                with open(working_list, 'w') as f:
                    for line in urllib.request.urlopen(self.list_location):
                        f.write(line.decode('utf-8'))
                return True
            elif connection_validator(self.list_location) != 200:
                return False
        else:
            with open(input_list) as immutable_list:
                with open(cache_list, 'w') as to_cache:
                    for item in immutable_list:
                        to_cache.write(item)
            return True

    def txt_to_list(self, input_txt):
        output_list = []
        if input_txt.startswith("http://") or\
             input_txt.startswith("https://"):
            for line in urllib.request.urlopen(input_txt):
                output_list.append((line.decode('utf-8')).rstrip('\n'))
        else:
            with open(input_txt, 'r') as working1: 
                for i in working1:
                    output_list.append(i.rstrip('\n'))
        return output_list

    def compare_return_diff(self, f1, f2):
        list1 = self.txt_to_list(f1)
        list2 = self.txt_to_list(f2)
        difference = set(list2).difference(set(list1))
        return difference

    def append_json(self, auto):
        log_this("'--add' option run")
        json_list = self.jsonfile
        lines_to_add = self.compare_return_diff(self.cached_list,self.list_location)
        if auto:
            approve_each_addition = "n"
        else:
            approve_each_addition = input("Would you like to approve each addition (y/n)? ")
        with open(json_list,"r") as j:
            data = json.load(j)
            working_data = data[:]
            for i in lines_to_add:
                if i in working_data:
                    pass
                else:
                    if approve_each_addition.lower() == "y" or \
                        approve_each_addition.lower() == "yes":
                        approve_item = input("Add: {}\n(y/n): ".format(i))
                        if approve_item.lower() == "y" or \
                        approve_item.lower() == "yes":
                            working_data.append(i)
                            log_this("{} added to list with '--add'".format(i))
                        else:
                            pass
                    else:
                        working_data.append(i)
                        log_this("{} added to list with '--add'".format(i))
        with open((json_list), "w") as f:
            json.dump(working_data, f, indent=4)
        self.write_to_cache(self.list_location,self.cached_list)

    def runit(self):
        if self.write_to_cache(self.list_location, self.cached_list):
            msg = "List successfully pulled from {} and added to cache".\
                format(self.list_location)
            print(msg)
            log_this(msg)
        else:
            msg = """Issue finding list: {}. Falling back by default
to cached list file if it exists.""".\
                    format(connection_validator(self.list_location))
            print(msg)
            log_this(msg)
            json_list = self.list_to_json(working_list)
        working_list = self.cached_list
        json_list = self.list_to_json(working_list)
            
        file = open(self.jsonfile, 'w')
        file.write(json.dumps(json_list, indent=4))
        file.close

if __name__ == "__main__":
    pass


##TODO: add remove \n or [:-3] back to one of the places to stop it from adding a \n
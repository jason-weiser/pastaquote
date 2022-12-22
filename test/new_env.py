import json

with open('/home/jason/python/twitterbot/test/test.json','r') as settings_json_file:
    settings = json.load(settings_json_file)
    print(settings['mode'])
    if settings['mode'] == 'random':
        print("Oh so random")
import json


json_path = './test.json'
json_file = open(json_path, 'r')
json_dict = json.load(json_file)

print(json_dict)
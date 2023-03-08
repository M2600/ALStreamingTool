import json

json_path = './test.json'

try:
    jsonDic = json.load(open(json_path, 'r'))
except json.decoder.JSONDecodeError as e:
    print(e.msg)
    if e.msg == "Expecting ',' delimiter":
        print('error message matched')
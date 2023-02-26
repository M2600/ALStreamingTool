import json


json_path = './test.json'

LastData = []


def get_json_data(jsonPath):
    with open(jsonPath, 'r', encoding = 'UTF-8') as f:
        textData = f.read()
        # ApexLegends outputs INVALID JSON data when the match is still running.
        try:
            jsonDict = json.loads(textData)
        except json.decoder.JSONDecodeError as e:
            # The match is still running.
            print(e.msg)
            if e.msg == 'Expecting value':
                # Remove last comma, spaces and newlines and add a closing bracket.
                jsonDict = json.loads(textData.rstrip()[:-1]+']') 
        else:
            # The match has finished.
            print('Valid JSON file')
        
        print('Length of JSON dict: '+str(len(jsonDict)))
        #print(jsonDict)
        return jsonDict
    
def get_new_elements(jsonDict):
    global LastData
    if not LastData:
        LastData = jsonDict
        return jsonDict
    else:
        NewData = []
        for i in jsonDict:
            if i not in LastData:
                NewData.append(i)
        LastData = jsonDict
        return NewData



if __name__ == '__main__':
    print(get_new_elements(get_json_data(json_path)))
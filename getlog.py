import datetime
from zoneinfo import ZoneInfo
import json
import glob, getpass


json_path = './test.json'

LastData = []
PlayerData = []

outputAllEvents = True
matchRunning = False


def epoch_to_datetime(epoch):
    return datetime.datetime.fromtimestamp(epoch, tz=ZoneInfo('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')

def get_json_path():
    #print('def get_json_path()')
    basePath = "C:\\Users\\"+getpass.getuser()+"\\Saved Games\\Respawn\\Apex\\assets\\temp\\live_api"
    jsonPathes = glob.glob(basePath + "\\*")
    print('Found '+str(len(jsonPathes))+(' JSON files.' if len(jsonPathes) > 1 else ' JSON file.'))
    print(jsonPathes)
    for p in jsonPathes:
        with open(p, 'r', encoding='UTF-8') as f:
            textData = f.read()
            try:
                jsonDict = json.loads(textData)
            except json.decoder.JSONDecodeError as e:
                # The match is still running.
                if e.msg == 'Expecting value':
                    # Remove last comma, spaces and newlines and add a closing bracket.
                    print('Found JSON file with running match: "'+p+'"')
                    global matchRunning
                    matchRunning = True
                    return p
            else:
                # The match has finished.
                print('Valid JSON file')
    print ('No JSON file with running match found.')
    return None


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
            global matchRunning
            matchRunning = False
        
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
    
def newMatch_init():
    print('def newMatch_init()')
    global PlayerData
    global LastData
    PlayerData = []
    LastData = []


def process_event(event):
    
    # Server events
    if event['category'] == 'init':
        print('['+epoch_to_datetime(event['timestamp'])+'][Init]: [GameVersion: '+event['gameVersion']+']') if outputAllEvents else None
        


    # Observer events
    elif event['category'] == 'observerSwitched':
        print('['+epoch_to_datetime(event['timestamp'])+'][Observerswitched]: [Observer: '+event['observer']['name']+'], [TargetPlayer: '+event['target']['name']+'], [TargetTeamId: '+str(event['target']['teamId'])+'], [TargetTeamName: '+event['target']['teamName']+']') if outputAllEvents else None
        


    # Match Informations
    elif event['category'] == 'matchSetup':
        print('['+epoch_to_datetime(event['timestamp'])+'][MatchSetup]: [Map: '+event['map']+']'+', [PlaylistName: '+event['playlistName']+']'+', [PlayistDesc: '+event['playlistDesc']+']'+', [AimAssistOn: '+str(event['aimAssistOn'])+']'+', [ServerId: '+event['serverId']+']'+', [AnonymousMode: '+str(event['anonymousMode'])+']') if outputAllEvents else None

    elif event['category'] == 'gameStateChanged':
        print('['+epoch_to_datetime(event['timestamp'])+'][GameStateChanged]: [State: '+event['state']+']') if outputAllEvents else None

    elif event['category'] == 'characterSelected':
        print('['+epoch_to_datetime(event['timestamp'])+'][CharacterSelected]: [Player: '+event['player']['name']+']'+', [Character: '+event['player']['character']+']') if outputAllEvents else None

    elif event['category'] == 'matchStateEnd':#
        print('['+epoch_to_datetime(event['timestamp'])+'][MatchStateEnd]: [Winners: '+event['winners'][0]['name']+', '+event['winners'][1]['name']+', '+event['winners'][2]['name']+']') if outputAllEvents else None

    elif event['category'] == 'ringStartClosing':#
        print('['+epoch_to_datetime(event['timestamp'])+'][RingStartClosing]: [stage: '+str(event['stage'])+']') if outputAllEvents else None

    elif event['category'] == 'ringFinishedClosing':#
        print('['+epoch_to_datetime(event['timestamp'])+'][RingFinishedClosing]: [stage: '+str(event['stage'])+']') if outputAllEvents else None

    elif event['category'] == 'playerConnected':
        print('['+epoch_to_datetime(event['timestamp'])+'][PlayerConnected]: [Player: '+event['player']['name']+']') if outputAllEvents else None

    elif event['category'] == 'playerDisconnected':
        print('['+epoch_to_datetime(event['timestamp'])+'][PlayerDisconnected]: [Player: '+event['player']['name']+']') if outputAllEvents else None

    elif event['category'] == 'playerStatChanged':#
        print('['+epoch_to_datetime(event['timestamp'])+'][PlayerStatChanged]: [Player: '+event['player']['name']+']'+', [StatName: '+event['statName']+']'+', [NewValue: '+str(event['newValue'])+']') if outputAllEvents else None

    

    # Combat Events
    elif event['category'] == 'playerDamaged':#
        pass
    elif event['category'] == 'playerKilled':#
        pass
    elif event['category'] == 'playerDowned':#
        pass
    elif event['category'] == 'playerAssist':#
        pass
    elif event['category'] == 'squadEliminated':#
        pass
    elif event['category'] == 'gibraltarShieldAbsorbed':#
        pass

    # Interaction Events
    elif event['category'] == 'playerRespawnTeam':
        pass
    elif event['category'] == 'playerRevive':
        pass
    elif event['category'] == 'inventoryPickUp':
        pass
    elif event['category'] == 'inventoryDrop':
        pass
    elif event['category'] == 'inventoryUse':
        pass
    elif event['category'] == 'bannerCollected':
        pass
    elif event['category'] == 'playerAbilityUsed':
        pass
    elif event['category'] == 'ziplineUsed':
        pass
    elif event['category'] == 'grenadeThrown':
        pass
    elif event['category'] == 'blackMarketAction':
        pass
    elif event['category'] == 'wraithPortal':
        pass
    elif event['category'] == 'ammoUsed':
        pass
    elif event['category'] == 'weaponSwitched':
        pass


def main():
    
    global json_path
    if matchRunning:
        jsonDic = get_json_data(json_path)
        newElements = get_new_elements(jsonDic)
        for e in newElements:
            process_event(e)
    else:
        json_path = get_json_path()
        newMatch_init()

def forDebug():
    jsonDic = get_json_data(json_path)
    for e in jsonDic:
        process_event(e)


if __name__ == '__main__':
    pass

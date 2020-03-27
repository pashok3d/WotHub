import json
import pandas as pd
from meta_data import vehicles_data
import os

def find_packet_index(lst, key, value):
    indices = []
    for i, dic in enumerate(lst):
        if dic[key] == value:
            indices.append(i)
    return indices

def nation_to_column(data):
    vehicle = data['vehicle'].split(':')
    return vehicle[0]

def vehicle_name_to_column(data):
    vehicle = data['vehicle'].split(':')
    vehicle_id = vehicle[1]
    return vehicles_data[vehicle_id]['short_name']

def tier_to_column(data):
    vehicle = data['vehicle'].split(':')
    vehicle_id = vehicle[1]
    return vehicles_data[vehicle_id]['tier']

def type_to_column(data):
    vehicle = data['vehicle'].split(':')
    vehicle_id = vehicle[1]
    return vehicles_data[vehicle_id]['type']

def position_to_column(data, index):
    positions = data['position']
    position = float(positions[index])
    return position

def preprocess(data): 
    #packets cleaning
    packets = data['packets']   
    packets_10_index = find_packet_index(packets, 'type', 10)
    packets_10 = [packets[i] for i in packets_10_index]
    packets = pd.DataFrame(packets_10) #keep only type 10 packets
    packets = packets.dropna()
    packets = packets.astype({'clock': 'int32'})
    packets.drop_duplicates(subset = ['clock','player_id'], keep = 'last', inplace = True) #keep only one position per second
    packets['x'] = packets.apply(lambda x: position_to_column(x,0), axis=1)
    packets['y'] = packets.apply(lambda x: position_to_column(x,1), axis=1)
    packets['z'] = packets.apply(lambda x: position_to_column(x,2), axis=1)
    packets = packets.drop(columns = ['type','position','team'])
    
    #map
    packets['map_name'] = data['map']
    
    #summary
    packets['client_version'] = data['summary']['clientVersionFromExe'] 
    packets['battle_type'] = data['summary']['battleType']
    
    #vehicles
    vehicles = data['summary']['vehicles']
    vehicles = pd.DataFrame.from_dict(vehicles, orient = 'index')
    vehicles = vehicles[['avatarSessionID','name','team','vehicleType']]
    vehicles = vehicles.rename({'avatarSessionID':'player_id','name':'nickname','vehicleType':'vehicle'}, axis = 1)
    vehicles = vehicles.astype({'player_id': 'int64'})
    packets = packets.merge(vehicles)
    
    #score_card
    results = data['score_card'][0] 
    packets['arena_id'] = results['arenaUniqueID'] 
    packets['winner_team'] = results['common']['winnerTeam'] 
    
    #vehicles_data
    packets['nation'] = packets.apply(nation_to_column, axis=1)
    packets['vehicle_name'] = packets.apply(vehicle_name_to_column, axis=1)
    packets['tier'] = packets.apply(tier_to_column, axis=1)
    packets['type'] = packets.apply(type_to_column, axis=1)
    packets = packets.drop('vehicle', axis = 1)

    return packets.reset_index(drop=True)

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    raw_data_path = os.path.join(dir_path,'raw_data')
    pro_data_path = os.path.join(dir_path,'pro_data')
    
    files = []
    print('Loading files...', end='\r')
    for r, d, f in os.walk(raw_data_path):
        for file in f:
            if '.json' in file:
                files.append(file)

    files_count = len(files)

    for count, file_name in enumerate(files):
        print(str(count) + '/' + str(files_count) + ' files preprocessed.', end='\r')
        file_path = os.path.join(raw_data_path,file_name)
        file_desc = open(file_path, encoding="utf8")
        data = json.load(file_desc)

        try:
            processed_data = preprocess(data)
        except:
            print('Failed to process file.', end='\r')
            continue  

        file_name = processed_data['map_name'][0] + '.csv'
        file_path = os.path.join(pro_data_path,file_name)

        if os.path.isfile(file_path):
            processed_data = processed_data.append(pd.read_csv(file_path), ignore_index = True)

        processed_data.to_csv(file_path, index = False)
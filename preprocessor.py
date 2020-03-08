import json
import pandas as pd
import os

def find_packet_index(lst, key, value):
    indices = []
    for i, dic in enumerate(lst):
        if dic[key] == value:
            indices.append(i)
    return indices

def position_to_column(data, index):
    positions = data['position']
    position = float(positions[index])
    return position

def feature_to_column(data,vehicles_dict,feature):
    player_id = str(int(data['player_id']))
    return vehicles_dict[player_id][feature]

def main(file_name):
    
    file_path = os.path.join(raw_data_path,file_name)
    file = open(file_path, encoding="utf8")
    data = json.load(file)
    
    #packets 
    packets = data['packets']
    packets_10_index = find_packet_index(packets, 'type', 10)
    packets_10 = [packets[i] for i in packets_10_index]
    #what if first create pandas dataframe and then cut
    packets = pd.DataFrame(packets_10)
    
    packets = packets.dropna()
    packets = packets.astype({'clock': 'int32'})
    packets.drop_duplicates(subset = ['clock','player_id'],keep = 'last', inplace = True) 
    
    packets['x'] = packets.apply(lambda x: position_to_column(x,0), axis=1)
    packets['y'] = packets.apply(lambda x: position_to_column(x,1), axis=1)
    packets['z'] = packets.apply(lambda x: position_to_column(x,2), axis=1)
    
    packets = packets.drop(columns = ['type','position','team'])
    #packets.drop_duplicates(keep = 'first', inplace = True) 
    
    #summary
    packets['map_name'] = data['map']
    packets['client_version'] = data['summary']['clientVersionFromExe'] 
    packets['battle_type'] = data['summary']['battleType']
        #vehicles
    vehicles = data['summary']['vehicles']
    
    vehicles_dict = {}
    
    for vehicle in vehicles:
        vehicle_dict = {	
            "id" : vehicles[vehicle]['avatarSessionID'],
    		"nickname" : vehicles[vehicle]['name'],
    		"team" : vehicles[vehicle]['team'],
    		"vehicle" : vehicles[vehicle]['vehicleType']
    	}
        vehicles_dict[vehicle_dict['id']] = vehicle_dict
    
    #score_card
    results = data['score_card'][0] 
    
    packets['arena_id'] = results['arenaUniqueID'] 
    packets['winner_team'] = results['common']['winnerTeam'] 
    
    vehicles_results = results['vehicles']
    for player in vehicles_results:
        vehicles_dict[player]['global_id'] = vehicles_results[player][0]['accountDBID']
        vehicles_dict[player]['credits'] = vehicles_results[player][0]['credits']
        vehicles_dict[player]['life_time'] = vehicles_results[player][0]['lifeTime']
        vehicles_dict[player]['shots'] = vehicles_results[player][0]['shots']
        vehicles_dict[player]['spotted'] = vehicles_results[player][0]['spotted']
        vehicles_dict[player]['kills'] = vehicles_results[player][0]['kills']
        vehicles_dict[player]['spotted'] = vehicles_results[player][0]['spotted']
        vehicles_dict[player]['mileage'] = vehicles_results[player][0]['mileage']
        vehicles_dict[player]['piercings'] = vehicles_results[player][0]['piercings']
        vehicles_dict[player]['xp'] = vehicles_results[player][0]['xp']
        vehicles_dict[player]['death_reason'] = vehicles_results[player][0]['deathReason']
    
    frags = data['score_card'][2]
    for player in frags:
        vehicles_dict[player]['frags'] = frags[player]['frags']
        
    #adding data to packets
    features_to_add = ['global_id','nickname','team','vehicle']
    for feature in features_to_add:
      packets[feature] = packets.apply(lambda x: feature_to_column(x,vehicles_dict,feature), axis=1)  
      
    file_name = file_name[:-5]
    file_path_save = os.path.join(pro_data_path,file_name)
    packets.to_csv(file_path_save + '.csv', index=False)
    

if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    raw_data_path = os.path.join(dir_path,'raw_data')
    pro_data_path = os.path.join(dir_path,'pro_data')
    
    files = []
    for r, d, f in os.walk(raw_data_path):
            for file in f:
                if '.json' in file:
                    files.append(file)
            
    for file in files:
        main(file)



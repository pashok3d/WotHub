import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def find_packet_index(lst, key, value):
    indices = []
    for i, dic in enumerate(lst):
        if dic[key] == value:
            indices.append(i)
    return indices

def positions_to_column(data):
    positions = data['position']
    x = float(positions[0])
    y = float(positions[1])
    z = float(positions[2])
    return [x,y,z]

def feature_to_column(data,vehicles_dict,feature):
    player_id = str(int(data['player_id']))
    return vehicles_dict[player_id][feature]

file = open('data.json', encoding="utf8")
data = json.load(file)

#packets 
packets = data['packets']
packets_10_index = find_packet_index(packets, 'type', 10)
packets_10 = [packets[i] for i in packets_10_index]
#whet if first create pandas dataframe and then cut
packets = pd.DataFrame(packets_10)

packets = packets.dropna()
packets = packets.astype({'clock': 'int32'})
packets.drop_duplicates(subset = ['clock','player_id'],keep = 'last', inplace = True) 

positions = packets.apply(positions_to_column,axis=1,result_type='expand')

packets['x'] = positions[0]
packets['y'] = positions[1]
packets['z'] = positions[2]

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
  

'''    
battle_data = [vehicles_dict[player] for player in vehicles_dict]
battle_data = pd.DataFrame(battle_data)
battle_data['arena_id'] = results['arenaUniqueID'] 
battle_data['winner_team'] = results['common']['winnerTeam'] 
battle_data['finish_reason'] = results['common']['finishReason'] 
battle_data['duration'] = results['common']['duration'] 
'''


pos = packets.loc[:,['x','z']].to_numpy()
team = packets.loc[:,'team'].to_numpy()

plt.scatter(pos[team == 1, 0], pos[team == 1, 1], s = 2, c = 'green')
plt.scatter(pos[team == 2, 0], pos[team == 2, 1], s = 2, c = 'red')
plt.xlim([-500, 500])
plt.ylim([-500, 500])
plt.xlabel('X')
plt.ylabel('Y')
plt.show()





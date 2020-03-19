import os
dir_path = os.path.dirname(os.path.realpath(__file__))
replays_path = os.path.join(dir_path,'replays')

replays = []
for r, d, f in os.walk(replays_path):
        for file in f:
            if '.wotreplay' in file:
                replays.append(file)
    
replays_count = len(replays)

for count, replay in enumerate(replays):
    output_name = replay[:-len('.wotreplay')] + '.json'
    path = 'wotreplay-parser.exe --parse --root ./ --type json --input ./replays/' + replay + ' --output ./raw_data/' + output_name 
    os.system(path)
    print(str(count) + '/' + str(replays_count) + ' files preprocessed.', end='\r')

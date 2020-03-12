import os
dir_path = os.path.dirname(os.path.realpath(__file__))
replays_path = os.path.join(dir_path,'replays')

replays = []
for r, d, f in os.walk(replays_path):
        for file in f:
            if '.wotreplay' in file:
                replays.append(file)

for replay in replays:
    output_name = replay[:-len('.wotreplay')] + '.json'
    path = 'wotreplay-parser.exe --parse --root ./ --type json --input ./replays/' + replay + ' --output ./raw_data/' + output_name 
    os.system(path)

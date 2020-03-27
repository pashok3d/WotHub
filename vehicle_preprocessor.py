import json
import pandas as pd

file_path = r'C:\Users\pavel\Documents\GitHub\WotHub\vehicles\vehicles_data.json'
file_desc = open(file_path, encoding="utf8")
json_data = json.load(file_desc)
data = pd.DataFrame(json_data)
data = data.loc[:,['id','short_name','tier','type']]
data = data.set_index('id')
data_dict = data.to_dict(orient='index')
f = open("vehicles.txt","w")
f.write(str(data_dict))
f.close()

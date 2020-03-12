import pandas as pd
import s3fs

df = pd.read_csv('https://wothub-data.s3.amazonaws.com/15839426139299_france_F116_Bat_Chatillon_Bourrasque_malinovka.csv')

df.head()
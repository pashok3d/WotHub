import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from meta_data import map_names, maps_data, vehicle_types, vehicle_types_data
from matplotlib.colors import Normalize
import scipy.stats as stat
import s3fs
from PIL import Image

def density(data, bandwidth, bins = 50j):
    x = data['x']
    y = data['z']
        
    #TO-DO: getting size from data
    xmin = -500.0
    xmax = 500.0
    ymin = -500.0
    ymax = 500.0
    
    X, Y = np.mgrid[xmin:xmax:bins, ymin:ymax:bins]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    try:
        kernel = stat.gaussian_kde(values)
        kernel.set_bandwidth(bw_method=kernel.factor / bandwidth)
        Z = np.reshape(kernel(positions).T, X.shape)
    except:
        return None

    Z = np.rot90(Z)
    vmax = np.abs(Z).max()
    vmin = np.abs(Z).min()
    cmap = plt.cm.jet
    
    # Normalize the colors b/w 0 and 1
    colors_norm = Normalize(vmin, vmax, clip=True)(Z)
    colors = cmap(colors_norm)
    
    # Now set the alpha channel
    colors[..., -1] = colors_norm 
        
    return [colors,[xmin, xmax, ymin, ymax]]


def load_data(map_name):
    try:
        file_path = 'https://wothub-data.s3.amazonaws.com/' + map_name + '.csv'
        df = pd.read_csv(file_path)
        #df = df.loc[(df['map_name'] == map_name),:] # FLAG Create local division
    except: 
        return pd.DataFrame([])
    return df

@st.cache
def load_img(map_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))   
    img_dir = os.path.join(dir_path,'maps/images')
    img_path = os.path.join(img_dir, map_name + '.png')
    img = plt.imread(img_path)
    return img

st.sidebar.title("WotHub")
st.sidebar.markdown('World of Tanks players position predictor.')
# choose parameters
map_to_filter = st.sidebar.selectbox('Map', map_names, index = 0)
team_to_filter = st.sidebar.radio('Team', (1,2))
levels_to_filter = st.sidebar.slider('Levels', 1, 10, (6,8))
types_to_filter = st.sidebar.multiselect('Type', vehicle_types, vehicle_types[0])
clock_to_filter = st.sidebar.slider('Clock', 0, 900, 300)
bandwidth_to_filter = st.sidebar.slider('Bandwidth', 1., 5., 2.)
st.sidebar.markdown('Made by [Pavel Tarashkevich](https://github.com/pashok3d)')

df = load_data(maps_data[map_to_filter]) 
img = load_img(maps_data[map_to_filter]) 

if not df.empty:
    type_bit_map = np.full(np.shape(df['type']), False)

    for type in types_to_filter:
        type_bit_map = np.asarray((type_bit_map) | (df['type'] == vehicle_types_data[type]))

    data_choice = df.loc[(df['team'] == team_to_filter) & (df['clock'] == clock_to_filter) & 
                                        (type_bit_map) &
                                        (df['tier'] >= levels_to_filter[0]) & (df['tier'] <= levels_to_filter[1])]
                                     
    if not data_choice.empty:
        color_map = density(data_choice, bandwidth_to_filter, 50j) 
        if color_map:
            background = Image.fromarray(np.uint8(img*255))
            density_map = Image.fromarray(np.uint8(color_map[0]*255))
            density_map = density_map.resize((512,512))
            background.paste(density_map, (0, 0),  density_map)
            st.image(background, use_column_width=True)
        else:
            st.text('Not enough data, try to change filter parameters.') 
    else:
        st.text('No data, try to change filter parameters.')
else:
    st.text('Failed to load data.')
    
    


import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from meta_data import map_names, maps
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
    kernel = stat.gaussian_kde(values)
    kernel.set_bandwidth(bw_method=kernel.factor / bandwidth)
    Z = np.reshape(kernel(positions).T, X.shape)
    
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

@st.cache
def load_data(map_name):
    df = pd.read_csv('https://wothub-data.s3.amazonaws.com/processed_data.csv')
    df = df.loc[(df['map_name'] == map_name),:] # FLAG Create local division
    return df

@st.cache
def load_img(map_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))   
    img_dir = os.path.join(dir_path,'maps/images')
    img_path = os.path.join(img_dir, map_name + '.png')
    img = plt.imread(img_path)
    return img

st.sidebar.title("WotHub")
# choose parameters
map_to_filter = st.sidebar.selectbox('Map', map_names, index = 15)
team_to_filter = st.sidebar.radio('Team', (1,2))
clock_to_filter = st.sidebar.slider('Clock', 0, 600, 300)
bandwidth_to_filter = st.sidebar.slider('Bandwidth', 1., 5., 2.)
st.sidebar.markdown('Made by [Pavel Tarashkevich](https://github.com/pashok3d)')

df = load_data(maps[map_to_filter]) 
img = load_img(maps[map_to_filter]) 

data_choice = df.loc[(df['team'] == team_to_filter) & (df['clock'] == clock_to_filter)]

if not data_choice.empty:
    color_map = density(data_choice, bandwidth_to_filter, 50j) 
    
    background = Image.fromarray(np.uint8(img*255))
    density_map = Image.fromarray(np.uint8(color_map[0]*255))
    density_map = density_map.resize((512,512))
    background.paste(density_map, (0, 0),  density_map)
    st.image(background)
else:
    st.text('No data.')
    
    


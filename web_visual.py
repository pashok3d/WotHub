import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from meta_data import map_names, maps
from matplotlib.colors import Normalize
import scipy.stats as stat

def density(data, bins = 50j):
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
def load_data(map):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    replays_path = os.path.join(dir_path,'pro_data')
    
    data_frames_paths = []
    for r, d, f in os.walk(replays_path):
            for file in f:
                if '.csv' in file:
                    data_frames_paths.append(os.path.join(r,file))
    
    df = pd.DataFrame([])
    
    for frame_path in data_frames_paths:
        df = df.append(pd.read_csv(frame_path), ignore_index = True)

    #df = df.loc[(df['map_name'] == maps[map_to_filter]),:] # FLAG Create local division

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
st.sidebar.markdown('`Made by Pavel Tarashkevich`')


df = load_data(maps[map_to_filter]) 
img = load_img(maps[map_to_filter]) 

data_choice = df.loc[(df['team'] == team_to_filter) & (df['clock'] == clock_to_filter),:]

if not data_choice.empty:
    color_map = density(data_choice, 50j)

    plt.style.use('classic')
    fig,ax = plt.subplots(figsize=(12, 12))
        
    ax.imshow(img, extent=[-500,500,-500,500]) 
    ax.imshow(color_map[0], extent=color_map[1])
    ax.set_axis_off()

    st.pyplot()
else:
    st.text('No data.')

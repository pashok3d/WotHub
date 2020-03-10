import pandas as pd
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import os

def density(data):
    x = data['x']
    y = data['z']
    
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = st.gaussian_kde(values)
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

if __name__ == '__main__':
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
        
    img_dir = os.path.join(dir_path,'maps\images')
    img_path = os.path.join(img_dir, df['map_name'][0] + '.png')
    img = plt.imread(img_path)
        
    color_map = density(df)
    
    plt.style.use('classic')
    fig,ax = plt.subplots(figsize=(7, 7))
        
    ax.imshow(img, extent=[-500,500,-500,500]) 
    ax.imshow(color_map[0], extent=color_map[1])
    ax.set_axis_off()
    
    plt.savefig('output.png', transparent = True)  









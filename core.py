import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from hypatie.plots import plot_radec, plot_altaz
from hypatie.transform import radec_to_altaz
from hypatie.data import cities
from constellations import constellations
from hipparcos import hip_stars
from io import StringIO

def load_constellations():
    data = constellations.split('\n')[1:-1]
    dc = {}
    for i in data:
        name = i.split(' ')[0]
        stars = i.split(' ')[2:]
        stars = [int(j) for j in stars]
        edges = [tuple(stars[k:k+2]) for k in [*range(0,len(stars),2)]]
        dc[name] = edges
    edges = []
    for k,v in dc.items():
        for i in v:
            edges.append(i)

    return edges

def load_hipparcos():
    df = pd.read_csv(StringIO(hip_stars)).set_index('hip')
    return df


def draw_chart(obs_loc, t, mag_max=5, alpha=0.3):
    lon, lat = obs_loc
    
    # Read Hipparcos stars
    df = load_hipparcos()
    df['alt'], df['az'] = radec_to_altaz(lon, lat, df['ra'], df['dec'], t)
    df = df[df['alt']>0]
    
    # Read constellations data
    edges = load_constellations()
    ls = []
    for i in edges:
        if (i[0] in df.index) and (i[1] in df.index):
            ls.append(i)
    edges = ls

    edge1 = [i[0] for i in edges]
    edge2 = [i[1] for i in edges]

    marker_size = (0.5 + 7 - df['Vmag'].values) ** 2.0

    df_bright = df[df['Vmag']<mag_max]

    xy1 = df[['az', 'alt']].loc[edge1].values
    xy2 = df[['az', 'alt']].loc[edge2].values
    xy1[:,0] = xy1[:,0]*(np.pi/180)
    xy2[:,0] = xy2[:,0]*(np.pi/180)
    lines_xy = np.array([*zip(xy1,xy2)])

    ax = plot_altaz(df_bright['az'], df_bright['alt'], mag=df_bright['Vmag'])
    ax.add_collection(LineCollection(lines_xy, alpha=alpha))
    
    return ax, df



#t = datetime(2022, 1, 13, 20, 21)
t = datetime.now()
obs_loc = cities['strasbourg'][:2]

ax, df = draw_chart(obs_loc, t, mag_max=5, alpha=0.4)
plt.show()

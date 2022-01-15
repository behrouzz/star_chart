import pandas as pd
import numpy as np
#from datetime import datetime
#import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from hypatie.plots import plot_radec, plot_altaz
from hypatie.transform import radec_to_altaz
#from hypatie.data import cities
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
    return dc

def create_edges(dc):
    """
    Create edges (lines) connecting each pair of stars
    
    Arguments
    ---------
        dc : dictionary of constellations
    Returns
    -------
        edges : list of all edges
    """
    edges = []
    for k,v in dc.items():
        for i in v:
            edges.append(i)
    return edges

def load_hipparcos():
    return pd.read_csv(StringIO(hip_stars)).set_index('hip')


def visible_hipparcos(obs_loc, t):
    lon, lat = obs_loc
    df = load_hipparcos()
    df['alt'], df['az'] = radec_to_altaz(lon, lat, df['ra'], df['dec'], t)
    df = df[df['alt']>0]
    return df

def draw_chart(df, df_show, dc_const, alpha):
    """
    df : visible hipparcos stars for the observer
    df_show : stars to be shown in the chart
    dc_const : dictionary of constellations
    """
    edges = create_edges(dc_const)
    edges = [i for i in edges if (i[0] in df.index) and (i[1] in df.index)]

    edge1 = [i[0] for i in edges]
    edge2 = [i[1] for i in edges]
    
    xy1 = df[['az', 'alt']].loc[edge1].values
    xy2 = df[['az', 'alt']].loc[edge2].values
    xy1[:,0] = xy1[:,0]*(np.pi/180)
    xy2[:,0] = xy2[:,0]*(np.pi/180)
    lines_xy = np.array([*zip(xy1,xy2)])

    marker_size = (0.5 + 7 - df['Vmag'].values) ** 2.0

    fig, ax = plot_altaz(df_show['az'], df_show['alt'], mag=df_show['Vmag'])
    ax.add_collection(LineCollection(lines_xy, alpha=alpha))
    
    return fig, ax, df_show


def draw(obs_loc, t, mag_max=5, alpha=0.3):
    df = visible_hipparcos(obs_loc, t)
    df_show = df[df['Vmag']<mag_max]
    dc_const = load_constellations()
    return draw_chart(df, df_show, dc_const, alpha)


dc = load_constellations()

const2star = {}
for k,v in dc.items():
    ls = []
    for i in range(len(v)):
        ls = ls + list(v[i])
    const2star[k] = list(set(ls))
    
star2const = {}
for k,v in const2star.items():
    for i in v:
        star2const[i] = k

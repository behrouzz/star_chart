import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from hypatie.plots import plot_radec, plot_altaz
from hypatie.transform import radec_to_altaz
from hypatie.data import cities
from stars import hip_stars, constellations
from io import StringIO

def constellations_func():
    class cns:
        def __init__(self, cns_str):
            self.name = cns_str.split(' ')[0]
            stars = cns_str.split(' ')[2:]
            stars = [int(i) for i in stars]
            self.edges = [tuple(stars[i:i+2]) for i in [*range(0,len(stars),2)]]

    data = constellations.split('\n')[:-1]
    dc = {}
    for i in data:
        tmp = cns(i)
        dc[tmp.name] = tmp.edges

    edges = []
    for k,v in dc.items():
        for i in v:
            edges.append(i)

    edge1 = [i[0] for i in edges]
    edge2 = [i[1] for i in edges]

    return edge1, edge2


def draw_chart(obs_loc, t, alpha=0.3):
    lon, lat = obs_loc

    df = pd.read_csv(StringIO(hip_stars)).set_index('hip')


    marker_size = (0.5 + 7 - df['Vmag'].values) ** 2.0

    t = t.isoformat()[:19].replace('T', ' ')

    alt, az = radec_to_altaz(
        lon=lon,
        lat=lat,
        ra=df['ra'],
        dec=df['dec'],
        t=t)

    new_df = pd.DataFrame(
        {'hip':df.index.values,
         'az':az, 'alt':alt,
         'Vmag':df['Vmag'].values})

    new_df = new_df.set_index('hip')

    bright_df = new_df[new_df['Vmag']<5]

    xy1 = new_df[['az', 'alt']].loc[edge1].values
    xy2 = new_df[['az', 'alt']].loc[edge2].values
    xy1[:,0] = xy1[:,0]*(np.pi/180)
    xy2[:,0] = xy2[:,0]*(np.pi/180)
    lines_xy = np.array([*zip(xy1,xy2)])

    ax = plot_altaz(bright_df['az'], bright_df['alt'], mag=bright_df['Vmag'])
    ax.add_collection(LineCollection(lines_xy, alpha=alpha))

    plt.show()



t = datetime(2022, 1, 13, 20, 21)
obs_loc = cities['strasbourg'][:2]

edge1, edge2 = constellations_func()
draw_chart(obs_loc, t, alpha=0.4)

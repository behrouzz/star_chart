from io import StringIO
from collections.abc import Iterable
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from constellations import constellations
from hipparcos import hip_stars


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

def draw_chart(df, df_show, dc_const, alpha, figsize=None):
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

    mag_max = df_show['Vmag'].max()

    marker_size = (0.5 + mag_max - df['Vmag'].values) ** 2

    fig, ax = plot_altaz(df_show['az'], df_show['alt'], mag=df_show['Vmag'], figsize=figsize)
    ax.add_collection(LineCollection(lines_xy, alpha=alpha, color='blue'))
    
    return fig, ax, df_show


def draw(obs_loc, t, mag_max=5, alpha=0.3, figsize=None):
    df = visible_hipparcos(obs_loc, t)
    df_show = df[df['Vmag']<mag_max]
    dc_const = load_constellations()
    return draw_chart(df, df_show, dc_const, alpha, figsize)

def plot_altaz(az, alt, mag=None, size=None, color='w', alpha=1, marker='o', ax=None, figsize=None):
    """
    Plot positions of bodies based on altitude/azimuth coordinates
    Arguments
    ---------
        az (iter of float): azimuth values
        alt (iter of float): altitude values
        mag (iter of float): apparent magnitudes; default None.
        size (int): size; default None.
        color (str): color; default 'k'.
        alpha (float): alpha value (transparency), between 0 and 1; default 1.
        marker (str): marker shape; default 'o'.
        ax (axes): axes object; default None.
    Returns
    -------
        matplotlib axes object
    """

    if isinstance(az, Iterable):
        az = np.array(az)
        alt = np.array(alt)
        mag = np.array(mag) if mag is not None else None
    else:
        az = np.array([az])
        alt = np.array([alt])
        mag = None
        
    az  = az*(np.pi/180)

    if size is None:
        if mag is None:
            size = [5] * len(az)
        else:
            size = (0.1 + max(mag)-mag)**1.8

    plt.style.use('dark_background')
    if ax is None:
        if figsize is None:
            fig = plt.figure()
        else:
            fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.1,0.1,0.8,0.8], polar=True)
        ax.set_theta_zero_location('N')
        ax.set_rlim(90, 0, 1)
        ax.set_yticks(np.arange(0,91,30))
        ax.set_xticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 6*np.pi/4, 7*np.pi/4])
        ax.set_xticklabels(['N','NE','E','SE','S','SW','W','NW'])
        ax.tick_params(axis=u'both', which=u'both',length=0)
    if matplotlib.__version__ < '3.0.0':
        alt = [90-i for i in alt]
    ax.scatter(az, alt, c=color, s=size, alpha=alpha, marker=marker)
    ax.grid(True, alpha=0.1)
    return fig, ax


def radec_to_altaz(lon, lat, ra, dec, t):
    """
    Convert ra/dec coordinates to az/alt coordinates
    Arguments
    ---------
        lon (float): longtitude of observer location
        lat (float): latitude of observer location
        ra (iter of float): right ascension value(s)
        dec (iter of float): declination value(s)
        t (datetime): time of observation.
    Returns
    -------
        altitude(s), azimuth(s)
    """
    d2r = np.pi/180
    r2d = 180/np.pi

    if isinstance(ra, Iterable):
        ra = np.array(ra)
        dec = np.array(dec)

    J2000 = datetime(2000,1,1,12)
    d = (t - J2000).total_seconds() / 86400 #day offset

    UT = t.hour + t.minute/60 + t.second/3600
    LST = (100.46 + 0.985647 * d + lon + 15*UT + 360) % 360
    ha = (LST - ra + 360) % 360
    
    x = np.cos(ha*d2r) * np.cos(dec*d2r)
    y = np.sin(ha*d2r) * np.cos(dec*d2r)
    z = np.sin(dec*d2r)
    xhor = x*np.cos((90-lat)*d2r) - z*np.sin((90-lat)*d2r)
    yhor = y
    zhor = x*np.sin((90-lat)*d2r) + z*np.cos((90-lat)*d2r)
    az = np.arctan2(yhor, xhor)*r2d + 180
    alt = np.arcsin(zhor)*r2d
    return alt, az

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

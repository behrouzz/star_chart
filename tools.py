import numpy as np
from collections.abc import Iterable
from datetime import datetime
from hypatie import utc2tdb

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


def load_constellations(const_str):
    data = const_str.split('\n')[1:-1]
    dc = {}
    for i in data:
        name = i.split(' ')[0]
        stars = i.split(' ')[2:]
        stars = [int(j) for j in stars]
        edges = [tuple(stars[k:k+2]) for k in [*range(0,len(stars),2)]]
        dc[name] = edges
    return dc

def create_edges(dc):
    edges = []
    for k,v in dc.items():
        for i in v:
            edges.append(i)
    return edges

class SS_GCRS:
    """
    Solar System Objects in GCRS
    """
    def __init__(self, dc, t):
        tdb = utc2tdb(t)
        earth = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
        self.sun = dc[(0,10)].get_pos(tdb) - earth
        self.mercury = dc[(0, 1)].get_pos(tdb) - earth
        self.venus = dc[(0, 2)].get_pos(tdb) - earth
        self.moon = dc[(0, 3)].get_pos(tdb) + dc[(3, 301)].get_pos(tdb) - earth
        self.mars = dc[(0, 4)].get_pos(tdb) - earth
        self.jupiter = dc[(0, 5)].get_pos(tdb) - earth
        self.saturn = dc[(0, 6)].get_pos(tdb) - earth
        self.uranus = dc[(0, 7)].get_pos(tdb) - earth
        self.neptune = dc[(0, 8)].get_pos(tdb) - earth

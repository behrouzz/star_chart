import numpy as np
import pandas as pd
from collections.abc import Iterable
from datetime import datetime
from hypatie import utc2tdb
from hypatie.transform import car2sph

def rev(x):
    return x % 360

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


def get_sun(t):
    """
    Get geocentric ecliptic position of the Sun
    """
    tt = utc2tt(t)
    jd = datetime_to_jd(tt)
    n = jd - 2451545
    L = rev(280.460 + 0.985647*n) # mean longitude
    g = rev(357.528 + 0.9856003*n) # mean anomaly
    # Ecliptic coordinates
    ecl_lon = rev(L + 1.915 * np.sin(g*d2r) + 0.020 * np.sin(2*g*d2r))
    ecl_lat = 0
    r = 1.00014 - 0.01671*np.cos(g*d2r) - 0.00014*np.cos(2*g*d2r)
    return ecl_lon, ecl_lat, r


def elon_fv(obj_name, df, lon_sun, s):
    ra, dec, R = df.loc[obj_name, ['ra', 'dec', 'r']]
    R = R / au
    radec = np.array([ra, dec])
    lon, lat = _equsph2eclsph(radec)

    if obj_name=='moon':
        elon = np.arccos(np.cos((lon_sun-lon)*d2r) * np.cos(lat*d2r) )*r2d
        fv = 180 - elon
    else:
        sun_gcrs = df.loc['sun'][['x','y','z']].values
        obj_gcrs = df.loc[obj_name][['x','y','z']].values
        r = np.linalg.norm(np.array(sun_gcrs - obj_gcrs)) / au
        elon = np.arccos((s**2 + R**2 - r**2)/(2*s*R))*r2d
        fv    = np.arccos((r**2 + R**2 - s**2)/(2*r*R))*r2d
    return elon, fv


class SS_GCRS:
    """
    Solar System Objects in GCRS
    """
    def __init__(self, dc, t):
        self.t = t
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

    def radec(self):
        car = np.array([self.sun, self.mercury, self.venus, self.moon,
                        self.mars, self.jupiter, self.saturn,
                        self.uranus,self.neptune])
        sph = car2sph(car)
        arr = np.hstack((car, sph))
        objs = ['sun', 'mercury', 'venus', 'moon', 'mars',
                'jupiter', 'saturn', 'uranus', 'neptune']
        df = pd.DataFrame(arr, columns=['x','y','z','ra','dec','r'], index=objs)
        colors = ["rgb(255,255,0)", "rgb(128,0,128)", "rgb(128,128,0)",
                  "rgb(255,255,255)", "rgb(255,0,0)", "rgb(128,0,0)",
                  "rgb(0,128,0)", "rgb(0,255,255)", "rgb(0,128,128)"]
        df['color'] = colors
        return df

    def altaz(self, obs_loc):
        df = self.radec()
        lon, lat = obs_loc
        df['alt'], df['az'] = radec_to_altaz(lon, lat, df['ra'].values, df['dec'].values, self.t)
        return df

    def final(self, obs_loc):
        df = self.altat(obs_loc)
        

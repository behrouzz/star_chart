import numpy as np
from hypatie.time import utc2tt, datetime_to_jd, utc2tdb
from datetime import datetime
from numeph import load_pickle
from tools import SS_GCRS, radec_to_altaz
from hypatie.transform import _equsph2eclsph, car2sph

d2r = np.pi/180
r2d = 180/np.pi
au = 149597870.70000002 # km

import pandas as pd

name2num = {'sun':10, 'mercury':1, 'venus':2, 'moon':301, 'mars':4,
           'jupiter':5, 'saturn':6, 'uranus':7, 'neptune':8}

objects = list(name2num.keys())

class _SSObj:
    def __init__(self, name, dc, tdb, earth_icrs, sun_gcrs, lon_sun, s, obs_loc=None, t=None):
        self.name = name
        self.dc = dc
        self.tdb = tdb
        self.earth_icrs = earth_icrs
        #self.earth_icrs = dc[(0, 3)].get_pos(self.tdb) + dc[(3, 399)].get_pos(self.tdb)
        self.icrs = self.get_icrs(self.name, self.dc, self.tdb)
        self.gcrs = self.icrs - self.earth_icrs
        ra, dec, self.distance = car2sph(self.gcrs)
        self.radec = np.array([ra, dec]) # ra, dec in GCRS
        if (obs_loc is not None) and (t is not None):
            LON, LAT = obs_loc
            self.alt, self.az = radec_to_altaz(LON, LAT, ra, dec, t)
            
        lon, lat = _equsph2eclsph(self.radec)

        if self.name=='moon':
            self.elongation = np.arccos(np.cos((lon_sun-lon)*d2r) * np.cos(lat*d2r) )*r2d
            self.fv = 180 - self.elongation
        else:
            r = np.linalg.norm(np.array(sun_gcrs - self.gcrs)) / au
            R = self.distance / au
            self.elongation = np.arccos((s**2 + R**2 - r**2)/(2*s*R))*r2d
            self.fv = np.arccos((r**2 + R**2 - s**2)/(2*r*R))*r2d
        
    def get_icrs(self, name, dc, tdb):
        if name=='moon':
            icrs = dc[(0, 3)].get_pos(tdb) + dc[(3, 301)].get_pos(tdb)
        else:
            icrs = dc[(0, name2num[name])].get_pos(tdb)
        return icrs

        

def asli(dc, t, obs_loc):
    tdb = utc2tdb(t)
    earth_icrs = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
    sun_gcrs = dc[(0, 10)].get_pos(tdb) - earth_icrs
    lon_sun, _, s = get_sun(t)

    
    my_dic = {}
    #for o in objects:
    for o in ['mercury', 'venus', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']:
        my_dic[o] =_SSObj(o, dc, tdb, earth_icrs, sun_gcrs, lon_sun, s, obs_loc, t)
    return my_dic
    


def rev(x):
    return x % 360

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


t = datetime.utcnow()

#===================================


dc = load_pickle('data/de440s_2020_2030.pickle')
ss = SS_GCRS(dc, t)
df = ss.radec()

dc_ss = {'sun': ss.sun, 'mercury': ss.mercury, 'venus': ss.venus,
         'moon': ss.moon, 'mars': ss.mars, 'jupiter': ss.jupiter,
         'saturn': ss.saturn, 'uranus': ss.uranus, 'neptune': ss.neptune}
#===================================


def elon_fv(obj_name, t):
    lon_sun, _, s = get_sun(t)
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




#ss = SolSys(dc, t)
"""
tdb = utc2tdb(t)
earth_icrs = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
a = _SSObj('sun', dc, tdb, earth_icrs)

sun_gcrs = a.gcrs
sun_lonlat = _equsph2eclsph(car2sph(sun_gcrs)[:-1])
"""
obs_loc = (7, 48)
a = asli(dc, t, obs_loc)

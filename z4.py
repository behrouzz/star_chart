import numpy as np
from hypatie.time import utc2tt, datetime_to_jd, utc2tdb
from datetime import datetime
from numeph import load_pickle
from tools import SS_GCRS
from hypatie.transform import _equsph2eclsph, car2sph

d2r = np.pi/180
r2d = 180/np.pi
au = 149597870.70000002 # km

import pandas as pd

name2num = {'sun':10, 'mercury':1, 'venus':2, 'moon':301, 'mars':4,
           'jupiter':5, 'saturn':6, 'uranus':7, 'neptune':8}

objects = list(name2num.keys())

class _SSObj:
    def __init__(self, name, dc, tdb, earth_icrs):
        self.name = name
        self.dc = dc
        self.tdb = tdb
        self.earth_icrs = earth_icrs
        #self.earth_icrs = dc[(0, 3)].get_pos(self.tdb) + dc[(3, 399)].get_pos(self.tdb)
        self.icrs = self.get_icrs(self.name, self.dc, self.tdb)
        

    def get_icrs(self, name, dc, tdb):
        if name not in objects:
            raise Exception('Object not found!')
        elif name=='moon':
            icrs = dc[(0, 3)].get_pos(tdb) + dc[(3, 301)].get_pos(tdb)
        else:
            icrs = dc[(0, name2num[name])].get_pos(tdb)
        return icrs
        

class SolSys:
    """
    Solar System Objects in GCRS
    """
    def __init__(self, dc, t):
        self.t = t
        tdb = utc2tdb(t)
        
        # ICRS
        self.earth = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
        self.sun = dc[(0,10)].get_pos(tdb)
        self.mercury = dc[(0, 1)].get_pos(tdb)
        self.venus = dc[(0, 2)].get_pos(tdb)
        self.moon = dc[(0, 3)].get_pos(tdb) + dc[(3, 301)].get_pos(tdb)
        self.mars = dc[(0, 4)].get_pos(tdb)
        self.jupiter = dc[(0, 5)].get_pos(tdb)
        self.saturn = dc[(0, 6)].get_pos(tdb)
        self.uranus = dc[(0, 7)].get_pos(tdb)
        self.neptune = dc[(0, 8)].get_pos(tdb)



        
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
        arr = np.array([self.sun, self.mercury, self.venus, self.moon,
                        self.mars, self.jupiter, self.saturn,
                        self.uranus,self.neptune])
        arr = car2sph(arr)
        objs = ['sun', 'mercury', 'venus', 'moon', 'mars',
                'jupiter', 'saturn', 'uranus', 'neptune']
        df = pd.DataFrame(arr, columns=['ra','dec','r'], index=objs)
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
        r = np.linalg.norm(np.array(ss.sun - dc_ss[obj_name])) / au
        elon = np.arccos((s**2 + R**2 - r**2)/(2*s*R))*r2d
        fv    = np.arccos((r**2 + R**2 - s**2)/(2*r*R))*r2d
    return elon, fv


"""
# just for test
from solsys import sun, moon, planet
p = planet('jupiter', t)
m = moon(t)
s = sun(t)


objects = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

for o in objects:
    elon, fv = elon_fv(o, t)
    print(o)
    print('Khodam: ', elon, fv)
    p = planet(o, t)
    print('Yaroue: ', p.elongation, p.FV)
    print('-'*50)
"""

#ss = SolSys(dc, t)

tdb = utc2tdb(t)
earth_icrs = dc[(0, 3)].get_pos(tdb) + dc[(3, 399)].get_pos(tdb)
a = _SSObj('sun', dc, tdb, earth_icrs)

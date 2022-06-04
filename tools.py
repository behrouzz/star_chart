import numpy as np
import pandas as pd
from collections.abc import Iterable
from datetime import datetime
from hypatie.time import utc2tdb, utc2tt, datetime_to_jd
from hypatie.transform import car2sph, _equsph2eclsph

d2r = np.pi/180
r2d = 180/np.pi
au = 149597870.70000002 # km

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



def app_mag(name, r, R, FV):
    mags = {'mercury' : -0.36 + 5*np.log10(r*R) + 0.027 * FV + 2.2E-13 * FV**6,
            'venus'   : -4.34 + 5*np.log10(r*R) + 0.013 * FV + 4.2E-7  * FV**3,
            'mars'    : -1.51 + 5*np.log10(r*R) + 0.016 * FV,
            'jupiter' : -9.25 + 5*np.log10(r*R) + 0.014 * FV,
            'saturn'  :0, # should be corrected!!
            'uranus'  : -7.15 + 5*np.log10(r*R) + 0.001 * FV,
            'neptune' : -6.90 + 5*np.log10(r*R) + 0.001 * FV}
    return mags[name]
  
    

class SS_GCRS:
    """
    Solar System Objects in GCRS
    """
    def __init__(self, dc, t):
        self.t = t
        tdb = utc2tdb(t)
        self.objects = ['sun', 'mercury', 'venus', 'moon', 'mars',
                        'jupiter', 'saturn', 'uranus', 'neptune']
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

        df = pd.DataFrame(arr, columns=['x','y','z','ra','dec','r'], index=self.objects)
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
        df = self.altaz(obs_loc)
        lon_sun, lat_sun, r_sun = get_sun(self.t)
        lonlats = _equsph2eclsph(df[['ra', 'dec']].values)
        df['lon'] = lonlats[:,0]
        df['lat'] = lonlats[:,1]

        # NEW
        planets = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
        df_s = df.loc[['sun']]
        df_m = df.loc[['moon']]
        df_p = df.loc[planets]

        df_m['elognation'] = np.arccos(np.cos((lon_sun-df_m['lon'])*d2r) * np.cos(df_m['lat']*d2r) )*r2d
        df_m['fv'] = 180 - df_m['elognation']
        df_m['phase'] = ((180-df_m['fv'])/180)*100

        sun_gcrs = df_s[['x','y','z']].values
        pla_gcrs = df_p[['x','y','z']].values

        d = df_s[['x','y','z']].values - df_p[['x','y','z']].values
        r = np.array([np.linalg.norm(i)/au for i in d]) # distance to sun
        R = (df_p['r'] / au).values
        
        df_p['elognation'] = np.arccos((r_sun**2 + R**2 - r**2)/(2*r_sun*R))*r2d
        df_p['fv']    = np.arccos((r**2 + R**2 - r_sun**2)/(2*r*R))*r2d
        df_p['phase'] = ((180-df_p['fv'])/180)*100

        # apparent magnitude
        tmp = pd.DataFrame(index=planets)
        tmp['d0'] = [6.74, 16.92,9.32, 191.01, 158.2, 63.95, 61.55]
        tmp['r'] = r
        tmp['R'] = R
        tmp['fv'] = df_p['fv']
        tmp.reset_index(inplace=True)
        df_p['mag'] = tmp.apply(lambda x: app_mag(x['index'], x['r'], x['R'], x['fv']), axis=1).values
        # diameter
        df_p['diam'] = tmp['d0'].values / r

        return df, df_s, df_m, df_p
        

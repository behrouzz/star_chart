import numpy as np
from hypatie.time import utc2tt, datetime_to_jd
from datetime import datetime
from numeph import load_pickle
from tools import SS_GCRS

d2r = np.pi/180
r2d = 180/np.pi
au = 149597870.70000002 # km

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

from hypatie.transform import _equsph2eclsph

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
    

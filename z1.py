from datetime import datetime
from numeph import load_pickle
from tools import SS_GCRS, app_mag
import numpy as np

t = datetime.utcnow()
obs_loc = (7, 48)

dc = load_pickle('data/de440s_2020_2030.pickle')

ss = SS_GCRS(dc, t)

df, df_s, df_m, df_p = ss.final(obs_loc)

print(df_p)
"""
planets = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']

from solsys import sun, moon, planet

s = sun(t, obs_loc)
m = moon(t, obs_loc)

for i in planets:
    p = planet(i, t, obs_loc)
    print(p.name, ':', p.mag)
"""

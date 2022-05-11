from datetime import datetime
from numeph import load_pickle
from tools import SS_GCRS
from hypatie.transform import car2sph
import numpy as np

t = datetime.utcnow()

dc = load_pickle('data/de440s_2020_2030.pickle')

ss = SS_GCRS(dc, t)

arr = np.array([
ss.sun,
ss.mercury,
ss.venus,
ss.moon,
ss.mars,
ss.jupiter,
ss.saturn,
ss.uranus,
ss.neptune
])

a = car2sph(arr)

b = a[:, :2]

from datetime import datetime
from numeph import load_pickle
from tools import SS_GCRS
import numpy as np

t = datetime.utcnow()

dc = load_pickle('data/de440s_2020_2030.pickle')

ss = SS_GCRS(dc, t)

df = ss.final((5,10))


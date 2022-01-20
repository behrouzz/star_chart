# https://plotly.com/python/reference/scatterpolar/
# https://plotly.com/python/reference/layout/polar/
# https://plotly.com/python/reference/layout/


from hypatie.data import cities
from datetime import datetime
import skychart as sch
import plotly.graph_objects as go
import pandas as pd
import numpy as np


my_df = pd.read_csv('hip7.csv').set_index('hip')

all_hip = sch.load_hipparcos()

city = 'strasbourg'

t = datetime.now()
obs_loc = cities[city][:2]

df = sch.visible_hipparcos(obs_loc, t)

# eslah
aa = set(all_hip.index).difference(set(my_df.index))
print(all_hip.loc[aa])
"""
>>> all_hip.loc[aa]
                ra        dec  Vmag
hip                                
55203   169.545550  31.529289  3.79
115125  349.777337 -13.455251  5.19
78727   241.092227 -11.373104  4.16

SEARCHING FOR THESE:
--------------------
SELECT main_id, ra, dec, V
FROM basic as b
JOIN allfluxes as f
ON b.oid=f.oidref
WHERE 
((V>3.7) AND (V<3.8) AND (ra>169) AND (ra<170))
OR
((V>5.1) AND (V<5.2) AND (ra>349) AND (ra<350))
OR
((V>4.1) AND (V<4.2) AND (ra>241) AND (ra<242))

RESULTS:
--------
  main_id  |        ra        |        dec        | V  
-----------|------------------|-------------------|----
"* ksi UMa"|169.54554950000002|31.529288899999997 |3.79
"*  94 Aqr"|349.77802373852126|-13.458781827991944|5.18
"* ksi Sco"|241.09222739999996|-11.3731039        |4.17

So, I should add these three stars to hip7.csv
"""
s1 = {'hip':55203, 'ra':169.54554950000002, 'dec':31.529288899999997, 'Vmag':3.79, 'plx':113.2, 'bv':0.606, 'period':np.nan, 'SpType':'G0V', 'main_id':'* ksi UMa'}
s2 = {'hip':115125, 'ra':349.77802373852126, 'dec':-13.458781827991944, 'Vmag':5.18, 'plx':44.8996, 'bv':0.895, 'period':42, 'SpType':'K2V', 'main_id':'*  94 Aqr'}
s3 = {'hip':78727, 'ra':241.09222739999996, 'dec':-11.3731039, 'Vmag':4.17, 'plx':43.0, 'bv':0.460, 'period':np.nan, 'SpType':'F6IV', 'main_id':'* ksi Sco'}

to_add = pd.DataFrame(list([s1,s2,s3]))
to_add = to_add.set_index('hip')

new_my_df = pd.concat([my_df, to_add])
new_my_df = new_my_df.to_csv('hip7_add3.csv')

#b = pd.merge(df.reset_index(), my_df.reset_index(), how='left', on='hip')


import pandas as pd
from BV_to_RGB import bs_bv2kelvin, temp2rgb
import numpy as np

df = pd.read_csv('hip7.csv').set_index('hip')

#df.loc[df['NAME'].notnull(), 'name'] = df['main_id'] + ' | ' + df['NAME']
#df.loc[df['NAME'].isna(), 'name'] = df['main_id']

df.loc[df['bv'].notnull(), 'temperature'] = df['bv'].apply(lambda x: bs_bv2kelvin(x))
df.loc[df['bv'].isna(), 'temperature'] = 'NA'

df.loc[df['bv'].notnull(), 'rgb'] = df.loc[df['bv'].notnull(), 'temperature'].apply(lambda x: temp2rgb(float(x)))
df.loc[df['bv'].isna(), 'rgb'] = 'NA'

mean_temp = df.loc[df['temperature']!='NA', 'temperature'].astype(float).mean()
rgb_mean = temp2rgb(mean_temp)

df['rgb'] = df['rgb'].astype(str).str.replace(' ','')


# bv should be searched
a = df[df['bv'].isna()]

"""
SELECT main_id, f.B, f.V
FROM basic AS b
LEFT JOIN allfluxes AS f
ON f.oidref=b.oid
WHERE main_id IN ('HD   7710', 'V* U Cam', 'HD  27762', 'HD 28630', '* tet01 Ori A', 'HD  43857', 'BD+55 1122', 'HD 101387', 'HD 119796', 'HD 137583', 'HD 138138')



    main_id    | B  | V  
---------------|----|----
"HD   7710"    |7.19|7.16
"V* U Cam"     |11.5|11.0
"HD  27762"    |7.08|6.93
"HD  28630"    |    |
"* tet01 Ori A"|6.75|6.73
"HD  43857"    |6.94|6.86
"BD+55  1122"  |    |
"HD 101387"    |8.0 |6.85
"HD 119796"    |9.05|6.8 
"HD 137583"    |7.17|7.01
"HD 138138"    |    |    




"""

bv = {"HD   7710": (7.19 - 7.16),
      "V* U Cam": (11.5 - 11.0),
      "HD  27762": (7.08 - 6.93),
      "HD 28630":9999,
      "* tet01 Ori A": (6.75 - 6.73),
      "HD  43857": (6.94 - 6.86),
      "BD+55 1122":9999,
      "HD 101387": (8.0 - 6.85),
      "HD 119796": (9.05 - 6.8),
      "HD 137583": (7.17 - 7.01),
      "HD 138138":9999}

df.loc[df['bv'].isna(), 'bv'] = df.loc[df['bv'].isna(), 'main_id'].apply(lambda x: bv[x])
df.loc[df['bv']==9999, 'bv'] = np.nan

df.to_csv('hip7_2.csv')
"""
df['n'] = df.reset_index().index

rgb_ls = []
for i,v in df.iterrows():
    if v['rgb']!='NA':
        rgb_ls.append([v['n'], "rgb" + str(v['rgb']).replace(' ', '')])
    else:
        rgb_ls.append([v['n'], str(rgb_mean).replace(' ', '')])
df['rgb_ls'] = rgb_ls
"""



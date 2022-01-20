import pandas as pd
from BV_to_RGB import bs_bv2kelvin, temp2rgb
import numpy as np

df = pd.read_csv('hip7_2.csv').set_index('hip')

df.loc[df['bv'].notnull(), 'temperature'] = df['bv'].apply(lambda x: bs_bv2kelvin(x))
df.loc[df['bv'].isna(), 'temperature'] = 'NA'

df.loc[df['bv'].notnull(), 'rgb'] = df.loc[df['bv'].notnull(), 'temperature'].apply(lambda x: temp2rgb(float(x)))
df.loc[df['bv'].isna(), 'rgb'] = 'NA'

mean_temp = df.loc[df['temperature']!='NA', 'temperature'].astype(float).mean()
rgb_mean = temp2rgb(mean_temp)

df['rgb'] = df['rgb'].astype(str).str.replace(' ','')

df.loc[df['bv'].isna(), 'rgb'] = str(rgb_mean).replace(' ','')

df['rgb'] = 'rgb' + df['rgb']

df.to_csv('hip7_3.csv')

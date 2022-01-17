from hypatie.data import cities
from datetime import datetime
import core as sch

t = datetime.now()
obs_loc = cities['strasbourg'][:2]

df = sch.visible_hipparcos(obs_loc, t)
df_show = df[df['Vmag']<3]

#=================================================

"""
>>> df_show
                ra        dec  Vmag        alt          az
hip                                                       
26634    84.912249 -34.074108  2.65   2.213580  206.954153
14354    46.294139  38.840274  3.32  39.162807  287.420483
22549    72.801516   5.605104  3.68  32.457000  236.906045
"""

import plotly.express as px
import numpy as np

df = df_show

df['new_az'] = df['az']#*(np.pi/180)
df['new_alt'] = 90-df['alt']

df['size'] = (df['Vmag'].max() - df['Vmag'].values)

fig = px.scatter_polar(df, r="new_alt", theta="new_az",
                       size='size',
                       direction="counterclockwise")

fig.write_html('Htmls/01.html', auto_open=True)


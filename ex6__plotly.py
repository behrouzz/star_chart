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

import plotly.graph_objects as go
import numpy as np

df = df_show

r = 90 - df['alt'].values
theta = df['az'].values
size = 1 + (df['Vmag'].max() - df['Vmag'].values)
sizeref = 2.*max(size)/(8.**2)


marker = {'size'    : size,
          'sizemode': 'area',
          'sizeref' : sizeref,
          'sizemin' : 2}

data = go.Scatterpolar(r=r, theta=theta, mode='markers', marker=marker)

fig = go.Figure(data=data)

# https://plotly.com/python/reference/layout/polar/

fig.update_layout(
    polar = dict(
      angularaxis = dict(direction="counterclockwise", rotation=90,
                         tickmode='array', tickvals=[0,90,180,270],
                         ticktext=['N','E','S','W']),
      
      radialaxis = dict(tickmode='array', tickvals=[0,30,60,90], ticktext=['90','60','30','0'])
    ))

fig.write_html('Htmls/01.html', auto_open=True)



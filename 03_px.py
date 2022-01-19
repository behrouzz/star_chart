from hypatie.data import cities
from datetime import datetime
import skychart as sch

city = 'strasbourg'

t = datetime.now()
obs_loc = cities[city][:2]

df = sch.visible_hipparcos(obs_loc, t)
df_show = df[df['Vmag']<4]

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

now_date = t.isoformat()[:10]
now_time = t.isoformat()[11:16]

title = city.title() + ' | ' + now_date + ' | ' + now_time


df = df_show
df = df.reset_index()
df['hip'] = 'HIP ' + df['hip'].astype(str)


df['new_az'] = df['az']#*(np.pi/180)
df['new_alt'] = 90-df['alt']

df['size'] = 0.5 + (df['Vmag'].max() - df['Vmag'].values)

hover_data = {'hip':False, 'ra':':.4f', 'dec':':.4f',
              'Vmag':':.2f',
              'alt':False, 'az':False,
              'new_az':False, 'new_alt':False, 'size':False}

fig = px.scatter_polar(df, r="new_alt", theta="new_az",
                       size='size', size_max=5,
                       direction="counterclockwise",
                       title = title,
                       template='plotly_dark',
                       width=1000, height=1000,
                       hover_data=hover_data,
                       hover_name='hip')

polar={'radialaxis' : {'tickmode':'array',
                       'tickvals':[0,30,60,90],
                       'ticktext':['90','60','30','0'],
                       'gridcolor': '#222',
                       'linecolor': '#222'},

       'angularaxis': {'tickmode':'array',
                       'tickvals':[0,90,180,270],
                       'ticktext':['N','E','S','W'],
                       'gridcolor': '#222'}
       
       }

fig.update_layout(polar=polar)

fig.write_html('Htmls/01.html', auto_open=True)


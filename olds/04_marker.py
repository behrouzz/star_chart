from hypatie.data import cities
from datetime import datetime
import skychart as sch

city = 'strasbourg'

t = datetime.now()
obs_loc = cities[city][:2]

df = sch.visible_hipparcos(obs_loc, t)
df_show = df[df['Vmag']<4]


now_date = t.isoformat()[:10]
now_time = t.isoformat()[11:16]
title = '<b>'+city.title()+'</b>' + '<br>' + now_date + '<br>' + now_time

#=================================================
import plotly.graph_objects as go
import numpy as np

df_show = df_show.reset_index()
df_show['hip'] = 'HIP ' + df_show['hip'].astype(str)

r = 90 - df_show['alt'].values
theta = df_show['az'].values
size = 1 + (df_show['Vmag'].max() - df_show['Vmag'].values)
sizeref = 2.*max(size)/(8.**2)


marker = {'size':size, 'sizemode':'area', 'sizeref':sizeref, 'sizemin':2}

hovertext = '<b>'+df_show['hip']+ '</b><br>' + 'ra: ' + df_show['ra'].astype(str)\
            + '<br>dec: ' + df_show['dec'].astype(str)\
            + '<br>Vmag: ' + df_show['Vmag'].astype(str)

data = go.Scatterpolar(r=r, theta=theta,
                       mode='markers',
                       marker=marker,
                       hovertext=hovertext,
                       hoverinfo='text')

fig = go.Figure(data=data)

# https://plotly.com/python/reference/layout/polar/

angularaxis = {'direction': "counterclockwise",
               'rotation': 90,
               'tickmode':'array',
               'tickvals':[0,90,180,270],
               'ticktext':['N','E','S','W'],
               'gridcolor': '#222'}

radialaxis = {'tickmode':'array',
              'tickvals':[0,30,60,90],
              'ticktext':['90','60','30','0'],
              'gridcolor': '#222',
              'linecolor': '#222'}

fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis})

fig.update_layout(title=title, height=1000, width=1000, template='plotly_dark')

fig.write_html('Htmls/01.html', auto_open=True)



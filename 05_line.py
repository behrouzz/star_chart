from hypatie.data import cities
from datetime import datetime
import skychart as sch

city = 'strasbourg'

t = datetime.now()
obs_loc = cities[city][:2]

df = sch.visible_hipparcos(obs_loc, t)
df_show = df[df['Vmag']<4]
dc_const = sch.load_constellations()
edges = sch.create_edges(dc_const)

edges = [i for i in edges if (i[0] in df.index) and (i[1] in df.index)]
#=================================================


import plotly.graph_objects as go
import numpy as np

data = []

for e in edges:
    th1 = df.loc[e[0]]['az']
    r1  = 90 - df.loc[e[0]]['alt']
    th2 = df.loc[e[1]]['az']
    r2  = 90 - df.loc[e[1]]['alt']

    data.append(go.Scatterpolar(r=[r1,r2], theta=[th1,th2], line={'color':'blue'}, showlegend=False, hoverinfo='none'))


fig = go.Figure(data=data)

fig.update_layout(
    polar = dict(
      angularaxis = dict(direction="counterclockwise", rotation=90,
                         tickmode='array', tickvals=[0,90,180,270],
                         ticktext=['N','E','S','W']),
      
      radialaxis = dict(tickmode='array', tickvals=[0,30,60,90], ticktext=['90','60','30','0'])
    ))

fig.write_html('Htmls/01.html', auto_open=True)


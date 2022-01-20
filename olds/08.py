# https://plotly.com/python/reference/scatterpolar/
# https://plotly.com/python/reference/layout/polar/
# https://plotly.com/python/reference/layout/


from hypatie.data import cities
from datetime import datetime
import skychart as sch
import plotly.graph_objects as go
import pandas as pd

def my_own_df(df):
    my_df = pd.read_csv('hip7.csv').set_index('hip')
    my_df = my_df.loc[df.index]
    my_df = pd.merge(my_df.reset_index(), df[['alt','az']].reset_index(), how='left', on='hip')
    my_df = my_df.set_index('hip')
    return my_df

city = 'strasbourg'

t = datetime.now()
obs_loc = cities[city][:2]

df = sch.visible_hipparcos(obs_loc, t)

df = my_own_df(df)
df.loc[df['NAME'].notnull(), 'name'] = df['main_id'] + ' | ' + df['NAME']
df.loc[df['NAME'].isna(), 'name'] = df['main_id']

df_show = df[df['Vmag']<4]
dc_const = sch.load_constellations()
edges = sch.create_edges(dc_const)

edges = [i for i in edges if (i[0] in df.index) and (i[1] in df.index)]

now_date = t.isoformat()[:10]
now_time = t.isoformat()[11:16]
title = '<b>'+city.title()+'</b>' + '<br>' + now_date + '<br>' + now_time

#=================================================

df_show = df_show.reset_index()
df_show['hip'] = 'HIP ' + df_show['hip'].astype(str)

marker_size = (1 + (df_show['Vmag'].max() - df_show['Vmag'].values))**1.7

star_marker = {'size': marker_size,
               'sizemode':'area',
               'sizeref':2.*max(marker_size)/(8.**2),
               'sizemin':0.5}

star_hovertext = '<b>'+df_show['name']+ '</b><br>' + 'ra: ' + \
                 df_show['ra'].astype(str) + '<br>dec: ' + \
                 df_show['dec'].astype(str) + \
                 '<br>Vmag: ' + df_show['Vmag'].astype(str)

data = []

star_data = go.Scatterpolar(r= 90-df_show['alt'].values,
                            theta=df_show['az'].values,
                            mode='markers',
                            marker=star_marker,
                            hovertext=star_hovertext,
                            hoverinfo='text',
                            showlegend=False)

for e in edges:
    th1 = df.loc[e[0]]['az']
    r1  = 90 - df.loc[e[0]]['alt']
    th2 = df.loc[e[1]]['az']
    r2  = 90 - df.loc[e[1]]['alt']
    cosnt_data = go.Scatterpolar(r=[r1,r2],
                                 theta=[th1,th2],
                                 mode='lines',
                                 line={'color':'blue'},
                                 showlegend=False,
                                 #name='',
                                 hoverinfo='skip')
    data.append(cosnt_data)

data.append(star_data)

fig = go.Figure(data=data)



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

fig.write_html('01.html', auto_open=True)



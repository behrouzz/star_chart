# https://plotly.com/python/reference/scatterpolar/
# https://plotly.com/python/reference/layout/polar/
# https://plotly.com/python/reference/layout/


from hypatie.data import cities
from datetime import datetime
import skychart as sch
import plotly.graph_objects as go
import pandas as pd
from utils import get_const_data, get_star_data
from plots import show_chart

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

# otypes
from hypatie.simbad_otypes import text
from io import StringIO
ot = pd.read_csv(StringIO(text), header=0, names=['_','short','long'])
del ot['_']
df = df.reset_index()
df = pd.merge(df, ot, how='left', left_on='otype_txt', right_on='short')
del df['short']
df = df.set_index('hip')

#-----------------

df.loc[df['NAME'].notnull(), 'name'] = df['main_id'] + ' | ' + df['NAME']
df.loc[df['NAME'].isna(), 'name'] = df['main_id']

                     
df_show = df[df['Vmag']<5]
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
               'sizemin':0.1,
               'color': df_show['rgb'],
               'opacity':1,
               'line':{'width':0}}

star_hovertext = '<b>'+df_show['name']+ '</b><br>' + '<i>'+df_show['long']+'</i><br>' + \
                 'ra: ' +  df_show['ra'].astype(str) + '<br>dec: ' + \
                 df_show['dec'].astype(str) + \
                 '<br>Vmag: ' + df_show['Vmag'].astype(str) + \
                 '<br>Temperature: ' + df_show['temperature'].astype(int).astype(str)


#data = get_const_data(edges, df)
#data.append(get_star_data(df_show, star_marker, star_hovertext))
#fig = show_chart(data, title)
fig = go.Figure()
fig = get_const_data(fig, edges, df)
fig = get_star_data(fig, df_show, star_marker, star_hovertext)
fig = show_chart(fig, title)




fig.write_html('01.html', auto_open=True)



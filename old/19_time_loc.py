#from hypatie.data import cities
from datetime import datetime
import skychart as sch
import plotly.graph_objects as go
import pandas as pd

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from hypatie.simbad_otypes import text
from io import StringIO
from locations import locs
from embeds import angularaxis, radialaxis

df_loc = pd.read_csv(StringIO(locs))
hip7 = pd.read_csv('hip7.csv')
ot = pd.read_csv(StringIO(text), header=0, usecols=[1,2], names=['short','long'])


app = dash.Dash(__name__)

app.layout = html.Div([html.Label('Time (UTC): '),
                       dcc.Input(id='inp_time',
                                 type='text',
                                 value=datetime.strftime(datetime.utcnow(), '%d/%m/%Y - %H:%M'),
                                 debounce=True),
                       dcc.Graph(id='chart')])


@app.callback(
    Output(component_id='chart', component_property='figure'),
    Input(component_id='inp_time', component_property='value')
)

def update_plot(t):
    time = datetime.strptime(t, '%d/%m/%Y - %H:%M')

    city = 'Strasbourg'
    df_city = df_loc[df_loc['city']==city]
    obs_loc = (df_city['lon'].iloc[0], df_city['lat'].iloc[0])

    df_orig = sch.visible_hipparcos(obs_loc, time) #should be changed
    df = df_orig.copy(deep=True)
    if t:
        my_df = hip7.copy(deep=True)
        my_df = my_df.set_index('hip')
        my_df = my_df.loc[df.index]
        my_df = pd.merge(my_df.reset_index(), df[['alt','az']].reset_index(), how='left', on='hip')
        df = my_df.set_index('hip')

    # otypes
    df = pd.merge(df.reset_index(), ot, how='left', left_on='otype_txt', right_on='short')
    del df['short']
    df = df.set_index('hip')

    #-----------------

    df.loc[df['NAME'].notnull(), 'name'] = df['main_id'] + ' | ' + df['NAME']
    df.loc[df['NAME'].isna(), 'name'] = df['main_id']

                         
    df_show = df[df['Vmag']<5]
    dc_const = sch.load_constellations()
    edges = sch.create_edges(dc_const)

    edges = [i for i in edges if (i[0] in df.index) and (i[1] in df.index)]

    now_date = time.isoformat()[:10]
    now_time = time.isoformat()[11:16]
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
                                     line={'color':'gray'},
                                     showlegend=False,
                                     #name='',
                                     hoverinfo='skip',
                                     opacity=0.5)
        data.append(cosnt_data)

    data.append(star_data)

    fig = go.Figure(data=data)





    fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis})

    fig.update_layout(title=title, height=1000, width=1000, template='plotly_dark')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

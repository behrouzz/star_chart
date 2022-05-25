from datetime import datetime
import pandas as pd

import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from embeds import angularaxis, radialaxis, create_star_marker_hover, create_gal_marker_hover, create_ss_marker_hover
from styles import *
from constellations import const_str
from tools import load_constellations, radec_to_altaz, create_edges, SS_GCRS

from numeph import load_pickle

df_loc = pd.read_csv('data/locations.csv')
cnt_ls = list(df_loc['country'].unique())
hip7 = pd.read_csv('data/hip7.csv')
dc_const = load_constellations(const_str)
all_edges = create_edges(dc_const)
df_gal = pd.read_csv('data/galaxiesV10.csv')
dc = load_pickle('data/de440s_2020_2030.pickle')


app = dash.Dash(__name__)

app.layout = html.Div([dcc.Dropdown(id='cnt_dd', options=[{'label':i, 'value':i} for i in cnt_ls], style=dd1_style),
                       dcc.Dropdown(id='cit_dd', style=dd2_style),
                       html.Label('Time (UTC): ', style=dt1_style),
                       dcc.Input(id='inp_time',
                                 type='text',
                                 value=datetime.strftime(datetime.utcnow(), '%d/%m/%Y - %H:%M'),
                                 debounce=True, style=dt2_style),
                       html.Div(dcc.Slider(id='mag_slider',
                                  min=1, max=7,
                                  value=5,
                                  step=0.5,
                                  tooltip={"placement": "bottom", "always_visible": True},
                                  vertical=False),
                                  style={'width':'1000px'}),
                       dcc.Graph(id='chart')])


@app.callback(
    Output('cit_dd', 'options'),
    Input('cnt_dd', 'value'))

def update_city_dd(country):
    cnt = 'France'
    if country:
        cnt = country
    tmp_df = df_loc.copy(deep=True)
    tmp_df = tmp_df[['country', 'city']].drop_duplicates()
    city_options = tmp_df[tmp_df['country']==cnt]['city'].values.tolist()
    city_options = [{'label':i, 'value':i} for i in city_options]
    return city_options


@app.callback(
    Output(component_id='chart', component_property='figure'),
    Input(component_id='inp_time', component_property='value'),
    Input(component_id='cit_dd', component_property='value'),
    Input(component_id='mag_slider', component_property='value')
)

def update_plot(t, inp_city, inp_mag_max):
    city = 'Strasbourg'
    if inp_city:
        city = inp_city
    df_city = df_loc[df_loc['city']==city]

    time = datetime.utcnow().strftime('%d/%m/%Y - %H:%M')
    if t:
        time = datetime.strptime(t, '%d/%m/%Y - %H:%M')
    
    if inp_mag_max:
        mag_max = inp_mag_max

    title = '<b>'+city.title()+'</b>'+'<br>'+\
            time.isoformat()[:10]+'<br>'+\
            time.isoformat()[11:16] +' UTC'+'<br>'+\
            '<i>Max mag: '+ str(mag_max)+'</i>'
    
    lon, lat = df_city['lon'].iloc[0], df_city['lat'].iloc[0]

    # Base DataFrame (hip7 above horizon)
    df = hip7.copy(deep=True)
    df['alt'], df['az'] = radec_to_altaz(lon, lat, df['ra'], df['dec'], time)
    df = df[df['alt']>0]
    df = df.set_index('hip')

    #=================================================
    data = []
    
    # CONSTELLATIONS ------------------------
    
    edges = all_edges.copy()
    edges = [i for i in edges if (i[0] in df.index) and (i[1] in df.index)]

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
    
    # STARS ---------------------------------

    df_show = df[df['Vmag']<mag_max].reset_index()
    
    star_marker, star_hovertext = create_star_marker_hover(df_show)

    star_data = go.Scatterpolar(r= 90-df_show['alt'].values,
                                theta=df_show['az'].values,
                                mode='markers',
                                marker=star_marker,
                                hovertext=star_hovertext,
                                hoverinfo='text',
                                showlegend=False)



    
    # GALAXIES ---------------------------------
    df_gal_tmp = df_gal.copy(deep=True)
    df_gal_tmp['alt'], df_gal_tmp['az'] = radec_to_altaz(lon, lat, df_gal_tmp['ra'], df_gal_tmp['dec'], time)
    df_gal_tmp = df_gal_tmp[df_gal_tmp['alt']>0]
    df_gal_tmp = df_gal_tmp[df_gal_tmp['Vmag']<mag_max]

    gal_marker, gal_hovertext = create_gal_marker_hover(df_gal_tmp)

    gal_data = go.Scatterpolar(r= 90-df_gal_tmp['alt'].values,
                                theta=df_gal_tmp['az'].values,
                                mode='markers',
                               marker_symbol='diamond-wide',
                                marker=gal_marker,
                                hovertext=gal_hovertext,
                                hoverinfo='text',
                                showlegend=False)

    # SOLAR SYSTEM ----------------------------
    
    ss = SS_GCRS(dc, time)
    df_ss = ss.altaz((lon, lat))
    df_ss = df_ss[df_ss['alt']>=0]

    ss_marker, ss_hovertext = create_ss_marker_hover(df_ss)

    ss_data = go.Scatterpolar(r= 90-df_ss['alt'].values,
                            theta=df_ss['az'].values,
                            mode='markers',
                           marker_symbol='circle-cross',
                            marker=ss_marker,
                            hovertext=ss_hovertext,
                            hoverinfo='text',
                            showlegend=False)
    
    #---------------------------------

    data.append(star_data)
    data.append(gal_data)
    data.append(ss_data)
    
    fig = go.Figure(data=data)
    
    fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis})

    fig.update_layout(title=title, height=1000, width=1000, template='plotly_dark')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

from datetime import datetime, date
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from embeds import *
from styles import *
from constellations import const_str
from tools import load_constellations, radec_to_altaz, create_edges, SS_GCRS
from hypatie.solar_system import load_pickle
from PIL import Image

img = Image.open('static/ads.jpg')
df_loc = pd.read_csv('static/locations.csv')
cnt_ls = list(df_loc['country'].unique())
hip7 = pd.read_csv('static/hip7.csv')
dc_const = load_constellations(const_str)
all_edges = create_edges(dc_const)
df_gal = pd.read_csv('static/galaxiesV10.csv')
dc = load_pickle('static/de440s_2020_2030.pickle')



app = dash.Dash(__name__,
                assets_url_path='static',
                assets_folder='static', title='Sky | AstroDataScience')
server = app.server

# DropDowns
dd_country = dcc.Dropdown(id='cnt_dd', options=[{'label':i, 'value':i} for i in cnt_ls],
                          placeholder='Country', className='cnt-cit')
dd_city = dcc.Dropdown(id='cit_dd', placeholder='City', className='cnt-cit')

dd_hour = dcc.Dropdown(id='t_hour', options=[{'label':str(i).zfill(2), 'value':str(i).zfill(2)} for i in range(24)],
                       placeholder='HH', style=hhmm_style)
dd_minute = dcc.Dropdown(id='t_minute', options=[{'label':str(i).zfill(2), 'value':str(i).zfill(2)} for i in range(60)],
                         placeholder='MM', style=hhmm_style)


app.layout = html.Div([html.Div(className='cnt-cit-div',
                                children=[dd_country, dd_city,
                                          html.P('.', style={'color':'white'}), html.Br(style={'display': 'block'})]),

                       # Date & Time
                       html.Div([# Date
                            html.Label('Date (UTC): ', className='brown'),
                            dcc.DatePickerSingle(
                               id='inp_date',
                               min_date_allowed=date(2020, 1, 1),
                               max_date_allowed=date(2030, 12, 31),
                               date=date.today(),
                               display_format='DD/MM/YYYY'),
                            html.Code(' <> '),
                            
                            # Time
                            html.Label('Time (UTC): ', className='brown'),
                            dd_hour,
                            html.Code(':'),
                            dd_minute,
                            html.Br(style={'display': 'block'}),
                            html.P('Maximum apparent magnitude:', className='mag'),
                            ]),
                       
                       html.Div(dcc.Slider(id='mag_slider',
                                           min=1, max=7,
                                           value=5,
                                           step=0.5,
                                           tooltip={"placement": "bottom", "always_visible": True},
                                           vertical=False),
                                style={'width':'1000px'}),
                       dcc.Graph(id='chart',
                                 config={'scrollZoom': False})]) # NEW


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
    Input(component_id='inp_date', component_property='date'),
    Input(component_id='t_hour', component_property='value'),
    Input(component_id='t_minute', component_property='value'),
    Input(component_id='cit_dd', component_property='value'),
    Input(component_id='mag_slider', component_property='value')
)

def update_plot(dt, hr, mn, inp_city, inp_mag_max):
    city = 'Strasbourg'
    if inp_city:
        city = inp_city
    df_city = df_loc[df_loc['city']==city]

    time = datetime.utcnow()
    if (dt is not None) and (hr is not None) and (mn is not None):
        dt_hr_mn = dt + 'T' + hr+':'+mn
        time = datetime.strptime(dt_hr_mn, '%Y-%m-%dT%H:%M') # movaqat
    
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

    #------------------------------------------
    data.append(star_data)
    data.append(gal_data)
    
    # SOLAR SYSTEM ----------------------------
    
    ss = SS_GCRS(dc, time)
    df, df_s, df_m, df_p = ss.final((lon, lat))

    df_s = df_s[df_s['alt']>=0]
    df_m = df_m[df_m['alt']>=0]
    df_p = df_p[df_p['alt']>=0]

    if len(df_s) > 0:
        sun_marker, sun_hovertext = create_sun_marker_hover(df_s)
        sun_data = go.Scatterpolar(r= 90-df_s['alt'].values,
                                   theta=df_s['az'].values,
                                   mode='markers+text', # new
                                   marker_symbol='circle-cross',
                                   marker=sun_marker,
                                   hovertext=sun_hovertext,
                                   hoverinfo='text',
                                   text='Sun', textposition="top center", # new
                                   showlegend=False)
        data.append(sun_data)

    if len(df_m) > 0:
        moon_marker, moon_hovertext = create_moon_marker_hover(df_m)
        moon_data = go.Scatterpolar(r= 90-df_m['alt'].values,
                                    theta=df_m['az'].values,
                                    mode='markers+text', # new
                                    marker_symbol='circle-cross',
                                    marker=moon_marker,
                                    hovertext=moon_hovertext,
                                    hoverinfo='text',
                                    text='Moon', textposition="top center", # new
                                    showlegend=False)
        data.append(moon_data)

    if len(df_p) > 0:
        p_marker, p_hovertext = create_planets_marker_hover(df_p)
        p_data = go.Scatterpolar(r= 90-df_p['alt'].values,
                                 theta=df_p['az'].values,
                                 mode='markers+text', # new
                                 marker_symbol='circle-cross',
                                 marker=p_marker,
                                 hovertext=p_hovertext,
                                 hoverinfo='text',
                                 text=df_p.index.str[:3], textposition="top center", # new
                                 showlegend=False)
        data.append(p_data)
        

    
    #---------------------------------


    
    fig = go.Figure(data=data)
    
    fig.update_polars({'angularaxis':angularaxis, 'radialaxis':radialaxis})

    fig.update_layout(title=title, height=1000, width=1000, template='plotly_dark',
                      #dragmode=False, # NEW
                      )

    fig.add_layout_image(
    dict(
        source=img,
        xref="paper", yref="paper",
        x=0.95, y=1.07,
        sizex=0.1, sizey=0.1,
        opacity=1
    )
)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

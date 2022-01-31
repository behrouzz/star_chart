# https://plotly.com/python/reference/scatterpolar/
# https://plotly.com/python/reference/layout/polar/
# https://plotly.com/python/reference/layout/


from hypatie.data import cities
from datetime import datetime
import skychart as sch
import plotly.graph_objects as go
import pandas as pd



import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import date

app = dash.Dash(__name__)

app.layout = html.Div([html.Div([html.H3('Select date:'),
                                 dcc.DatePickerSingle(id='sale_date',
                                                      min_date_allowed=date(2020,1,1),
                                                      max_date_allowed=date(2030,1,1),
                                                      date=date(2022,1,27),
                                                      initial_visible_month=date(2022,1,27),
                                                      style={'width':'200px', 'margin':'0 auto'})]
                                ),
                       html.Div([dcc.Graph(id='sales_cat')])
                       ])


@app.callback(
    Output(component_id='sales_cat', component_property='figure'),
    Input(component_id='sale_date', component_property='date')
)

def update_plot(t):
    time = [int(i) for i in t.split('-')]
    time = datetime(time[0], time[1], time[2])

    def my_own_df(df):
        my_df = pd.read_csv('hip7.csv').set_index('hip')
        my_df = my_df.loc[df.index]
        my_df = pd.merge(my_df.reset_index(), df[['alt','az']].reset_index(), how='left', on='hip')
        my_df = my_df.set_index('hip')
        return my_df

    city = 'strasbourg'

    #t = datetime.now()
    #t = datetime(2022, 1, 19, 22)
    obs_loc = cities[city][:2]

    df_orig = sch.visible_hipparcos(obs_loc, time)
    df = df_orig.copy(deep=True)
    if t:
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

    now_date = time.isoformat()[:10]
    now_time = time.isoformat()[11:16]
    title = '<b>'+city.title()+'</b>' + '<br>' + now_date + '<br>' + now_time

    #=================================================

    df_show = df_show.reset_index()
    df_show['hip'] = 'HIP ' + df_show['hip'].astype(str)

    marker_size = (1 + (df_show['Vmag'].max() - df_show['Vmag'].values))**1.7

    import plotly.express as px

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

    #fig.write_html('01.html', auto_open=True)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)

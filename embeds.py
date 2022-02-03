def create_star_marker_hover(df_show):
    # star_marker
    marker_size = (1 + (df_show['Vmag'].max() - df_show['Vmag'].values))**1.7
    star_marker = {'size': marker_size,
                   'sizemode':'area',
                   'sizeref':2.*max(marker_size)/(8.**2),
                   'sizemin':0.1,
                   'color': df_show['rgb'],
                   'opacity':1,
                   'line':{'width':0}}
    # star_hover
    star_hovertext = '<b>'+df_show['name']+ '</b><br>' + \
                     '<i>'+df_show['long']+'</i><br>' + \
                     'RA: ' + df_show['ra'].apply(lambda x: round(x,5)).astype(str) + ' <i>(deg)</i><br>' + \
                     'DEC: ' + df_show['dec'].apply(lambda x: round(x,5)).astype(str) + ' <i>(deg)</i><br>' + \
                     'Vmag: ' + df_show['Vmag'].astype(str) + '<br>' + \
                     'Parallax: ' + df_show['plx'].astype(str) + ' <i>(mas)</i><br>' + \
                     'Temperature: ' + df_show['temp'] + ' <i>(°K)</i>'
    
    return star_marker, star_hovertext

def create_gal_marker_hover(df):
    marker = {'color': 'rgb(255,0,0)'}
    hovertext = '<b>'+df['name']+ '</b><br>' + \
                '<i>'+df['long']+'</i><br>' + \
                'RA: ' + df['ra'].apply(lambda x: round(x,5)).astype(str) + ' <i>(deg)</i><br>' + \
                'DEC: ' + df['dec'].apply(lambda x: round(x,5)).astype(str) + ' <i>(deg)</i><br>' + \
                'Vmag: ' + df['Vmag'].astype(str) + '<br>' + \
                'Redshift: ' + df['z'].astype(str) + '<br>' + \
                'Radial Velocity: ' + df['radvel'].astype(str) + ' <i>(km/s)</i><br>' + \
                'Distance: ' + df['dist_pc'].astype(str) + ' <i>(pc)</i>'
    return marker, hovertext

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

dd1_style = {'width':'250px',
             'background-color':'black',
             'color':'blue'}

dd2_style = {'width':'250px',
             'background-color':'black',
             'color':'blue'}

dt1_style = {#'width':'150px',
             'height':'20px',
             'background-color':'black',
             'color':'white'}

dt2_style = {'width':'115px',
             'height':'20px',
             'background-color':'black',
             'color':'white'}
#{'display':'inline-block'}

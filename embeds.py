def create_star_marker_hover(df):
    # star_marker
    marker_size = (1 + (df['Vmag'].max() - df['Vmag'].values))**1.7
    marker = {'size': marker_size,
              'sizemode':'area',
              'sizeref':2.*max(marker_size)/(8.**2),
              'sizemin':0.1,
              'color': df['rgb'],
              'opacity':1,
              'line':{'width':0}}
    # star_hover
    hovertext = '<b>'+df['name']+'</b><br>' + \
                '<i>'+df['long']+'</i><br>' + \
                'RA: '+df['ra'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'DEC: '+df['dec'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'Vmag: '+df['Vmag'].astype(str)+'<br>' + \
                'Parallax: '+df['plx'].astype(str)+' <i>(mas)</i><br>' + \
                'Temperature: '+df['temp']+' <i>(°K)</i>'
    
    return marker, hovertext


def create_sun_marker_hover(df):
    # sun_marker
    marker = {'size': 20,
              'sizemode':'area',
              'color': 'rgb(255,255,0)',
              'opacity':1,
              'line':{'width':0.5}}
    # sun_hover
    hovertext = '<b>'+'Sun'+'</b><br>' + \
                'RA: '+df['ra'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'DEC: '+df['dec'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>'
    return marker, hovertext

def create_moon_marker_hover(df):
    # moon_marker
    marker = {'size': 18,
              'sizemode':'area',
              'color': 'rgb(255,255,255)',
              'opacity':1,
              'line':{'width':0.5}}
    # moon_hover
    hovertext = '<b>'+'Moon'+'</b><br>' + \
                'RA: '+df['ra'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'DEC: '+df['dec'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'Elognation: '+df['elognation'].apply(lambda x: int(x)).astype(str)+' <i>(deg)</i><br>' + \
                'Phase: '+df['phase'].apply(lambda x: int(x)).astype(str)+' <i>%</i><br>'
    return marker, hovertext


def create_planets_marker_hover(df):
    #marker_size = df['diam']
    marker_size = (1 + (df['mag'].max() - df['mag'].values))**1.7
    # planets_marker
    marker = {'size': marker_size,
              'sizemode':'area',
              'sizeref':2.*max(marker_size)/(8.**2.2),
              'sizemin':0.1,
              'color': df['color'],
              'opacity':1,
              'line':{'width':0}}
    # planets_hover
    hovertext = '<b>'+df.index.str.title()+'</b><br>' + \
                'RA: '+df['ra'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'DEC: '+df['dec'].apply(lambda x: round(x,5)).astype(str)+' <i>(deg)</i><br>' + \
                'Elognation: '+df['elognation'].apply(lambda x: int(x)).astype(str)+' <i>(deg)</i><br>' + \
                'Phase: '+df['phase'].apply(lambda x: int(x)).astype(str)+' <i>%</i><br>' + \
                'Apparent magnitude : '+df['mag'].apply(lambda x: round(x,1)).astype(str)+'<br>' + \
                'Diameter : '+df['diam'].apply(lambda x: round(x,1)).astype(str)+' <i>(arcsec)</i><br>'
    return marker, hovertext


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

dd1_style = {'width':'250px', 'color':'blue'}
dd2_style = {'width':'250px', 'color':'blue', 'display':'inline-block'}

dt_lb_style = {'color':'brown'}
tt_lb_style = {'color':'brown'}

hour_style = {'width':'50px',
              'font-size':'14px',
              'vertical-align':'middle',
              'color':'blue', 'display':'inline-block'}

minute_style = {'width':'50px',
                'font-size':'14px',
                'vertical-align':'middle',
                'color':'blue', 'display':'inline-block'}

#{'display':'inline-block'}

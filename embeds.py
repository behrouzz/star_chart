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
    #df_show.loc[df_show['temperature'].notnull(), 'temp'] = df_show[df_show['temperature'].notnull()].astype(int).astype(str)
    df_show.loc[df_show['temperature'].isna(), 'temp'] = 'NA'
    
    star_hovertext = '<b>'+df_show['name']+ '</b><br>' + \
                     '<i>'+df_show['long']+'</i><br>' + \
                     'RA: ' + df_show['ra'].apply(lambda x: round(x,5)).astype(str) + '<br>' + \
                     'DEC: ' + df_show['dec'].apply(lambda x: round(x,5)).astype(str) + '<br>' + \
                     'Vmag: ' + df_show['Vmag'].astype(str) + '<br>' + \
                     'Temperature: ' + df_show['temp'].astype(str)
    
    return star_marker, star_hovertext


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



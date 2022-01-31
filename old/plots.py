import plotly.graph_objects as go

def show_chart(fig, title='', height=1000, width=1000):
    #fig = go.Figure(data=data)

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
    fig.update_layout(title=title, height=height, width=width, template='plotly_dark')
    return fig


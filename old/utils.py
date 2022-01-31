import plotly.graph_objects as go

def get_const_data(fig, edges, df):
    #cosnt_data = []
    for e in edges:
        th1 = df.loc[e[1]]['az']
        r1  = 90 - df.loc[e[1]]['alt']
        th2 = df.loc[e[2]]['az']
        r2  = 90 - df.loc[e[2]]['alt']
        tr = go.Scatterpolar(
            r=[r1,r2],
            theta=[th1,th2],
            mode='lines',
            line={'color':'gray'},
            showlegend=False,
            name=e[0],#
            legendgroup=e[0],#
            hoverinfo='skip',#
            opacity=0.5)
        fig.add_trace(tr)
    return fig

def get_star_data(fig, df_show, star_marker, star_hovertext):
    tr = go.Scatterpolar(
        r= 90-df_show['alt'].values,
        theta=df_show['az'].values,
        mode='markers',
        marker=star_marker,
        hovertext=star_hovertext,
        hoverinfo='text',
        showlegend=False,
        legendgroup='Stars')
    fig.add_trace(tr)
    return fig

def create_edges(dc):
    edges = []
    for k,v in dc.items():
        for i in v:
            edges.append((k, i[0], i[1]))
    return edges

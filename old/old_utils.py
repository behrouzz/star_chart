import plotly.graph_objects as go

def get_const_data(edges, df):
    cosnt_data = []
    for e in edges:
        th1 = df.loc[e[0]]['az']
        r1  = 90 - df.loc[e[0]]['alt']
        th2 = df.loc[e[1]]['az']
        r2  = 90 - df.loc[e[1]]['alt']
        edge_data = go.Scatterpolar(
            r=[r1,r2],
            theta=[th1,th2],
            mode='lines',
            line={'color':'gray'},
            showlegend=False, #name='',
            hoverinfo='skip',
            opacity=0.5)
        cosnt_data.append(edge_data)
    return cosnt_data

def get_star_data(df_show, star_marker, star_hovertext):
    star_data = go.Scatterpolar(
        r= 90-df_show['alt'].values,
        theta=df_show['az'].values,
        mode='markers',
        marker=star_marker,
        hovertext=star_hovertext,
        hoverinfo='text',
        showlegend=False)
    return star_data

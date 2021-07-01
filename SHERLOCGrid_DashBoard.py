import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from textwrap import dedent as d
from PIL import Image
import numpy as np

#Set argumments here
base_folder = '/export/data6/M2020/SHERLOC/SHERLOC_DOWNLINK/Bi_la_sana/0098/Processed'
file_name = 'SS__0098_0675637642_495RLS__0040136SRLC10203_308___J02'
ConImg = 'SC3_0098_0675636936_460FDR_N0040136SRLC10203_0000LUJ01.png'
###_____________________________________________________
processed_file = file_name + '_baselined_grid_final.csv'
wave_file = file_name + '_waves.csv'
raw_file = file_name + '_raw_grid.csv'
baseline_file = file_name + '_baselines_grid.csv'
img_path = base_folder + '/' + ConImg

image = Image.open(img_path,'r')
array_img = np.asarray(image)
datafile = pd.read_csv(base_folder + '/' + processed_file)
rawfile =pd.read_csv(base_folder + '/' + raw_file)
baselinefile =pd.read_csv(base_folder + '/' + baseline_file)

wavefile = pd.read_csv(base_folder + '/' + wave_file)
waves = list(wavefile['2'])
laser_wave = 248.6
ramanshift = [(1.0/laser_wave - 1.0/wv)*10**7 for wv in waves]

df = pd.DataFrame()
df['x'] = datafile['x']
df['y'] = datafile['y']
df['index'] = list(datafile.index)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

s1 = 700
s = s1 * 0.75
s2 = 750
s3 = 250

# Add images
fig = px.scatter(df, x="x", y="y", custom_data=["index"], width=s1, height=s)

fig.update_xaxes(range=[0, len(array_img[0])])
fig.update_yaxes(range=[len(array_img),0])

fig.add_layout_image(
        dict(
            source=image,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=len(array_img[0]),
            sizey=len(array_img),
            opacity=1,
            layer="below")
)


# Set templates
fig.update_layout(template="plotly_white")
fig.update_layout(clickmode='event+select')

fig.update_traces(marker_size=8)

fig_empty = px.line(width=s2, height=s3)
fig_empty.update_xaxes(range=[200, 2000])
fig_empty.update_yaxes(range=[-200, 400])
fig_empty.update_layout(
margin=dict(
    t=30, # top margin: 30px, you want to leave around 30 pixels to
          # display the modebar above the graph.
    b=10, # bottom margin: 10px
    l=10, # left margin: 10px
    r=30, # right margin: 10px
),
# Some more layout options
)


app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='grid_fig', figure=fig
        )
    ], style={'width': '45%', 'display': 'inline-block','padding': '0 20'}),

    html.Div([
        dcc.Graph(id='baseline_fig', figure=fig_empty),
        dcc.Graph(id='raman_fig', figure=fig_empty)
    ], style={'display': 'inline-block', 'width': '49%'}),


    html.Div(className='row', children=[

        html.Div([
            dcc.Markdown(d("""
              Click on points in the graph.
            """)),
            html.Pre(id='hover-data', style=styles['pre']),
        ], className='three columns'),

    ])
])


@app.callback(
    Output('hover-data', 'children'),
    [Input('grid_fig', 'hoverData')])

def display_hover_data(hoverData):
    return json.dumps({'spectrum no.' : hoverData['points'][0]['pointIndex']}, indent = 2)

@app.callback(
    dash.dependencies.Output('raman_fig', 'figure'),
    [dash.dependencies.Input('grid_fig', 'hoverData')])

def update_x_timeseries(hoverData):

    dff = pd.DataFrame()
    dff['ramanshift'] = ramanshift

    index = hoverData['points'][0]['pointIndex']

    y = list(datafile.T[index][1:2049])

    dff['spectrum'] = y

    fig = px.line(dff, x='ramanshift', y='spectrum', width=s2, height=s3)
    fig.update_xaxes(range=[200, 2000])
    #fig.update_yaxes(range=[-200, 300])

    fig.update_layout(
    margin=dict(
        t=10, # top margin: 30px, you want to leave around 30 pixels to
              # display the modebar above the graph.
        b=10, # bottom margin: 10px
        l=10, # left margin: 10px
        r=30, # right margin: 10px
    ),
    # Some more layout options
    )

    return fig

@app.callback(
    dash.dependencies.Output('baseline_fig', 'figure'),
    [dash.dependencies.Input('grid_fig', 'hoverData')])

def update_y_timeseries(hoverData):

    dff = pd.DataFrame()
    dff['ramanshift'] = ramanshift

    index = hoverData['points'][0]['pointIndex']

    y = list(rawfile.T[index][1:])
    z = list(baselinefile.T[index][1:])

    dff['raw spectrum'] = y
    dff['baseline'] = z

    fig = px.line(dff, x='ramanshift', y=dff.columns[1:], width=s2, height=s3)
    fig.update_xaxes(range=[200, 2000])

    fig.update_layout(
        legend=dict(
            x=0.8,
            y=.1,
            )
        )
    fig.update_layout(
    margin=dict(
        t=30, # top margin: 30px, you want to leave around 30 pixels to
              # display the modebar above the graph.
        b=10, # bottom margin: 10px
        l=10, # left margin: 10px
        r=30, # right margin: 10px
    ),
    # Some more layout options
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)

import dash
from sklearn import preprocessing
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.tools as tls
from datetime import datetime
import timeit
from timeit import default_timer as timer
from analyse import *
from signal_processing import *
from get_data import *
#from hilbert_huang_transform import *

print(dcc.__version__) # 0.6.0 or above is required

app = dash.Dash()

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')


])
height  = 480
title = "Dashboard"
page1_title = "HHT"
page2_title = "FFT"
home = "Home"
button_width = 300
import base64
# image_filename = 'assets/thruster2.PNG' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())
index_page = html.Div([
     html.Div([
            html.H2("{}".format(title),className="dash-title"),
    ], className='banner'),

    html.Br(),

    html.Div([

    html.Div([
    html.A(html.Button('Fourier Transform', className='three columns',
    style={'backgroundColor':'#42C4F7','width':'{}'.format(button_width)},
    ),
    href='/{}'.format(page2_title)),
    ],style={'float':'left'}),
    html.Div([
    html.A(html.Button('Hilbert Huang Transform', className='three columns',
    style={'backgroundColor':'#42C4F7','width':'{}'.format(button_width),
    },
    ),
    href='/{}'.format(page1_title)),
    ],style={'float':'left','clear':'left'}),

    html.Div([
    html.A(html.Button('Wavelet Transform', className='three columns',
    style={'backgroundColor':'#42C4F7','width':'{}'.format(button_width),
    },
    ),
    href='/{}'.format(page2_title)),
    ],style={'float':'left','clear':'left'}),

    html.Div([
    html.A(html.Button('Deep learning', className='three columns',
    style={'backgroundColor':'#42C4F7','width':'{}'.format(button_width),
    },
    ),
    href='/{}'.format(page2_title)),
    ],style={'float':'left','clear':'left'}),

    ],id="wraper"),

    # html.Div([
    # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()) ),
    # ],style={'margin-top':30}),


])

##############################################################################
# page 1: wavelet page.
page_1_layout = html.Div([
    html.Div([
           html.H2("{}".format(title),className="dash-title"),
   ], className='banner'),
   # Home button
   html.Div([
       html.A(html.Button('Home', className='three columns',
       style={'backgroundColor':'#42C4F7',
       'width':150}),
       href='/{}'.format(home)),
       html.A(html.Button('FFT', className='three columns',
       style={'backgroundColor':'#42C4F7',
       'width':150}),
       href='/{}'.format(page2_title)),
       html.Br(),
       html.Div([
       ]),
   ]),
   html.Br(),
   html.Br(),

   #dates drop down
   dcc.Dropdown(
       id='hht-date',
       placeholder="Select a sample",
       options=[{'label':str(date), 'value':str(date)} for date in get_dates()[:-16]],
       value=get_dates()[0]
   ),
   html.Br(),
   #bearing selection Dropdown
   dcc.RadioItems(
       id = "hht-bearings",
       options=[
           {'label': 'Bearing 1', 'value': 0},
           {'label': 'Bearing 2', 'value': 1},
           {'label': 'Bearing 3', 'value': 2},
           {'label': 'Bearing 4', 'value': 3},

       ],
       value=0,
       labelStyle={'display': 'inline-block'}
       ),
    # graph selection
    dcc.Checklist(
    id = "hht-imfs",
    options=[
        {'label': 'Intrinsic Mode Functions', 'value': 0},
        {'label': 'IQR', 'value': 1},
    ],
    values=[0],
    labelStyle={'display': 'inline-block'}
    ),
    html.Br(),
    dcc.Dropdown(
        id='all-imfs',
        placeholder="Select an imf",
    ),
    # graph container
    html.Br(),
    html.Br(),
    html.Div(id="hht-graphs")

])




##############################################################################
#page 2: FFT
page_2_layout = html.Div([
    html.Div([
           html.H2("{}".format(title),className="dash-title"),
    ], className='banner'),
    html.Div([


        html.A(html.Button('Home', className='three columns',
        style={'backgroundColor':'#42C4F7',
        'width':150}),
        href='/{}'.format(home)),
        html.A(html.Button('HHT', className='three columns',
        style={'backgroundColor':'#42C4F7',
        'width':150}),
        href='/{}'.format(page1_title),style={}),
        html.Br(),
        html.Div([
        ]),
    ]),

    # html.Div(id='page-2-content'),
    html.Br(),
    html.Br(),
    # html.Div(id='output-container-date-picker-single',
    # style={'backgroundColor':'#4CAF50','width':300,'text-align':'center',
    # 'color':'white','font-size':18,'font-family':'Serif'}),
    html.Br(),
    dcc.Dropdown(
        id='dates',
        placeholder="Select a sample",
        options=[{'label':str(date), 'value':str(date)} for date in get_dates()[:-16]],
        value=get_dates()[0]
    ),
    # bearings selection radio button
    html.Br(),
    dcc.RadioItems(
        id = "bearings",
        options=[
            {'label': 'Bearing 1', 'value': 0},
            {'label': 'Bearing 2', 'value': 1},
            {'label': 'Bearing 3', 'value': 2},
            {'label': 'Bearing 4', 'value': 3},

        ],
        value=0,
        labelStyle={'display': 'inline-block'}
        ),
    html.Br(),
    # plot selection graphs
    dcc.Checklist(
    id = "checklist",
    options=[
        {'label': 'Envelop spectrum', 'value': 0},
        {'label': 'Overal acceleration', 'value': 1},
        {'label': 'Acceleration', 'value': 2},
    ],
    values=[0,1],
    labelStyle={'display': 'inline-block'}
    ),


    dcc.Checklist(
    id = "faults",
    options=[
        {'label': 'BPFO', 'value': 0},
        {'label': 'BPFI', 'value': 1},

    ],
    values=[0],
    labelStyle={'display': 'inline-block'}
    ),

    dcc.Checklist(
    id = "faults-amplitude",
    options=[
        {'label': 'BPFO Amplitude', 'value': 0},
        {'label': 'BPFI Amplitude', 'value': 1},

    ],
    values=[0],
    labelStyle={'display': 'inline-block'}
    ),



    dcc.RadioItems(
    id="radio",
    options=[
        {'label': 'Order', 'value': 0},
        {'label': 'Hz', 'value': 1},
    ],
    value=1,
    labelStyle={'display': 'inline-block','float':'right'}
    ),

    html.Br(),
    html.Br(),
    html.Div(id="graphs")
    ])



############################################################################
# hht call backs
@app.callback(Output('all-imfs','options'), [
Input('hht-date', 'value'),
Input('hht-bearings', 'value'),
])
def display_imfs_values(hht_date_name,hht_bearings_value):
    data = get_data(hht_date_name,hht_bearings_value)
    imfs = hilbert_huang_transform(data)
    m = len(imfs)
    return [{'label': i+1, 'value': i} for i in range(m)]




@app.callback(Output('hht-graphs','children'), [
Input('hht-date', 'value'),
Input('hht-bearings', 'value'),
Input('hht-imfs', 'values'),
Input('all-imfs', 'value'),
])
def display_graphs(hht_date_name,hht_bearings_value,
                hht_imfs_value,all_imfs_value):
    graphs = []
    k = hht_bearings_value
    label = "data points"
    hht_fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True,
    vertical_spacing=0.009,horizontal_spacing=0.009)
    hht_val = 0
    if hht_val in hht_imfs_value and isinstance(all_imfs_value, int):
        data = get_data(hht_date_name,k)
        imfs = hilbert_huang_transform(data)
        m = len(imfs)

        hht_fig.append_trace({'y':imfs[all_imfs_value],'type':'scatter','name':'imfs'},1,1)
        hht_fig['layout'].update(title='Bearing {}, {}th imf for {} with {} imfs'.format(k+1,
        all_imfs_value+1,
        hht_date_name,m))
        hht_fig['layout']['xaxis1'].update(dict(title='{}'.format(label)))
        hht_fig['layout']['yaxis1'].update(dict(title='Amplitude'))
        imfs = html.Div([
        dcc.Graph(
                figure = hht_fig,
                id='imfs',
                ),
                ],style={'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
                'margin-top':'20px'})

        graphs = [imfs]

    return graphs







################################################################################

#fft call backs

@app.callback(Output('graphs', 'children'), [
Input('checklist', 'values'),
Input(component_id='dates', component_property='value'),
 Input(component_id='radio', component_property='value'),
 Input(component_id='faults', component_property='values'),
  Input(component_id='bearings', component_property='value'),
  Input(component_id='faults-amplitude', component_property='values')
])
def display_graphs(checklist_value,date_name,radio_value,faults_value,
                   bearings_value,faults_amplitude_value):
    #checklist value
    graphs = []
    envelop_val = 0; overall_accel_val = 1; accel_val = 2;
    velocity_val = 3; velocity_spectrum_val = 4
    bpfo_val = 0
    bpfo_harmonic_value = 0
    bearing1_value = 0; bearing2_value = 1; bearing3_value = 2;
    bearing4_value = 3;
    bpfo_amp_val = 0
    if bearings_value == bearing1_value:
        k = 0
    elif bearings_value == bearing2_value:
        k = 1
    elif bearings_value == bearing3_value:
        k = 2
    elif bearings_value == bearing4_value:
        k = 3
    bearing_data = get_data(date_name,k)
    dates, rms = get_overall_accel(k)
    freq, amplitude = get_envelop_spectrum(bearing_data)
    if bpfo_amp_val in faults_amplitude_value:
        values = get_bpfo_amps(k)
    else:
        values = []

    signal = html.Div([
        dcc.Graph(
            id='signal',
            figure = {
                'data': [{
                    # 'x':dates,
                    'y': bearing_data,
                }],
                'layout': {
                    'title':'Bearing {} Acceleration for {}'.format(k+1,date_name),
                    'xaxis':{'title':'Time (ms)'},
                    'yaxis':{'title':'Acceleration'},
                    'height': height,
                }

            })
            ],style={'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'
            ,'margin-top':'20px'})


    label = "Frequency in Hz"
    envelop_fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True,
    vertical_spacing=0.009,horizontal_spacing=0.009)
    envelop_fig.append_trace({'x':freq[:500],'y':amplitude[:500],
    'type':'scatter','name':'Envelop'},1,1)
    if bpfo_val in faults_value:
        bpfo, bpfo_amp = BPFO(date_name,k)
        envelop_fig.append_trace({'x':bpfo,'y':bpfo_amp,
        'type':'scatter','name':'BPFO'},1,1)
    envelop_fig['layout'].update(title='Bearing {} envelop spectrum for {}'.format( k+1,
    date_name))
    envelop_fig['layout']['xaxis1'].update(dict(title='{}'.format(label)))
    envelop_fig['layout']['yaxis1'].update(dict(title='Amplitude'))
    envelop = html.Div([
    dcc.Graph(
    figure = envelop_fig,
    id='acceleration',
    ),
    ],style={'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)',
    'margin-top':'20px'})


    rms_graph = html.Div([
        dcc.Graph(
            id='signal',
            figure = {
                'data': [{
                    # 'x':dates,
                    'y': rms,
                }],
                'layout': {
                    'title':'Bearing {} Overall Acceleration with time'.format(k+1),
                    'xaxis':{'title':'Time index'},
                    'yaxis':{'title':'Magnitude'},
                    'height': height,
                }

            })
            ],style={'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'
            ,'margin-top':'20px'})



    bpfo_amp_graph = html.Div([
        dcc.Graph(
            id='bpfo_amp',
            figure = {
                'data': [{
                    # 'x':dates,
                    'y': values,
                }],
                'layout': {
                    'title':'Bearing {} BPFO Amplitude with time'.format(k+1),
                    'xaxis':{'title':'Time index'},
                    'yaxis':{'title':'Amplitude'},
                    'height': height,
                }

            })
            ],style={'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'
            ,'margin-top':'20px'})

    if accel_val in checklist_value and signal not in graphs:
        graphs.append(signal)
    if accel_val not in checklist_value:
        try:
            graphs.remove(signal)
        except:
            pass


    if envelop_val in checklist_value and envelop not in graphs:
        graphs.append(envelop)
    if envelop_val not in checklist_value:
        try:
            graphs.remove(envelop)
        except:
            pass


    if overall_accel_val in checklist_value and rms_graph not in graphs:
        graphs.append(rms_graph)
    if overall_accel_val not in checklist_value:
        try:
            graphs.remove(rms_graph)
        except:
            pass


    if bpfo_amp_val in checklist_value and bpfo_amp_graph not in graphs:
        graphs.append(bpfo_amp_graph)
    if bpfo_amp_val not in checklist_value:
        try:
            graphs.remove(bpfo_amp_graph)
        except:
            pass

    return graphs



















@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/{}'.format(page1_title):
        return page_1_layout
    elif pathname == '/{}'.format(page2_title):
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

# css and font style
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/737dc4ab11f7a1a8d6b5645d26f69133d97062ae/dash-wind-streaming.css",
                "https://fonts.googleapis.com/css?family=Raleway:400,400i,700,700i",
                "https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i"]
for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(port=9000,debug=True)

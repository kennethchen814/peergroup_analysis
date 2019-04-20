# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15

@author: kchen
"""

import pandas as pds
import dash
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Input, Output, State
import plotly_express as px
import numpy as np
import time


#external_stylesheets = ['https://codepen.io/chriddyp/pen/brPBPO.css']
data_source = pds.read_csv('alll_mixA_agg.csv')
data_source = data_source.sort_values(by = ['bank', 'Report_Date'])
max_date = data_source[data_source.RSSD == 852218].shape[0]
key = [x for x in range(max_date)]
value = [x for x in data_source[data_source.RSSD == 852218].Report_Date]
date_map = dict(zip(key, value))
data_map2 = dict(zip(value, key))
data_source['date_index'] = data_source.Report_Date.map(data_map2)

bank_lookup = {852218: 'JPMC',
               480228: 'BAC',
               451965: 'Wells',
               476810: 'Citi',
               75633: 'BMO',
               723112: 'FifthThird',
               504713: 'USBank',
               817824: 'PNC',
               112837: 'CapOne',
               497404: 'TD',
               541101: 'BNY',
               35301: 'StateStreet',
               852320: 'BBT',
               675332: 'SunTrust',
               2182786: 'Goldman',
               1456501: 'MS',
               280110: 'Key',
               212465: 'MUFG',
               3303298: 'Citizens',
               233031: 'Regions',
               1394676: 'AMEX',
               30810: 'Discover',
               12311: 'Huntington',
               60143: 'Comerica'}

rssd_list = [bank for bank in bank_lookup]

app = dash.Dash(__name__,static_file='assets')
server = app.server
app.config['suppress_callback_exceptions']=True

"""
------------------------------------------------------------------------------------------------------------------------------------
page1 layouts
"""
  

page_1 = html.Div([
    html.Div(
            className='four columns',
            children=[
                    html.Div(children=[
                            html.H5('Bank and Peers:',
                                    style={'border-bottom':'4px solid #C4C4CD', 'padding-top':20})]),
                    html.Div(children=[
                                html.H6('Bank:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':15}),
                                dcc.Dropdown(
                                            id='bank',
                                            options=[
                                                    {'label':'JPMorgan Chase', 'value':852218},
                                                    {'label':'Bank of America', 'value':480228},
                                                    {'label':'Wells Fargo', 'value':451965},
                                                    {'label':'Citigroup', 'value':476810},
                                                    {'label':'Bank of Montreal', 'value':75633},
                                                    {'label':'Fifth Third', 'value':723112},
                                                    {'label':'US Bank', 'value':504713},
                                                    {'label':'PNC', 'value':817824},
                                                    {'label':'Capital One', 'value':112837},
                                                    {'label':'TD Bank', 'value':497404},
                                                    {'label':'Bank of New York Mellon', 'value':541101},
                                                    {'label':'State Street', 'value':35301},
                                                    {'label':'BB&T', 'value':852320},
                                                    {'label':'Sun Trust', 'value':675332},
                                                    {'label':'Goldman Sachs', 'value':2182786},
                                                    {'label':'Morgan Stanley', 'value':1456501},
                                                    {'label':'Key Bank', 'value':280110},
                                                    {'label':'MUFG', 'value':212465},
                                                    {'label':'Citizens', 'value':3303298},
                                                    {'label':'Regions', 'value':233031},
                                                    {'label':'American Express', 'value':1394676},
                                                    {'label':'Discover', 'value':30810},
                                                    {'label':'Huntington', 'value':12311},
                                                    {'label':'Comerica', 'value':60143}
                                            ],
                                            value = 852218)
                                ],
                            ),
                    html.Div(children=[
                                        html.H6('Peers:',
                                                style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':20}
                                               ),
                                        dcc.Dropdown(
                                                    id='peers',
                                                    options=[
                                                            {'label':'JPMorgan Chase', 'value':852218},
                                                            {'label':'Bank of America', 'value':480228},
                                                            {'label':'Wells Fargo', 'value':451965},
                                                            {'label':'Citigroup', 'value':476810},
                                                            {'label':'Bank of Montreal', 'value':75633},
                                                            {'label':'Fifth Third', 'value':723112},
                                                            {'label':'US Bank', 'value':504713},
                                                            {'label':'PNC', 'value':817824},
                                                            {'label':'Capital One', 'value':112837},
                                                            {'label':'TD Bank', 'value':497404},
                                                            {'label':'Bank of New York Mellon', 'value':541101},
                                                            {'label':'State Street', 'value':35301},
                                                            {'label':'BB&T', 'value':852320},
                                                            {'label':'Sun Trust', 'value':675332},
                                                            {'label':'Goldman Sachs', 'value':2182786},
                                                            {'label':'Morgan Stanley', 'value':1456501},
                                                            {'label':'Key Bank', 'value':280110},
                                                            {'label':'MUFG', 'value':212465},
                                                            {'label':'Citizens', 'value':3303298},
                                                            {'label':'Regions', 'value':233031},
                                                            {'label':'American Express', 'value':1394676},
                                                            {'label':'Discover', 'value':30810},
                                                            {'label':'Huntington', 'value':12311},
                                                            {'label':'Comerica', 'value':60143}
                                                            ], 
                                                    value=[480228, 451965, 476810], multi=True
                                                    )
                                    ]
                            ),

                    
                    html.Div(children=[
                            html.H5('Plot Setting',
                                     style={'border-bottom':'4px solid #C4C4CD'})],
                                     style={'padding-top':20}),
                    html.Div(children=[
                                html.H6('X-Axis:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':15}),
                                dcc.Dropdown(
                                            id='x',
                                            options=[
                                                    {'label':'Average Loan Balance (in ths)', 'value':'avg_os'},
                                                    {'label':'Loan Loss Reserve (in ths)', 'value':'alll'},
                                                    {'label':'Loan Loss Reserve (in %)', 'value':'alll_rate'},
                                                    {'label':'Net Credit Loss (in ths)', 'value':'ncl'},
                                                    {'label':'Net Credit Loss (in %)', 'value':'ncl_rate'},
                                                    {'label':'ALLL / NCL Ratio', 'value':'alll_to_ncl'},
                                                    {'label':'ALLL / Non-accrual Ratio', 'value':'alll_to_nonaccrual'}
                                                    ],
                                            value='ncl')                                
                                        ]
                            ),
                    html.Div(children=[
                                html.H6('Y-Axis:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':20}),
                                dcc.Dropdown(
                                            id='y',
                                            options=[
                                                    {'label':'Average Loan Balance (in ths)', 'value':'avg_os'},
                                                    {'label':'Loan Loss Reserve (in ths)', 'value':'alll'},
                                                    {'label':'Loan Loss Reserve (in %)', 'value':'alll_rate'},
                                                    {'label':'Net Credit Loss (in ths)', 'value':'ncl'},
                                                    {'label':'Net Credit Loss (in %)', 'value':'ncl_rate'},
                                                    {'label':'ALLL / NCL Ratio', 'value':'alll_to_ncl'},
                                                    {'label':'ALLL / Non-accrual Ratio', 'value':'alll_to_nonaccrual'}
                                                    ],
                                            value='alll_rate')                                
                                        ]
                            ),
                    
                    html.Div(children=[
                            html.Button(id='submit-btn', n_clicks=0, children='Submit',style={'background-color':'#FFE600'}),
                            ],style={'padding-top':20,'padding-bottom':20}),
                    
                    
                
                    html.Div(children=[
                                html.H5('Reporting Period:',
                                        style={'border-bottom':'4px solid #C4C4CD'})],
                                        style={'padding-top':15}),
                    
                    html.Div(children=[
                                html.H6('Select Reporting Period:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':20}),
                                dcc.Slider(
                                    id='rprt_date',
                                    min = 0,
                                    max = max_date-1,
                                    step = 1,
                                    value=0,
                                    updatemode='drag'),
                                dcc.Loading(id="loading-1", children=[html.Div(id="loading-output-1")], type="default")]),  
                    html.Div(children=[
                                html.H6(id='slider-output')])
                            ], style={'margin-left':'5%'}
                            ),
                                
    html.Div(
            className='nine columns',
            children=[
                    html.Div(children=[
                            html.H5('Peer Group Ratio Analysis:'),
                            dcc.Graph(id = 'summary_plot')
                            ]),                         
                    ], style={'display':'inline-block','width':900, 'padding-top':20}
                ),
    html.Div(id='data_prep',style={'display':'none'}),
    ]) 


"""
------------------------------------------------------------------------------------------------------------------------------------
Page2 layouts
"""
page_2 = html.Div([
    html.Div(
            className='four columns',
            children=[
                    html.Div(children=[
                            html.H5('Bank and Financial Ratio:',
                                    style={'border-bottom':'4px solid #C4C4CD', 'padding-top':20})]),
                    html.Div(children=[
                                html.H6('Bank:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':15}),
                                dcc.Dropdown(
                                            id='bank2',
                                            options=[
                                                    {'label':'JPMorgan Chase', 'value':852218},
                                                    {'label':'Bank of America', 'value':480228},
                                                    {'label':'Wells Fargo', 'value':451965},
                                                    {'label':'Citigroup', 'value':476810},
                                                    {'label':'Bank of Montreal', 'value':75633},
                                                    {'label':'Fifth Third', 'value':723112},
                                                    {'label':'US Bank', 'value':504713},
                                                    {'label':'PNC', 'value':817824},
                                                    {'label':'Capital One', 'value':112837},
                                                    {'label':'TD Bank', 'value':497404},
                                                    {'label':'Bank of New York Mellon', 'value':541101},
                                                    {'label':'State Street', 'value':35301},
                                                    {'label':'BB&T', 'value':852320},
                                                    {'label':'Sun Trust', 'value':675332},
                                                    {'label':'Goldman Sachs', 'value':2182786},
                                                    {'label':'Morgan Stanley', 'value':1456501},
                                                    {'label':'Key Bank', 'value':280110},
                                                    {'label':'MUFG', 'value':212465},
                                                    {'label':'Citizens', 'value':3303298},
                                                    {'label':'Regions', 'value':233031},
                                                    {'label':'American Express', 'value':1394676},
                                                    {'label':'Discover', 'value':30810},
                                                    {'label':'Huntington', 'value':12311},
                                                    {'label':'Comerica', 'value':60143}
                                            ],
                                            value=[852218, 480228, 451965, 476810], multi=True)
                                ],
                            ),
                
                     html.Div(children=[
                                html.H6('Financial Ratio:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':20}),
                                dcc.Dropdown(
                                            id='y2',
                                            options=[
                                                    {'label':'Average Loan Balance (in ths)', 'value':'avg_os'},
                                                    {'label':'Loan Loss Reserve (in ths)', 'value':'alll'},
                                                    {'label':'Loan Loss Reserve (in %)', 'value':'alll_rate'},
                                                    {'label':'Net Credit Loss (in ths)', 'value':'ncl'},
                                                    {'label':'Net Credit Loss (in %)', 'value':'ncl_rate'},
                                                    {'label':'ALLL / NCL Ratio', 'value':'alll_to_ncl'},
                                                    {'label':'ALLL / Non-accrual Ratio', 'value':'alll_to_nonaccrual'}
                                                    ],
                                            value='alll_rate')                                
                                        ]
                            ),
                   
                    html.Div(children=[
                                html.H5('Reporting Period:',
                                        style={'border-bottom':'4px solid #C4C4CD'})],
                                        style={'padding-top':15}),
                    
                    html.Div(children=[
                                html.H6('Select Reporting Period:',
                                        style={'width':200,'display':'inline-block','vertical-align':'top', 'padding-top':20}),
                                dcc.RangeSlider(
                                    id='rprt_date2',
                                    min = 0,
                                    max = max_date-1,
                                    step = 1,
                                    value=[0, 25],
                                    updatemode='drag',
                                    allowCross = False)]),  
                    html.Div(children=[
                                html.H6(id='slider-output2')]),
                           
    
    
                    html.Div(children=[
                            html.Button(id='submit-btn2', n_clicks=0, children='Submit',style={'background-color':'#FFE600'}),
                            ],style={'padding-top':15,'padding-bottom':15})
                    ], style={'margin-left':'5%'}),
    
                                
    html.Div(
            className='nine columns',
            children=[
                    html.Div(children=[
                            html.H5('Financial Ratio Time Series:'),
                            dcc.Graph(id = 'summary_plot2')
                            ]),                         
                    ], style={'display':'inline-block','width':900, 'padding-top':20}
            )
    ]) 




"""
------------------------------------------------------------------------------------------------------------------------------------
APP layouts and callback
"""
tabs_styles = {
              'height': '44px'
              }
tab_style = {
            'borderBottom': '1px solid #d6d6d6',
            'padding': '6px',
            'fontWeight': 'bold'
            }

tab_selected_style = {
                    'borderTop': '1px solid #d6d6d6',
                    'borderBottom': '1px solid #d6d6d6',
                    'backgroundColor': '#FFE600',
                    'color': 'grey',
                    'padding': '6px'
                    }

app.layout = html.Div([
    html.Div(
            className = 'ten columns',
            children=[
                    html.Div('Peer Bank Allowance Ratio Benchmarking Analysis',
                             style={'font-size':40,'color':'#FFE600','margin-left':'6%','font-weight':'bold'},
                             className = 'nine columns'),
                    html.Div(html.Img(src=app.get_asset_url('EY_Logo_Beam_RGB_White_Yellow.png'),
                                      style={'height':60}),
                             style={'height':70,'line-height':70,'text-align':'right'},
                             className = 'two columns')                                    
                    ], style={'display':'inline-block','height':70,'line-height':70,'margin-bottom':50,'margin-top':'1%'}
            ),
    html.Div(
            className = 'nine columns',
            children=[
                    dcc.Tabs(id="tabs-example", children=[
                        dcc.Tab(label='Peer Ratio Analysis', value='tab-1-example', style=tab_style, selected_style=tab_selected_style),
                        dcc.Tab(label='Financial Ratio Time Series', value='tab-2-example', style=tab_style, selected_style=tab_selected_style),
                     ] , value='tab-1-example',)
                    ], style={'margin-left':'5%'}),
    html.Div(id='tabs-content-example')
])


"""
------------------------------------------------------------------------------------------------------------------------------------
All callback
"""

## call back for tabs

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return page_1
    elif tab == 'tab-2-example':
        return page_2
    
@app.callback(Output("loading-output-1", "children"), [Input("rprt_date", "value")])
def input_triggers_spinner(value):
    time.sleep(.5)
    return value
    
## call back for tab # 1


@app.callback(Output('data_prep','children'), [Input('submit-btn','n_clicks')], [State('bank','value'), State('peers','value'), State('x','value'), State('y','value')])
def prep(n_clicks, bank, peers, x, y):
    
    nonpeer_list = [x for x in rssd_list if x not in [bank]+peers]
    type_cond = [data_source['RSSD'].isin([bank]), data_source['RSSD'].isin(peers), data_source['RSSD'].isin(nonpeer_list)]
    type_choise = ['Bank', 'Peers', 'Non-Peers']
    data_source['type'] = np.select(type_cond, type_choise, default = 'Non')
    
    #data_prep = data_source[['Report_Date', 'RSSD', 'bank', 'type', 'avg_os', x, y]]
    
    return data_source.to_json()


@app.callback(Output('slider-output', 'children'),
    [Input('rprt_date', 'value')])
def update_output(value):
    return 'Report Date: {}'.format(date_map[value])



@app.callback(Output('summary_plot','figure'), [Input('data_prep', 'children'), Input('rprt_date','value')], [State('x','value'), State('y','value')])
def summary_plot(data_prep, rprt_date, x, y):
    
    plot_data = pds.read_json(data_prep)
    plot_data = plot_data[plot_data.Report_Date == date_map[rprt_date]]
    
    sum_plot = px.scatter(plot_data, x=x, y=y, size="avg_os", color="type", hover_name="bank", template='plotly_dark', 
                         labels = {'avg_os': 'Average Loan Balance (in ths)',
                                   'alll': 'Loan Loss Reserve (in ths)',
                                   'alll_rate': 'Loan Loss Reserve (in %)',
                                   'ncl':'Net Credit Loss (in ths)',
                                   'ncl_rate':'Net Credit Loss (in %)',
                                   'alll_to_ncl':'ALLL / NCL Ratio',
                                   'alll_to_nonaccrual':'ALLL / Non-accrual Ratio'})

    sum_plot['layout'].update({
    'plot_bgcolor':'rgba(0,0,0,0)',
    'paper_bgcolor':'rgba(0,0,0,0)',
    },
    xaxis=dict(
        showgrid=True,
        gridcolor='#747480',
        gridwidth=0.5,
        zerolinecolor='#747480',
        zerolinewidth=1,
        linecolor='#FFE600',
        linewidth=2
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#747480',
        gridwidth=0.5,
        zerolinecolor='#747480',
        zerolinewidth=1,
        linecolor='#FFE600',
        linewidth=2
    ))
    
    return sum_plot


## call back for tab # 2
@app.callback(Output('slider-output2', 'children'),
    [Input('rprt_date2', 'value')])
def update_output2(value):
    return 'Report Date from: {}'.format(date_map[value[0]]) + ' to {}'.format(date_map[value[1]])


@app.callback(Output('summary_plot2','figure'), [Input('submit-btn2','n_clicks')], [State('bank2','value'), State('y2','value'), State('rprt_date2','value')])
def summary_plot2(n_clicks, bank2, y2, rprt_date2):
    
    plot_data = data_source[(data_source['RSSD'].isin(bank2))&(data_source['date_index']>=rprt_date2[0])&(data_source['date_index']<=rprt_date2[1])]
    
    sum_plot = px.line(plot_data, x="Report_Date", y=y2, color="bank", hover_name="bank", line_shape="spline",
                        labels = {'avg_os': 'Average Loan Balance (in ths)',
                                   'alll': 'Loan Loss Reserve (in ths)',
                                   'alll_rate': 'Loan Loss Reserve (in %)',
                                   'ncl':'Net Credit Loss (in ths)',
                                   'ncl_rate':'Net Credit Loss (in %)',
                                   'alll_to_ncl':'ALLL / NCL Ratio',
                                   'alll_to_nonaccrual':'ALLL / Non-accrual Ratio'}, template='plotly_dark',)
    
    sum_plot['layout'].update({
    'plot_bgcolor':'rgba(0,0,0,0)',
    'paper_bgcolor':'rgba(0,0,0,0)',
    },
    xaxis=dict(
        showgrid=True,
        gridcolor='#747480',
        gridwidth=0.5,
        zerolinecolor='#747480',
        zerolinewidth=1,
        linecolor='#FFE600',
        linewidth=2
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#747480',
        gridwidth=0.5,
        zerolinecolor='#747480',
        zerolinewidth=1,
        linecolor='#FFE600',
        linewidth=2
    ))
    
    return sum_plot

## run function

if __name__ == '__main__':
    app.run_server()
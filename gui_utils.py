# - coding: utf-8 --
'''
@info utilities to draw the ilu gui
@author Rui Henriques
@version 1.0
'''

import pandas as pd
import dash_core_components as dcc 
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.dependencies import State
from enum import Enum


''' ============================== '''
''' ====== A: CREATE BUTTON ====== '''
''' ============================== '''

Button = Enum('Button', 'radio timerange input input_hidden checkbox multidrop daterange date time upload unidrop graph figure html link hours pie text')

def button(button_id, title, values, radio, sel_options=None):
    '''
    @function draws button
    @inputs id, label, values, radio (boolean), options
    @returns Dash button
    '''
    button = None
    style={'width':'100%','font-size':'12px'}
    
    # A: Input, DateRange buttons
    if radio is Button.input: 
        button = dcc.Input(id=button_id,value='0' if values is None else values,style={'width':'10%','font-size':'12px'})
    elif radio is Button.input_hidden:
        button = dcc.Input(id=button_id,value='0' if values is None else values,style={'width': '100%', 'display': 'none'})
    elif radio is Button.daterange: 
        button = dcc.DatePickerRange(id=button_id,start_date=pd.to_datetime(values[0]),end_date=pd.to_datetime(values[1]),style=style)
    elif radio is Button.date: 
        button = dcc.DatePickerSingle(id=button_id,date=pd.to_datetime(values),style=style)
    elif radio is Button.time: 
        #button = dcc.Slider(id=button_id,min=0,max=24,step=0.5,value=int(values))
        marks = {}
        for i in range(0,25,2): #[0,4,8,12,16,20,24]:
            marks[i]={'label': str(i)+'h'}
        button = dcc.Slider(id=button_id,step=0.5,min=0,max=24,value=int(values),marks=marks)
    elif radio is Button.hours:
        button= dcc.RangeSlider(id=button_id,min=0,max=24,step=0.5,value=[5, 15],marks={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'11',12:'12',13:'13',14:'14',15:'15',16:'16',17:'17',18:'18',19:'19',20:'20',21:'21',22:'22',23:'23',24:'24'})
    elif radio is Button.timerange:
        if False:
            marks = {}
            for i in [0,4,8,12,16,20,24]:
                marks[i]={'label': str(i)+'h'}
            button = dcc.RangeSlider(id=button_id,step=1,min=0,max=24,value=[0,24],marks=marks)
        else:
            explicit = False
            if len(values)==3: explicit = values[2]
            checkButton = dcc.Checklist(id=button_id+"_pick",options=[{'value':'pick','label':' Pick time range'}],value=[],
                                        labelStyle={'display':'none' if explicit else 'inline-block','margin':'5px'},style=style)
            labelStyle = {'display':'inline','font-size':'11px','color':'#404040','margin-left':'4px','margin-right':'7px'}
            inputStyle = {'display':'inline','font-size':'12px','color':'#404040','margin-left':'3px','height':'30px','width':'100px'}
            itime = dcc.Input(id=button_id+"_start",type='time',value=values[0],min="00:00",max="23:59",style=inputStyle, className="form-control")
            ftime = dcc.Input(id=button_id+"_end",type='time',value=values[1],min="00:00",max="23:59",style=inputStyle, className="form-control")
            #dropStyle = {'display':'block','font-size':'11px','color':'#404040','height':'30px','width':'62px','vertical-align':'center'}
            #dropButton = dcc.Dropdown(id=button_id+"_days", options=[{'value':'nextday','label':'+1 day'},{'value':'sameday','label':'+0 days'}],value="nextday", multi=False, style=dropStyle)
            
            timeButton = html.Div([itime, html.Label("+0 days",style=labelStyle), 
                                    ftime, html.Label("+0 days" if values[1]>values[0] else "+1 day",id=button_id+"_days",style=labelStyle)],
                                   id=button_id,style={'display':'inline-block' if explicit else 'none'})
            #dbc.Col([dropButton],width="auto")],no_gutters=True)
            button = html.Div([checkButton,timeButton])
    elif radio is Button.upload:
        button = html.Div([
            dcc.Upload(id=button_id,children=html.Div(['Drag and Drop or ',html.A('Select Files')]),
                style={'width':'100%','height':'60px','lineHeight':'60px','borderWidth':'1px','borderStyle':'dashed','borderRadius':'5px','textAlign':'center'},
                multiple=False),
            html.Div(id=button_id + '_output', style={'textOverflow': 'ellipsis', 'overflow': 'hidden'}),
        ],style=style)

    # B: HTML buttons
    elif radio is Button.html:
        button = html.Div(id=button_id,children=values,style={'width':'80%','font-size':'14px'})
        #if sel_options is None: 
        return button
    elif radio is Button.text:
        style['height'] = '220px' #if sel_options==None else str(sel_options)+'px'
        #textStyle = {'width':'58%','height':height,'font-family':'monospace','font-size':'15px'}
        #style['font-family']='monospace'
        style['font-size']='14px'
        button = html.Div(style={'overflow':'auto','display':'flex', 'whiteSpace': 'pre-line'},#,'flex-direction':'column-reverse'},
                          children=[dcc.Textarea(id=button_id,value=values,placeholder=values,style=style)])
    elif radio is Button.graph or radio is Button.figure: 
        button = dcc.Graph(id=button_id, figure=get_null_plot(),style=style)

    # C: Radio, CheckBox, Drop buttons
    else: 
        options = []
        for v in values: 
            if type(v) is str: options.append({'value':v, 'label':' '+v.replace('_',' ').capitalize()})
            else: options.append({'value':str(v), 'label':' '+str(v)})
        if radio is Button.radio: 
            sel_option = options[0]['value'] if sel_options is None else sel_options
            button = dcc.RadioItems(id=button_id,options=options,value=sel_option,
                                    labelStyle={'display':'inline-block','margin':5},style=style)
        elif radio is Button.checkbox: 
            if sel_options is None: sel_options = []
            button = dcc.Checklist(id=button_id,options=options,value=sel_options,
                                   labelStyle={'display':'inline-block','margin':5},style=style)
            if len(values)==1: return html.Div(button)
        else:
            multi = True if radio is Button.multidrop else False
            sel_options = [options[0]['value']] if sel_options is None else sel_options
            #if not multi: sel_options = sel_options[0] #TODO
            button = dcc.Dropdown(id=button_id,options=options,value=sel_options,multi=multi,style=style)
            
    # D: return framed button
    titlehtml = []
    if radio is not Button.input_hidden:
        title = title.replace('_',' ').capitalize()+':'
        titlehtml.append(html.Label(title,style={'margin-top':10,'font-size':'12px','font-weight':'bold'}))
    return html.Div(titlehtml+[button])


''' ============================ '''
''' ====== C: PAGE LAYOUT ====== '''
''' ============================ '''

def get_block_parameters(block_id, title, parameters, prefix="", hidden=False, empty=False): #'width':('%f%%' % width),
    boxstyle = {'background-color':'#dce7f3','border-radius':'5px','margin':0,'margin-bottom':'20px',
                'border':'none','vertical-align':'top','padding':'10px','width':'100%','height':'100%','display':'inline-block'}
    if hidden: boxstyle['display']='none'
    if title is None: block=[]
    else: block = [html.Label(title.replace('_',' ').capitalize(),style={'color':'#536878','font-weight':'bold','font-size':'13px'})]
    for param in parameters: 
        sel_options = None if len(param)<=3 else param[3]
        if hidden: button_type = Button.input_hidden
        else: button_type = param[2]
        block.append(button(prefix+param[0],param[0],param[1],param[2],sel_options))
    body = html.Div(block, id=block_id) if empty else html.Div(block,id=block_id,style=boxstyle) 
    return body #html.Div([body,html.Br()])


def get_layout(pagetitle, parameters, visuals, prefix=""):
    
    # A: create header
    titlestyle = {'color':'#cc6666','margin-right':6,'margin-bottom':12,'margin-left':12,'margin-top':10,
                  'vertical-align':'bottom','font-weight':'bold','font-size':'15px','display':'inline-block'}
    homestyle = {'background-color':'#f3e7dc','margin-bottom':12,'height':'30px',
                 'line-height':'10px','border':'none','color':'gray','font-size':'11px','display':'inline-block'}
    layout = [html.Button('HOME',id='return_home',style=homestyle),html.H6(pagetitle, style=titlestyle),html.Br()]
    
    # B: create body
    pageparameters = []
    for blockparam in parameters: 
        #print(blockparam[0])
        if type(blockparam[1])==list:
            pageparameters.append(dbc.Col(get_block_parameters(prefix + blockparam[0], blockparam[0], blockparam[1], prefix)))
        else: 
            hidden_components = [get_block_parameters(prefix + blockparam[0], blockparam[0], [], prefix, True, False)]
            for key in blockparam[1]:
                component = get_block_parameters(prefix+key, key+" :: "+blockparam[0], blockparam[1][key], prefix+key, True, False)
                hidden_components.append(component)
            pageparameters.append(dbc.Col(html.Div(hidden_components)))
    #print(pageparameters)
    
    layout.append(dbc.Row(pageparameters,no_gutters=False))
    submitstyle = {'background-color':'#6ABB97','border':'none','font-size':'14px','width':'100%','margin-top':20}
    layout.append(dbc.Row([dbc.Col(html.Button('Run query', id=prefix+'button',style=submitstyle))]))
        
    # C: create visuals    
    visuals_list = []
    for param in visuals:
        mbutton =  button(prefix+param[0],param[0],param[1],param[2],None if len(param)<=3 else param[3])
        visuals_list.append(dbc.Row(dbc.Col(mbutton)))
    layout.append(html.Div(visuals_list, id=prefix + 'charts'))

    return html.Div(layout,style={'width':'70%','margin':20})


def get_vertical_layout(parameters):
    pageparameters = []
    for blockparam in parameters: 
        pageparameters.append(dbc.Row(get_block_parameters(blockparam[0], blockparam[0], blockparam[1], "")))
    return html.Div(pageparameters)

def get_hidden_components(hidden_parameters, qprefix):
    hidden_components = []
    for key in hidden_parameters:
        block = get_block_parameters(qprefix+key,key.capitalize()+" parameters",hidden_parameters[key],qprefix+key,True)
        hidden_components.append(dbc.Col(block))
    return dbc.Row(hidden_components)

def get_states(parameters):
    states = []
    for iparameters in parameters:
        for param in iparameters[1]:
            states.append(State(param[0],'value'))
    return states

''' ================================ '''
''' ====== D: OTHER APP UTILS ====== '''
''' ================================ '''

def get_null_plot(message=None):
    title='parameterize and click <b>run</b> to visualize'
    if message is not None: title=message
    nulllayout = go.Layout(height=200, title=title, font=dict(size=9)) #color='#7f7f7f'
    return go.Figure(layout=nulllayout) 

def get_graph(fig, title=None):
    title = [] if title is None else [html.Div([html.H3(title, style={'marginBottom': 0})], style={'textAlign': "center"})]
    return html.Div(title+[dcc.Graph(figure=fig)])

def format_labels(label_format, lst):
    return [{'label': label_format.format(str(el).capitalize()), 'value': el} for el in lst]

def get_null_label():
    return html.Label('None',style={'color':'gray'})

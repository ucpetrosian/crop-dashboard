from flask import Flask
import pandas as pd
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input, dash_table, State
import plotly.express as px
from statistics import mean

launch = "python_anywhere" ## Should be github if you are running this locally
user = "cpetrosi" ## 

if launch == "python_anywhere":
    static_path = "/home/audreypet/crop-dashboard"
elif launch == "github":
    static_path = f"C:/Users/{user}/Documents/GitHub/crop-dashboard"

trex_all = pd.read_csv(f"{static_path}/sample-data/trex_data.csv")
time_format = "%Y-%m-%d %H:%M:%S"
trex_all["TIMESTAMP"] = [datetime.strptime(time, time_format) for time in trex_all["TIMESTAMP"]]

lynn_all = pd.read_csv(f"{static_path}/sample-data/lynn_data.csv")
lynn_all["TIMESTAMP"] = [datetime.strptime(time, time_format) for time in lynn_all["TIMESTAMP"]]

matt_all = pd.read_csv(f"{static_path}/sample-data/matt_data.csv")
matt_all["TIMESTAMP"] = [datetime.strptime(time, time_format) for time in matt_all["TIMESTAMP"]]
trex_all.LW_IN = trex_all.LW_IN.astype(float)
trex_drop = trex_all[trex_all.LW_IN < -10000000].index
trex_all.drop(trex_drop, inplace = True)
st = ["TS1_2cm", "TS1_6cm", "TS2_2cm", "TS2_6cm", "TS3_2cm", "TS3_6cm", "TS4_2cm", "TS4_6cm", "TS5_2cm", "TS5_6cm",]

trex_all = pd.concat([trex_all, lynn_all])

for param in st:
    trex_drop = trex_all[trex_all[param] < -10000000].index
    trex_all.drop(trex_drop, inplace = True)

range_path = f"{static_path}/read-in-csvs/all_dl_ranges.csv"
rangedf = pd.read_csv(range_path, header=[0],sep=',',na_values="NAN",engine='python')

test_calls = ['e_probe', 'e_sat_probe', 'H2O_probe', 'RH_3_1_1', 'T_DP_3_1_1', 'FW', 'H_FW', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_3_1_1', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P_Tot', 'batt_volt']

reports = ['G', 'G_1_1_1', 'G_2_1_1', 'G_3_1_1', 'G_4_1_1', 'G_5_1_1', 'SG_1_1_1', 'SG_2_1_1', 'SG_3_1_1', 'SG_4_1_1', 'SG_5_1_1', 'G_plate_1_1_1', 'G_plate_2_1_1', 'G_plate_3_1_1', 'G_plate_4_1_1', 'G_plate_5_1_1', 'TS1_2cm', 'TS1_6cm', 'TS2_2cm', 'TS2_6cm', 'TS3_2cm', 'TS3_6cm','TS4_2cm', 'TS4_6cm', 'TS5_2cm', 'TS5_6cm', 'SWC_1_1_1', 'SWC_2_1_1', 'SWC_3_1_1', 'SWC_4_1_1', 'SWC_5_1_1', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_1_1_3', 'T_CANOPY', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P', 'V_batt']


almonds = ["VAC", "OLA", "WWF", "WES"]
olives = ["ART_011", "ORO_022", "ORO_043", "COR_CS3"]
pistachios = ["BLS_001", "BLS_002"]
grapes = ["FLT", "SLC", "SLM_001", "VOK_001", "RIP_722", "RIP_760"]
# Read in parameters classified by equipment group
almond_list = pd.read_csv(f"{static_path}/read-in-csvs/Almond_Equipment.csv")
grape_list = pd.read_csv(f"{static_path}/read-in-csvs/Grape_Equipment.csv")
olive_list = pd.read_csv(f"{static_path}/read-in-csvs/Olive_Equipment.csv")
pistachio_list = pd.read_csv(f"{static_path}/read-in-csvs/Pistachio_Equipment.csv")

# Read in coordinates for sites
coords = pd.read_csv(f"{static_path}/read-in-csvs/Site_Long_Lat.csv")
area = pd.read_csv(f"{static_path}/read-in-csvs/Site_Area_Coords.csv")


# Creates a dictionary that lists which parameters exist for each crop. Used to populate dropdowns based on crops later.

almond_dict = dict()
for j in almond_list.loc[0].unique():
    almond_dict[j] = []

for i in range(0, len(almond_list.loc[0])):
    almond_dict[almond_list.loc[0][i]].append(almond_list.columns[i])

almond_dict["All"] = sorted(list(almond_list.keys()), key = str.lower)
almond_dict["Reports"] = sorted(test_calls, key = str.lower)
    
grape_dict = dict()
for j in grape_list.loc[0].unique():
    grape_dict[j] = []

for i in range(0, len(grape_list.loc[0])):
    grape_dict[grape_list.loc[0][i]].append(grape_list.columns[i])

grape_dict["All"] = sorted(list(grape_list.keys()), key = str.lower)    
grape_dict["Reports"] = sorted(test_calls, key = str.lower)

olive_dict = dict()
for j in olive_list.loc[0].unique():
    olive_dict[j] = []

for i in range(0, len(olive_list.loc[0])):
    olive_dict[olive_list.loc[0][i]].append(olive_list.columns[i])
    
olive_dict["All"] = sorted(list(olive_list.keys()), key = str.lower)
olive_dict["Reports"] = sorted(reports, key = str.lower)
    
pistachio_dict = dict()
for j in pistachio_list.loc[0].unique():
    pistachio_dict[j] = []

for i in range(0, len(pistachio_list.loc[0])):
    pistachio_dict[pistachio_list.loc[0][i]].append(pistachio_list.columns[i])
    
pistachio_dict["All"] = sorted(list(pistachio_list.keys()), key = str.lower)
pistachio_dict["Reports"] = sorted(reports, key = str.lower)



last_week = relativedelta(weeks=+1)

# Assigns sites to crops.

site_dict = {
    "Almonds": almonds,
    "Grapes": grapes,
    "Olives": olives,
    "Pistachios": pistachios,
    "Table Grapes": ["BRO_001"],
    "Custom": ["OLA", "WWF", "VAC", "WES", "SLC", "FLT", "SLM_001", "VOK_001", "RIP_722", "RIP_760",
               "ORO_022", "ORO_043", "COR_CS3", "ART_011", "BLS_001", "BLS_002", "BRO_001"]
}
    


# Dashboard

calls = test_calls

today = date.today()
ini = today - timedelta(days=6)
ini2 = today - timedelta(days=30)

server = Flask(__name__)
dash_app = Dash(__name__, server = server, routes_pathname_prefix = "/dash/")


dash_app.layout = [html.Div([
    dcc.Location(id = "url"),
    html.Div(id = "window-check", style = {'display': "none"}),   ##### NEW
    html.Div([
        # Title and image at the top.
        
        html.Div([
            html.H1(["Crop Sensing Group Flux Dashboard"], 
                style = {"display": "inline-block", "margin-left": "35%", "vertical-align": "50%"},
                id = "title-text"),
            # html.Img(src=dash_app.get_asset_url('usda.png'), 
            #      style = {"width": 55, "display": "inline-block", "vertical-align": "10%", "margin-left": 10})
        ]),
        
        
        # Container for crop radio selection and label, packaged with Divs strategically for styling
        
        html.Div([
            html.Div([
                html.Div([
                    html.Label(["Crops:"], style = {"text-align": "left", "font-weight": "bold", 
                                                "padding-left": 75}, id = "crop-label")
                         ]),
                html.Div([
                    dcc.RadioItems(options = [
    #                 {"label": html.Div(["All"], style = {'display':'inline-block', "margin-right": 5, 
    #                                                       "padding-left": 2}), 
    #                  "value": "All"},
                    {"label": html.Div(["Almonds"], style = {'display':'inline-block', "margin-right": 5,
                                                             "padding-left": 2}), 
                     "value": "Almonds"},
                    {"label": html.Div(["Grapes"], style = {'display':'inline-block', "padding-left": 2,
                                                            "margin-right": 5}), 
                     "value": "Grapes"},
                    {"label": html.Div(["Olives"], style = {'display':'inline-block', "margin-right": 5,
                                                            "padding-left": 2}), 
                     "value": "Olives"},
                    {"label": html.Div(["Pistachios"], style = {'display':'inline-block', "margin-right": 5,
                                                                "padding-left": 2}),
                     "value": "Pistachios"},
                    {"label": html.Div(["Table Grapes"], style = {'display':'inline-block', "margin-right": 5,
                                                                "padding-left": 2}),
                     "value": "Table Grapes"},
                    {"label": html.Div(["Custom"], style = {'display':'inline-block', "margin-right": 5,
                                                                "padding-left": 2}),
                     "value": "Custom"}],
                value = "Almonds",
                id = "crop-radio",
                inline = True,
                style = {"margin-bottom": 10, "padding-left": 71, "margin-top": 10, "margin-bottom": 20,
                         "display": "inline-block"})
            ]),
        ]),
            
            
            # A couple Divs that contain the site selection drop down and its labels,
            # Second Site hidden on app load.
            
            html.Div([
                html.Label(["Sites:"], id = "site-label-1", 
                           style = {"text-align": "left", "font-weight": "bold", 
                                    "padding-left": 75})
            ]),
              
            html.Div([
                dcc.Dropdown(
                    id = 'site-selection',
                    multi = True,
                    searchable = False,
                    clearable = True,
                    maxHeight = 420,
                    style = {"margin-bottom": 10, "margin-top": 10, "margin-right": "15%"})
            ], style = {"width": "35%", "display": "inline-block", "padding-left": 75},
            id = "site-select-div"),
            html.Div([
                html.Label(["Site 2 (For Parameter 2):"], id = "site-label-2",
                          style = {})
            ]),
            html.Div([
                dcc.Dropdown(
                    id = "second-site",
                    multi = False,
                    clearable = True,
                    searchable = False,
                    maxHeight = 420,
                    style = {})
            ], id = "second-site-div", style = {"width": "29.75%", "display": "inline-block", "padding-left": 75,
                                                "margin-top": 10}),





            # Div for equipment group selection dropdown
                
            html.Div([

                html.Div([
                    html.Label(["Equipment Group:"], style = {"text-align": "left", "font-weight": "bold",
                                                              "margin-top": 10},)
            ], id = "equip-label", style = {"margin-top": 5}),
                dcc.Dropdown(
#                     options = ["Asperated Shield"],
#                     value = ["Asperated Shield"],
                    id = 'equip-group',
                    style = {"margin-bottom": 15, "margin-top": 10, "margin-right": "15%"},
                    clearable = False,
                    searchable = False,
                    maxHeight = 300)
                ], 
                style = {"width": "90%", "display": "inline-block",
                        "padding-left": 75},
                id = "equip-group-div"),
            
            # Dropdown for first parameter selection and label.
            
            html.Div([            
                html.Label(["Parameter:"],
                         id = "param-text-1",
                         style = {}),
                html.Label(["Plot Type:"], id = "plot-type-label", 
                           style = {"text-align": "center", "font-weight": "bold", 
                                    "margin-left": "12.8%", 'display': "inline-block"}),
            ]),

            html.Div([
                html.Div([
                    dcc.Dropdown(
        #                     options = ["e_probe"],
                            # value = ["batt_volt"],
                            id = "param-select",
                            style = {"margin-top": 10, "margin-right": "15%"},
                            clearable = False,
                            searchable = False,
                            maxHeight = 420)
                ], style = {"display": "inline-block", "width": "35%",
                            "padding-left": 75},
                    id = "param-select-div"),

                # Dropdown that customizes plot displayed based on used dropdown
                
                html.Div([
                    dcc.Dropdown(
                            options = [
                                {'label': "Line Plot: Parameter vs. Time", 'value': "LP-PT"},
                                {'label': "Line Plot: Two Parameters vs. Time", "value": "LP-2PT"},
                                {'label': "Scatter Plot: Parameter vs. Time", "value": "SP-PT"},
                                {'label': "Scatter Plot: Two Parameters vs. Time", "value": "SP-2PT"},
                                {'label': "Scatter Plot: Parameter vs. Parameter", 'value': "SP-PP"}],
                            value = "LP-PT",
                            multi = False,
                            clearable = False,
                            searchable = False,
                            id = 'plot-type-dropdown')
                ], style = {},
                   id = "right-dropdown-div")
                
            ]),
            
            # Second parameter dropdown, hidden upon initialization
            
            html.Div([
                html.Label(["Parameter 2:"], id = "param-text-2",
                style = {"text-align": "left", "font-weight": "bold", 
                "padding-left": 75,
                "padding-right": "24.5%"})
                ], style = {"margin-top": 10}),
            html.Div([
                dcc.Dropdown(
                    id = "second-param",
                    style = {},
                    clearable = False,
                    searchable = False,
                    maxHeight = 420)
            ], style = {"width": "35%", "display": "inline-block", "padding-left": 75},
                id = "second-param-div")

            
            
        ], style = {"display": "grid"}),
    
            
        ]),
        
        # Generates two graph objects: one for the map, one for the graph.
        
        html.Div([dcc.Graph(id = "map-graph",
                 style = {"width": "35%", "display": "inline-block", "padding-left": 75}),
#                  html.Div([""], style = {"display": "inline-block"}),
                 dcc.Graph(id = "norm-graph",
                 style = {"width": "57%", "display": "inline-flex", "margin-left": 35})]),
        html.Div([
                    html.Label(["Plot Type:"], id = "plot-type-label-mobile", 
                           style = {"text-align": "center", "font-weight": "bold", 
                                    "margin-left": "12.8%", 'display': "inline-block"}),
                    dcc.Dropdown(
                            options = [
                                {'label': "Line Plot: Parameter vs. Time", 'value': "LP-PT"},
                                {'label': "Line Plot: Two Parameters vs. Time", "value": "LP-2PT"},
                                {'label': "Scatter Plot: Parameter vs. Time", "value": "SP-PT"},
                                {'label': "Scatter Plot: Two Parameters vs. Time", "value": "SP-2PT"},
                                {'label': "Scatter Plot: Parameter vs. Parameter", 'value': "SP-PP"}],
                            value = "LP-PT",
                            multi = False,
                            clearable = False,
                            searchable = False,
                            id = 'plot-type-dropdown-mobile')
                ], style = {},
                   id = "right-dropdown-div-mobile"),
    
        # Creates storage for each non-site drop down to improve user experience.
    
        dcc.Store(id = "drop1-store",
                  data = {'drop1': 'option1'}),
        dcc.Store(id = "drop2-store",
                  data = {"drop2": "option2"}),
        dcc.Store(id = "drop3-store",
                  data = {"drop3": "option3"})],
        style = {"font-family": "Helvetica, sans-serif"})
             ]



# Fills equipment group dropdown based on radio selection. Alphabetizes equipment group names for continuity.
@server.route("/")

@callback(
    Output("equip-group", "options"),
    Input("crop-radio", "value"))

def populate_dropdown(radio):
    if radio == "Almonds":
        return [{'label': i, 'value': i} for i in sorted(almond_dict.keys())]
    elif radio == "Grapes":
        return [{'label': i, 'value': i} for i in sorted(grape_dict.keys())]
    elif radio == "Olives":
        return [{'label': i, 'value': i} for i in sorted(olive_dict.keys())]
    elif radio == "Pistachios":
        return [{'label': i, 'value': i} for i in sorted(pistachio_dict.keys())]
    elif radio == "Table Grapes":
        return [{'label': i, 'value': i} for i in sorted(olive_dict.keys())]
    else:
        return [{'label': i, 'value': i} for i in sorted(olive_dict.keys())]


# Populates second dropdown based on equipment selected in first dropdown.

@callback(
    Output("param-select", "options"),
    Input("equip-group", "value"),
    Input("crop-radio", "value"))

def talking_dropdown(selected_param, radio):
    if radio == "Almonds":
        return [{'label': i, 'value': i} for i in almond_dict[selected_param]]
    elif radio == "Grapes":
        return [{'label': i, 'value': i} for i in grape_dict[selected_param]]
    elif radio == "Olives":
        return [{'label': i, 'value': i} for i in olive_dict[selected_param]]
    elif radio == "Pistachios":
        return [{'label': i, 'value': i} for i in pistachio_dict[selected_param]]
    elif radio == "Table Grapes":
        return [{'label': i, 'value': i} for i in olive_dict[selected_param]] 
    else:
        return [{'label': i, 'value': i} for i in olive_dict[selected_param]]
    
    
# Repeat same code as above but for second parameter dropdown.
    
@callback(
    Output("second-param", "options"),
    Input("equip-group", "value"),
    Input("crop-radio", "value"))

def second_talking_dropdown(selected_param, radio):
    if radio == "Almonds":
        return [{'label': i, 'value': i} for i in almond_dict[selected_param]]
    elif radio == "Grapes":
        return [{'label': i, 'value': i} for i in grape_dict[selected_param]]
    elif radio == "Olives":
        return [{'label': i, 'value': i} for i in olive_dict[selected_param]]
    elif radio == "Pistachios":
        return [{'label': i, 'value': i} for i in pistachio_dict[selected_param]]
    elif radio == "Table Grapes":
        return [{'label': i, 'value': i} for i in olive_dict[selected_param]] 
    else:
        return [{'label': i, 'value': i} for i in olive_dict[selected_param]]

# Sets site options based on crop selection, exception granted for "custom" option.
    
@callback(
    Output("site-selection", "options"),
    Input("crop-radio", "value"))
def site_dropdown(radio):
        if radio != "Custom":
            return [{'label': i, 'value': i} for i in site_dict[radio]]
        else:
            return [{'label': i, 'value': i} for i in site_dict["Custom"]]

# Stores current equipment value selected
    
@callback(
    Output('drop1-store', 'data'),
    Input('crop-radio', 'value'),
    State('equip-group', 'value'), 
)

def update_store1(radio_value, drop1_value):
    return {'drop1': drop1_value}

# Stores current parameter selected

@callback(
    Output('drop2-store', 'data'),
    Input('crop-radio', 'value'),
    State('param-select', 'value'), 
)

def update_store2(radio_value, drop2_value):
    return {'drop2': drop2_value}

# Stores the second parameter.

@callback(
    Output("drop3-store", "data"),
    Input("crop-radio", "value"),
    State("second-param", "value"))

def update_store3(radio_value, drop3_value):
    return {'drop3': drop3_value}


# Maintains equipment when changing radio items
# Initializes equipment group and prevents invalid equipment group for being selected for certain crops

@callback(
    Output('equip-group', 'value'),
    Input('drop1-store', 'data'),
    Input("equip-group", "options"),
    Input('crop-radio', 'value')
)
def update_dropdowns1(store_data, options, crop):
    if crop != "Almonds" and (store_data['drop1'] == "IRT Sensor" or store_data['drop1'] == "Fine Wire Thermocouple"):
        return "Asperated Shield"
    elif store_data['drop1'] == None:
        return options[0]['value']
    else:
        return store_data['drop1']

# Maintains parameter when changing radio items
# If no equipment has been selected, default will populate menu     
    
@callback(
    Output('param-select', 'value'),
    Input('drop2-store', 'data'),
    Input('param-select', 'options'),
    Input('crop-radio', 'value'),
    Input('equip-group', 'value')
)
def update_dropdowns2(store_data, options, site, equipment):
    if store_data["drop2"] == None:
        return options[0]['value']
    elif site == "Almonds":
        if store_data['drop2'] in almond_dict[equipment]:
            return store_data['drop2']
        else:
            return options[0]['value']
    elif site == "Olives":
        
        # Checks to see if current selected parameter exists for site, 
        # if not displays first parameter under equipment
        
        if store_data['drop2'] in olive_dict[equipment]:
            return store_data['drop2']
        else:
            return options[0]['value']
    elif site == "Pistachios":
        if store_data['drop2'] in pistachio_dict[equipment]:
            return store_data['drop2']
        else:
            return options[0]['value']
    elif site == "Grapes":
        if store_data['drop2'] in grape_dict[equipment]:
            return store_data['drop2']
        else:
            return options[0]['value']
    elif site == "Table Grapes":
        if store_data["drop2"] in olive_dict[equipment]:
            return store_data['drop2']
        else:
            return options[0]['value']
    else:
        if store_data["drop2"] in olive_dict[equipment]:
            return store_data['drop2']
        else:
            return options[0]['value']
        

# Almost identical code as above, used for secondary parameter dropdown.
        
@callback(
    Output("second-param", 'value'),
    Input('drop3-store', 'data'),
    Input('second-param', 'options'),
    Input('crop-radio', 'value'),
    Input('equip-group', 'value')
)

def update_second_parameter(store_data, options, site, equipment):
    if store_data["drop3"] == None:
        return options[1]['value']
    elif site == "Olives":
        
        # Checks to see if current selected parameter exists for site, 
        # if not displays first parameter under equipment
        
        if store_data['drop3'] in olive_dict[equipment]:
            return store_data['drop3']
        else:
            return options[1]['value']
    elif site == "Almonds":
        if store_data['drop3'] in almond_dict[equipment]:
            return store_data['drop3']
        else:
            return options[1]['value']
    elif site == "Pistachios":
        if store_data['drop3'] in pistachio_dict[equipment]:
            return store_data['drop3']
        else:
            return options[1]['value']
    elif site == "Grapes":
        if store_data['drop3'] in grape_dict[equipment]:
            return store_data['drop3']
        else:
            return options[1]['value']
    elif site == "Table Grapes":
        if store_data["drop3"] in olive_dict[equipment]:
            return store_data['drop3']
        else:
            return options[1]['value']
    else:
        if store_data["drop3"] in olive_dict[equipment]:
            return store_data['drop3']
        else:
            return options[1]['value']
        
# Populate dropdown depending on crop selection and number of parameters viewing

@callback(
    Output("site-selection", "value"),
    Input("site-selection", "options"),
    Input("crop-radio", "value"),
    Input("plot-type-dropdown", "value"))

def site_populate(options, radio, num_param):
    if num_param in ['LP-PT', 'SP-PT']:
        if radio == "Custom":
            return site_dict["Custom"]
        else:
            return [options[i]["value"] for i in range(0,len(site_dict[radio]))]
    else:
        return options[0]["value"]

# Switch on/off second dropdown based on # of parameters
    
@callback(
    Output("second-param", "style"),
    Input("plot-type-dropdown", "value"))

def add_second_dropdown(num_param):
    if num_param in ['LP-PT', 'SP-PT']:
        return {"display": "none"}
    else:
        return {"margin-top": 5, "margin-right": "15%", "margin-bottom": 10}
    
# Disables/Enabled ability to selected multiple sites depending on plot type.

@callback(
    Output("site-selection", "multi"),
    Input("plot-type-dropdown", "value"))

def adjust_site_dropdown(num_param):
    if num_param in ['LP-PT', 'SP-PT']:
        return True
    else:
        return False
    
# Creates options for the second site, depending on what crop is selected.
    
@callback(
    Output("second-site", "options"),
    Input("crop-radio", "value"))

def second_site_options(radio):
    if radio != "Custom":
            return [{'label': i, 'value': i} for i in site_dict[radio]]
    else:
        return [{'label': i, 'value': i} for i in site_dict["Custom"]]
    
# Initializes a site for second site dropdown

@callback(
    Output("second-site", "value"),
    Input("second-site", "options"))

def second_site_drop_intialize(options):
    return options[0]["value"]

# Hides/shows second site style based on inputted plot type dropdown

@callback(
    Output("second-site", "style"),
    Output("second-site-div", "style"),
    Input("plot-type-dropdown", "value"),
    Input("window-check", "children"))

def show_second_site(num_param, width):
    if width > 1300:
        if num_param in ['LP-PT', 'SP-PT']:
            return [{"display": "none"},
                    {"width": "35%", "display": "inline-block", "padding-left": 75,
                                                "margin-top": 10}]
        else:
            return [{"margin-top": 5, "margin-right": "15%", "margin-bottom": 10},
                    {"width": "35%", "display": "inline-block", "padding-left": 75,
                                                "margin-top": 10}]
    else:
        if num_param in ['LP-PT', 'SP-PT']:
            return [{"display": "none"},
                    {"width": "90%", "display": "inline-block", "padding-left": 12,
                                                "margin-top": 10}]
        else:
            return [{"margin-top": 5, "margin-right": "15%", "margin-bottom": 10},
                    {"width": "90%", "display": "inline-block", "padding-left": 12}]
                    
# Adjusts placement of elemtents based on plot type dropdown input.
        
@callback(
    Output("equip-label", "style"),
    Output("plot-type-label", "style"),
    Output("param-text-1", "style"),
    Output("right-dropdown-div", "style"),
    Input("plot-type-dropdown", "value"),
    Input("window-check", "children"))

def change_equip_label(plot_type, width):
    if width > 1300:
        rdiv = (width-16) * .57
        block = ((width // 100) - 21) / 100
        graph_size = rdiv * (.765 + block)
        buffer = 35 + ((rdiv - graph_size)/2) - 75 + 10

        p1_buff = ((width-16) * .35) - 83.633

        if plot_type in ["LP-PT", "SP-PT"]:
            return [{},
                    {"text-align": "center", "font-weight": "bold", 
                                        "margin-left": buffer, 'display': "inline-block"},
                    {"text-align": "left", "font-weight": "bold", 
                            "padding-left": 75, 'display': "inline-block",
                            "padding-right": p1_buff},
                    {"display": "inline-block", "width": "35%", "padding-left": buffer}]
        else:
            return [{"margin-top": 10},
                    {"text-align": "center", "font-weight": "bold", "margin-left": buffer-10, 'display': "inline-block"},
                    {"text-align": "left", "font-weight": "bold", 
                            "padding-left": 75, 'display': "inline-block",
                            "padding-right": p1_buff},
                    {"display": "inline-block", "width": "35%", "padding-left": buffer}]
    else:
        rdiv = (width-16) * .57
        block = ((width // 100) - 21) / 100
        graph_size = rdiv * (.765 + block)
        buffer = 35 + ((rdiv - graph_size)/2) - 75 + 10

        p1_buff = ((width-16) * .35) - 83.633

        if plot_type in ["LP-PT", "SP-PT"]:
            return [{},
                    {"display": "none"},
                    {"text-align": "left", "font-weight": "bold", 
                            "padding-left": 12, 'display': "inline-block"},
                    {"display": "inline-block", "width": "35%", "padding-left": buffer}]
        else:
            return [{"margin-top": 10},
                    {"display": "none"},
                    {"text-align": "left", "font-weight": "bold", 
                            "padding-left": 12, 'display': "inline-block"},
                    {"display": "inline-block", "width": "35%", "padding-left": buffer}]

# Edits/hides/shows site dropdown based on plot type dropdown
    
@callback(
    Output("site-label-1", "children"),
    Output("site-label-2", "style"),
    Input("plot-type-dropdown", "value"),
    Input("window-check", "children"))

def site_text_update(plot_type, width):
    if width > 1300:
        if plot_type in ['LP-PT', 'SP-PT']:
            return ["Sites:", {"display": "none"}]
        else:
            return ["Site 1 (For Parameter 1):",
                {"text-align": "left", "font-weight": "bold", "padding-left": 75}]
    else:
        if plot_type in ['LP-PT', 'SP-PT']:
            return ["Sites:", {"display": "none"}]
        else:
            return ["Site 1 (For Parameter 1):",
                {"text-align": "left", "font-weight": "bold", "padding-left": 12}]

# Grabs screen size and stores it in empty Div
dash_app.clientside_callback(
    """
    function(href) {
        return window.innerWidth;
    }
    """,
    Output('window-check', 'children'),
    Input('url', 'href')
    )

# Hides/Shows/Edits labels of parameter dropdown labels based on plot type selection

@callback(
    Output("param-text-1", "children"),
    Output("param-text-2", "style"),
    Output("second-param-div", "style"),
    Input("plot-type-dropdown", "value"),
    Input("window-check", "children"))

def param_text_update(plot_type, width):
    if plot_type in ["LP-PT", "SP-PT"]:
        return ["Parameter:",
                {"display": "none"},
                {"width": "35%", "display": "inline-block", "padding-left": 75}]
    else:
        if width > 1300:
            return ["Parameter 1:", 
                {"text-align": "left", "font-weight": "bold", "padding-left": 75, "padding-right": "24.5%"},
                {"width": "35%", "display": "inline-block", "padding-left": 75}]
        else:
            return ["Parameter 1:", 
                {"text-align": "left", "font-weight": "bold", "padding-left": 12, "padding-right": "24.5%"},
                {"width": "90%", "display": "inline-block", "padding-left": 12}]
@callback(
    Output("title-text", "style"),
    Output("crop-label", "style"),
    Output("crop-radio", "style"),
    Output("site-label-1", "style"),
    Output("site-select-div", "style"),
    Output("equip-group-div", "style"),
    Output("param-select-div", "style"),
    Output("map-graph", "style"),
    Output("norm-graph", "style"),
    Input("window-check", "children")

)

def part_1_mobile_adjust(width):
    if width > 1300:
        return [
            {"display": "inline-block", "width": "100%", "vertical-align": "50%", "text-align": "center"},
            {"text-align": "left", "font-weight": "bold", "padding-left": 75},
            {"margin-bottom": 10, "padding-left": 71, "margin-top": 10, "margin-bottom": 20, 
             "display": "inline-block"},
            {"text-align": "left", "font-weight": "bold", "padding-left": 75},
            {"width": "35%", "display": "inline-block", "padding-left": 75},
            {"width": "35%", "display": "inline-block", "padding-left": 75},
            {"display": "inline-block", "width": "35%", "padding-left": 75},
            {"width": "35%", "display": "inline-block", "padding-left": 75},
            {"width": "57%", "display": "inline-flex", "margin-left": 35}
        ]
    else:
        return [
            {"display": "inline-block", "width": "100%", "vertical-align": "50%", "text-align": "center"},
            {"text-align": "left", "font-weight": "bold", "padding-left": 12},
            {"margin-bottom": 10, "padding-left": 7, "margin-top": 10, "margin-bottom": 20, 
             "display": "inline-block"},
            {"text-align": "left", "font-weight": "bold", "padding-left": 12},
            {"width": "90%", "display": "inline-block", "padding-left": 12},
            {"width": "90%", "display": "inline-block", "padding-left": 12},
            {"display": "inline-block", "width": "90%", "padding-left": 12, "margin-bottom": -10},
            {"width": "95%", "display": "inline-block", "padding-left": 12},
            {"width": "103%", "display": "inline-flex", "margin-left": -20}
        ]

@callback(
    Output("plot-type-dropdown", "value"),
    Output("plot-type-dropdown-mobile", "style"),
    Output("plot-type-label-mobile", "style"),
    Output("plot-type-dropdown", "style"),
    Input("plot-type-dropdown-mobile", "value"),
    Input("window-check", "children"),
    Input("plot-type-dropdown", "value")
)

def plot_type_dropdown_mobile(value, width, orig_val):
    if width > 1300:
        return [
            orig_val,
            {"display": "none"},
            {"display": "none"},
            {}
        ]
    else:
        return [
            value,
            {"width": "90%", "display": "inline-block", "padding-left": 12},
            {"text-align": "center", "font-weight": "bold", "margin-left": 12, 'display': "inline-block",
             "margin-top": 10, "margin-bottom": 5},
            {"display": "none"}
        ]


# Generates and customizes map.
# Displays sites on map depending on user input from radio items.

@callback(
    Output("map-graph", "figure"),
    Input("crop-radio", "value"),
    Input("site-selection", "value"))

def plot_map(sites, custom_sites):
    
    # Sets default zoom for plot depending on site, some crops have sites that are very close to/far from each other.
    
    if sites != "Custom":
        coords_temp = coords[coords["Crop"] == sites]
        area_temp = area[area["Crop"] == sites]
        if sites != "Almonds" and sites != "Grapes":
            h_set = 8
        else:
            h_set = 6.1
    else:
        try:
            coords_temp = coords[coords["Site"].isin(custom_sites)]
            h_set = 5.75

        except:
            coords_temp = coords[coords["Site"] == custom_sites]
            h_set = 8

        
    fig = px.scatter_mapbox(coords_temp, lat = "Lat", lon = "Lon", hover_name = "Site",
                            zoom = h_set, height = 450,
                            center = {"lat": mean(coords_temp.iloc[:,0]), "lon": mean(coords_temp.iloc[:,1])},
                            color = "Crop",
                            color_discrete_map={
                            "Almonds": "Blue",
                            "Olives": "Red",
                            "Pistachios": "Green",
                            "Grapes": "Purple",
                            "Table Grapes": "Yellow"}
                            )
    
#     # Creates boundaries for each ranch.
    
#     for ranch in range(0, len(area_temp)):
#         fig.add_trace(go.Scattermapbox(
#             mode = "lines",
#             hoverinfo = "none",
#             showlegend = False,
#             lon = area_temp.iloc[ranch,0:5],
#             lat = area_temp.iloc[ranch,5:10],
#             marker = {'size': 8},
#             line = go.scattermapbox.Line(color = area_temp.iloc[ranch,12], width = 2)
#         ))
        
#     # Makes site markers as top layer, fixes buggy hover feature.
#     fig.data = tuple(fig.data[::-1])
    # Chooses map background type
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_traces({'marker':{'size': 8}})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":75})
    # Puts legend in top left corner of map.
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
))
    return fig

# Generates a plot based on selected parameter and crop.

@callback(
    Output("norm-graph", "figure"),
    Input("crop-radio", "value"),
    Input("param-select", "value"),
    Input("plot-type-dropdown", "value"),
    Input("site-selection", "value"),
    Input("second-param", "value"),
    Input("second-site", "value"),
    Input("window-check", "children"))

def plot_graph(crops, yaxis_column_name, plot, first_drop, second_param, second_site, width):
    if plot in ['LP-PT', 'SP-PT']:
        site_drop = first_drop
    else:
        site_drop = [first_drop, second_site]
    # Generates a data frame for plot based on crop/site selected.
    if crops == "Almonds" or crops == "Grapes":
        sites = site_drop
        try:
            temp = trex_all.Site.isin(sites)
            data_temp = trex_all[temp]
        except:
            data_temp = trex_all[trex_all["Site"] == sites]
    elif crops == "Olives" or crops == "Pistachios" or crops == "Table Grapes":
        sites = site_drop
        try:
            temp = matt_all.Site.isin(sites)
            data_temp = matt_all[temp]
        except:
            data_temp = matt_all[matt_all["Site"] == sites]
    else:
        sites = site_drop
        combine_df = pd.concat([trex_all,matt_all])
        combine_df["V_batt"] = combine_df["V_batt"].combine_first(combine_df["batt_volt"])
        print(type(sites))
        try:
            temp = combine_df.Site.isin(sites)
            data_temp = combine_df[temp]
        except:
            data_temp = combine_df[combine_df["Site"] == sites]       
        
    # Dash will use generate one plot depending on user input, data is the same, plots have slight visual tweaks. 
    
    if plot == "LP-PT" or plot == "SP-PT":
        if plot == "LP-PT":
            fig = px.line(data_temp, x = data_temp.TIMESTAMP, y = data_temp[yaxis_column_name], custom_data = ["Site"],
                         color = data_temp.Site,
                        #  color_discrete_map={
                        # "BLS_001": "lime",
                        # "BLS_002": "blue",
                        # "ORO_022": "goldenrod",
                        # "ORO_043": "green",
                        # "COR_CS3": "magenta",
                        # "ART_011": "red",
                        # "OLA": "olive",
                        # "WWF": "steelblue",
                        # "VAC": "saddlebrown",
                        # "SLC": "orange",
                        # "FLT": "black",
                        # "WES": "darkmagenta",
                        # "BRO_001": "gold"},
                         height = 490)
            fig.update_traces(line={'width': 1.5})

        else:
            fig = px.scatter(data_temp, x = data_temp.TIMESTAMP, y = data_temp[yaxis_column_name], color = data_temp.Site,
                         custom_data = ["Site"],
                        #  color_discrete_map={
                        # "BLS_001": "lime",
                        # "BLS_002": "blue",
                        # "ORO_022": "goldenrod",
                        # "ORO_043": "green",
                        # "COR_CS3": "magenta",
                        # "ART_011": "red",
                        # "OLA": "olive",
                        # "WWF": "steelblue",
                        # "VAC": "saddlebrown",
                        # "SLC": "orange",
                        # "FLT": "black",
                        # "WES": "darkmagenta",
                        # "BRO_001": "gold"},
                         height = 490)
        # Assigns starting range for plot based on parameter.
        # Still allows user to pan up/down and left/right.

        ylow = int(rangedf[yaxis_column_name][0])
        yhi = int(rangedf[yaxis_column_name][1])
        fig.update_yaxes(range = [ylow, yhi], fixedrange = False)
        
        # Customized box on hover which shows date, time, y-value, and site.
    
        fig.update_traces(hovertemplate = '<b>%{customdata}</b><br>' +
                  'TIMESTAMP: %{x|%Y-%m-%d %H:%M}<br>'+yaxis_column_name+': %{y}<extra></extra>')
        if width > 1300:
            fig.update_layout(legend_title_text = "Sites (Click to Toggle)")
        else:
            fig.update_layout(legend_title_text = "Sites")
        fig.update_layout(
        xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1D",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="1W",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1M",
                     step="month",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True,
            thickness = .1
        ),
        type="date"
    )
)
    else:
        if plot != "SP-PP":
            # Create a new data frame to allow plotting command to use "group" option for organization, color ease.
            data = {
                "date": data_temp.TIMESTAMP,
                yaxis_column_name: data_temp[yaxis_column_name],
                second_param: data_temp[second_param],
                "Site": data_temp.Site
            }
            df = pd.DataFrame(data)
            # print(df)
            df_long = df.melt(id_vars=['date', "Site"], 
                              value_vars=[yaxis_column_name, second_param],
                              var_name='param_type',
                              value_name='param_vals')
            df_long_site_1 = df_long[df_long["Site"] == site_drop[0]]
            df_long_site_1 = df_long_site_1[df_long_site_1["param_type"] == yaxis_column_name]
            df_long_site_2 = df_long[df_long["Site"] == site_drop[1]]
            df_long_site_2 = df_long_site_2[df_long_site_2["param_type"] == second_param]

            if plot == "LP-2PT":
                fig = px.line(df_long_site_1, x = df_long_site_1.date, 
                             y = df_long_site_1.param_vals,
                             color = df_long_site_1.param_type,
                             custom_data = ["param_type"],
                             height = 490)
                fig.add_trace(
                    go.Scatter(
                        x = df_long_site_2.date,
                        y = df_long_site_2.param_vals,
                        mode = "lines",
                        name = second_param
                    ))
                fig.update_traces(line={'width': 1.5})
                
                range_options = [int(rangedf[yaxis_column_name][0]), int(rangedf[yaxis_column_name][1]),
                     int(rangedf[second_param][0]), int(rangedf[second_param][1])]
                ylow = min(range_options)
                yhi = max(range_options)
                fig.update_yaxes(range = [ylow, yhi], fixedrange = False)
                fig.update_traces(
                hovertemplate = '<b>TIMESTAMP</b>: %{x|%Y-%m-%d %H:%M}<br>' +
                              '<b>Y-Value</b>: %{y}<br>')

            else:
                fig = px.scatter(df_long_site_1, x = df_long_site_1.date, 
                             y = df_long_site_1.param_vals,
                             color = df_long_site_1.param_type,
                             custom_data = ["param_type"],
                             height = 490)
                fig.add_trace(
                    go.Scatter(
                        x = df_long_site_2.date,
                        y = df_long_site_2.param_vals,
                        name = second_param,
                        mode = "markers"
                    ))
                fig.update_traces(
                hovertemplate = '<b>TIMESTAMP</b>: %{x|%Y-%m-%d %H:%M}<br>' +
                              '<b>Y-Value</b>: %{y}<br>')
                range_options = [int(rangedf[yaxis_column_name][0]), int(rangedf[yaxis_column_name][1]),
                     int(rangedf[second_param][0]), int(rangedf[second_param][1])]
                ylow = min(range_options)
                yhi = max(range_options)
                fig.update_yaxes(range = [ylow, yhi], fixedrange = False)
            fig.update_layout(
            xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1D",
                         step="day",
                         stepmode="backward"),
                    dict(count=7,
                         label="1W",
                         step="day",
                         stepmode="backward"),
                    dict(count=1,
                         label="1M",
                         step="month",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True,
                thickness = .1,
            ),
            type="date"
            ))
        else:
            if site_drop[0] == site_drop[1]:
                pvp_df = data_temp[[yaxis_column_name, second_param]]
                fig = px.scatter(pvp_df, x = pvp_df.iloc[:,0],
                             y = pvp_df.iloc[:,1],
                            height = 490)
            else:
                site_1 = data_temp[data_temp["Site"] == site_drop[0]]
                site_1 = site_1[["TIMESTAMP", yaxis_column_name]]
                site_2 = data_temp[data_temp["Site"] == site_drop[1]]
                site_2 = site_2[["TIMESTAMP", second_param]]
                plot_ready = pd.merge(site_1, site_2, on='TIMESTAMP')
                fig = px.scatter(plot_ready, x = plot_ready.iloc[:,1],
                                 y = plot_ready.iloc[:,2],
                                height = 490)

            xlow = int(rangedf[yaxis_column_name][0])
            xhi = int(rangedf[yaxis_column_name][1])
            ylow = int(rangedf[second_param][0])
            yhi = int(rangedf[second_param][1])
            fig.update_yaxes(range = [ylow, yhi], fixedrange = False) 
            fig.update_xaxes(range = [xlow, xhi], fixedrange = False)
            fig.update_layout(plot_bgcolor= "#efefef")

                # Sets default plot setting as pan instead of zoom.
            fig.update_layout(dragmode='pan')
            fig.update_layout(xaxis_title = yaxis_column_name + " from " + site_drop[0],
                              yaxis_title = second_param + " from " + site_drop[1])
            fig.update_traces(
                hovertemplate = '<b>'+yaxis_column_name+' ('+site_drop[0]+')</b>: %{x}<br>' +
                              '<b>'+second_param+' ('+site_drop[1]+')</b>: %{y}<br>'
            )
            fig.update_layout(title = "Data for Sites: " + site_drop[0] + " and " + site_drop[1])
            return fig
        
        # Set a unique range based on the two normal ranges of selected parameters.
        

        
        # Customized box on hover which shows date, time and parameter.
        # Tweaked from command under "if" statement to emphasize parameter and not site.
    
#         fig.update_traces(hovertemplate = '<b>'+site_drop+'</b><br>'
#                           'TIMESTAMP: %{x|%Y-%m-%d %H:%M}<br>'+
#                           '%{customdata}'+': %{y}<extra></extra>')
        if width > 1300:
            fig.update_layout(legend_title_text = "Parameters (Click to Toggle)",
                            yaxis_title = site_drop[0] + ': ' + yaxis_column_name +
                            " / "+ site_drop[1] + ': ' + second_param,
                            xaxis_title = "TIMESTAMP",
                            title = "Data for Sites: " + site_drop[0] + " and " + site_drop[1])
        else:
            fig.update_layout(legend_title_text = "Parameters",
                            yaxis_title = site_drop[0] + ': ' + yaxis_column_name +
                            " / "+ site_drop[1] + ': ' + second_param,
                            xaxis_title = "TIMESTAMP",
                            title = "Data for Sites: " + site_drop[0] + " and " + site_drop[1])
        
    fig.update_traces({'marker':{'size':3.5}})

    
    # Changes date display on tick marks
    
    fig.update_xaxes(tickformat = "%m/%d\n%Y")
    
    # Sets default range from one week ago to today.
    
    fig.update_xaxes(range = [max(data_temp.TIMESTAMP) - last_week, max(data_temp.TIMESTAMP)])
    
    fig.update_layout(plot_bgcolor= "#efefef")
    
    # Sets default plot setting as pan instead of zoom.
    fig.update_layout(dragmode='pan')
    
    # Creates a slider to view different x-axis range easily. 
    # Can manually change range with slider or use buttons that show data from last day, week, month.
    # All options are negotiable just placeholder for now.
    
    
    return fig

application = server

if __name__ == '__main__':
    dash_app.run(debug=True)
#     dash_app.run_server(host="0.0.0.0", port="8050")
#     Will be put on wifi if launched

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)
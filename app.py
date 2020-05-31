# -*- coding: utf-8 -*-
__author__ = "Nitin Patil"

import math
import pandas as pd
from flask_caching import Cache

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table import DataTable
#from dash_table.Format import Sign
import dash_table.FormatTemplate as FormatTemplate

import plotly.graph_objects as go
from plotly.subplots import make_subplots

cache = Cache(config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './cache/'
})
TIMEOUT = 60

# To print number with commna separator 10,000,000
#num = 10000000
#print(f"{num:,d}")

##########################################################################
PATH = "./data"
def last_update():
    with open("./data/LastUpdate.txt", "r") as f:
        update_date = f.read()
        return (f"""Last updated on {update_date} GMT+5:30""")

df_ledger = pd.read_csv(f"{PATH}/Ledger.csv")
##########################################################################

def create_datatable_world(id):

    df = df_ledger

    return DataTable(id=id,
                    
                    columns=[{"name": i, "id": i}
                             for i in df.columns],
                    editable=True,
                    row_deletable=True,
                    data=df.to_dict("rows"),
                    row_selectable=False, #"single" if countryName != 'Schengen' else False,
                    sort_action="native",
                    style_as_list_view=True,
                    style_cell={'font_family': 'Helvetica',
                                'font_size': '1.1rem',
                                'padding': '.1rem',
                                'backgroundColor': '#ffffff', },
                    fixed_rows={'headers': True, 'data': 0},
                    style_table={'minHeight': '600px',
                                 'height': '600px',
                                 'maxHeight': '600px',
                                 },
                    style_header={'backgroundColor': '#ffffff',
                                  'fontWeight': 'bold'},
                    export_format='csv',
                    #export_headers='display', # only supported for export_format: xlsx
                    merge_duplicate_headers=True,
                    
                        )




##########################################################################

external_stylesheets = [#"https://codepen.io/plotly/pen/EQZeaW.css",
                        "./assets/Base.css"]

TITLE="MyAccount"
DESCRIPTION = "Simple and hassle free way to maintain all the accounts."

app = Dash(__name__, external_stylesheets=external_stylesheets,
                assets_folder='./assets/',
                meta_tags=[
                    {"name": "author", "content": "Nitin Patil"},
                    {"name": "keywords", "content": "MyAccount, ledger, account, tally, ctron"},
                    {"name": "description", "content": DESCRIPTION},
                    {"property": "og:title", "content": TITLE},
                    {"property": "og:type", "content": "website"},
                    {"property": "og:image", "content": "share_img.png"},
                    {"property": "og:url", "content": "https://moneymantra.herokuapp.com/"},
                    {"property": "og:description", "content":DESCRIPTION},
                    {"name": "twitter:card", "content": "summary_large_image"},
                    {"name": "twitter:site", "content": "@_nitinp"},
                    {"name": "twitter:title", "content": TITLE},
                    {"name": "twitter:description","content": DESCRIPTION},
                    #{"name": "twitter:image", "content": 'https://github.com/nitinai/coronavirus_dash/blob/master/assets/share_img.png'},
                    {"charset":"UTF-8"},
                    {"name": "viewport", "content": "width=device-width, height=device-height, initial-scale=1.0"}, #, shrink-to-fit=no
                    {"name": "X-UA-Compatible", "content": "ie=edge"},
                ])

app.title = TITLE

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-MQ9HJRF');</script>
        <!-- End Google Tag Manager -->
        
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- <script type='text/javascript' src='https://platform-api.sharethis.com/js/sharethis.js#property=5e8a16e50febbf0019e83180&product=sticky-share-buttons&cms=sop' async='async'></script> -->
    </head>
    <body>
        <!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MQ9HJRF"
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->

        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.config['suppress_callback_exceptions'] = True

server = app.server # the Flask app to run it on web server

# flash_caching
cache.init_app(server)

app.layout = html.Div([

    # Title bar
    html.Div([
        html.Div([
            
            html.H4(TITLE),

        ], className="banner"),
    ]),

    # all_content
    html.Div([
        
        html.Div([

            html.Div([
                dcc.Tabs(
                        id="tabs_world_table",
                        value='My Ledger',
                        parent_className='custom-tabs',
                        className='custom-tabs-container',
                        children=[
                            dcc.Tab(
                                    id='tab_world_table',
                                    label='My Ledger',
                                    value='My Ledger',
                                    className='custom-tab',
                                    selected_className='custom-tab--selected',
                                    children=[
                                    create_datatable_world(id="world_countries_table"), 
                                    ]
                                    ),
                            
                        ],
                        #style = {"margin-left": "2rem","margin-right": "2rem"}
                                ), 
            ], className="last_update"),

            html.Button('Add Row', id='editing-rows-button', n_clicks=0),
            html.Button('Save Data', id='save_table_button', n_clicks=0),
            html.P(id="save_table_btn_msg")
        ], className="row"),

        html.Div([
            html.Hr(),
        ]),

        # Footer
        html.Div([
            
            html.P(
            children=["Developed by NITIN PATIL | If you have any feedback on this app, please let him know on ", 
            html.A('Twitter', href='https://twitter.com/intent/tweet?source=webclient&text=%40_nitinp', target='_blank')
                    ]),

            ], id='my-footer',),

    ],className="all_content"), # excluding the title bar

])


@app.callback(
    Output('world_countries_table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('world_countries_table', 'data'),
     State('world_countries_table', 'columns')])
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    Output('save_table_btn_msg', 'children'),
    [Input('save_table_button', 'n_clicks')],
    [State('world_countries_table', 'data'),
     State('world_countries_table', 'columns')])
def add_row(n_clicks, data, columns):
    msg=""
    #print(type(data))
    #print(len(data))
    #msg = str(type(data))+ ' ' + str(len(data)) + " " + str(data[0])
    if n_clicks > 0:
        df = pd.DataFrame(data)
        df.to_csv(f"{PATH}/Saved.csv")
        msg="Data save successfully"
    return msg

if __name__ == '__main__':
    app.run_server(debug=True)

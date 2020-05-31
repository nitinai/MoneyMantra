# -*- coding: utf-8 -*-
__author__ = "Nitin Patil"

import math
import pandas as pd
from flask_caching import Cache

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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


##########################################################################



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

    html.Div([
        
        html.Div([

            html.Div([
                html.P(children=last_update()), 
            ], className="last_update"),

            html.Hr(),
        ], className="row"),

        html.Div([
            html.Hr(),
        ]),

        # Footer
        html.Div([
            
            html.P(
            children=["Developed by NITIN PATIL | If you have any feedback on this dashboard, please let him know on ", 
            html.A('Twitter', href='https://twitter.com/intent/tweet?source=webclient&text=%40_nitinp', target='_blank')
                    ]),

            ], id='my-footer',),

    ],className="all_content"), # excluding the title bar

])


if __name__ == '__main__':
    app.run_server(debug=True)

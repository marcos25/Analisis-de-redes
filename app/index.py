from main import app

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import graph
import main_app

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

main_menu = html.Div([

    dbc.Container([
        dbc.Row([
            html.H1('Network Graphs Visualization'),
        ], justify='center', className='m-1'),
        dbc.Row([
            html.Img(src="assets/images/main_image.png", width="60%")
        ], justify='center', className='m-1'),

        html.Br(),

        html.Table([

            html.Tr(
                dcc.Link('Start', href='main_app', className='btn btn-primary btn-lg', style={'width': '100%'}),
            ),
         
        ], style={'margin-left':'auto', 'margin-right':'auto', 'border-collapse':'separate', 'border-spacing':'17px'}),
    ])

])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return main_menu
    elif pathname == '/main_app':
        return main_app.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False)

from main import app
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import graph
import digraph
import transport_network

# ----- Dropdown menu for 
data_structures = ['Graph', "Directed Graph", "Transport Network"]
select_data_structure_dropdown = dcc.Dropdown(
    id='select-data-structure-dropdown',
    value='Graph',
    clearable=False,
    options=[ {'label': name.capitalize(), 'value': name} for name in data_structures],
    style={"width":"14em"}
)

layout = html.Div([
    # Title of the page
    dbc.Row([
            html.H1('Graph', id="title"),
    ], justify='center', className='position-relative'),


    dbc.Row([
        # Left column
        html.Div([
            html.H4('Select Data Structure'),
            select_data_structure_dropdown,

            html.Br()
        ], className="col-md-6"),
    ]),

    html.Div([], id="data-structure-div")
])

@app.callback(
    [Output("data-structure-div", "children"), Output("title", "children")],
    Input("select-data-structure-dropdown", "value")
)
def x(select_data_structure_dropdown_value):
    if select_data_structure_dropdown_value == "Graph":
        return graph.layout, "Graph"
    elif select_data_structure_dropdown_value == "Directed Graph":
        return digraph.layout, "Directed Graph"
    else:
        return transport_network.layout, "Transport Network"

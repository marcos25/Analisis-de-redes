import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd  # pip install pandas
import plotly.express as px
import random
from red import *
import base64
import uuid

from main import app

# ----- Dropdown menu for algorithm selection -----
algorithms = ["Find maximum flow using Ford-Fulkerson algorithm", 
              "Find minimum-cost flow using Primal algorithm",
              "Find minimum-cost flow using Dual algorithm",
              "Find total minimum-cost flow using Simplex algorithm"]

select_algorithm_dropdown = dcc.Dropdown(
    id='select-algorithm-dropown-network',
    value="Find maximum flow using Ford-Fulkerson algorithm",
    clearable=False,
    options=[ {'label': name, 'value': name} for name in algorithms],
    style={"width":"32em"}
)
# -------------------------------------------------------

default_stylesheet =[{
                        'selector': '.edge',
                        'style':{
                            'curve-style': 'bezier',
                            'label': 'data(restrictions)',
                            'target-arrow-shape': 'triangle',
                        }
                    },

                    {
                        'selector': '.red_edges',
                        'style':{
                            'curve-style': 'bezier',
                            'label': 'data(restrictions)',
                            'line-color': '#FF8080',
                            'target-arrow-shape': 'triangle'
                        }
                    },

                    {
                        'selector': '.blue_edges',
                        'style':{
                            'curve-style': 'bezier',
                            'label': 'data(restrictions)',
                            'line-color': '#80B7FF',
                            'target-arrow-shape': 'triangle',
                        }
                    },

                    {
                        'selector': '.node',
                        'style': {
                            'content': 'data(label)',
                            'text-halign':'center',
                            'text-valign':'center',
                            'width':'30px',
                            'height':'30px'
                        }
                    },

                    {
                        'selector':'.red_nodes',
                        'style':{
                            'content': 'data(label)',
                            'text-halign':'center',
                            'text-valign':'center',
                            'width':'30px',
                            'height':'30px',
                            'background-color': '#FF8080'
                        }
                    },

                    {
                        'selector':'.blue_nodes',
                        'style':{
                            'content': 'data(label)',
                            'text-halign':'center',
                            'text-valign':'center',
                            'width':'30px',
                            'height':'30px',
                            'background-color': '#80B7FF'
                        }
                    }]

# ----- Dash Cytoscape instance to display data structures -----
canvas = cyto.Cytoscape(
            id='network',
            minZoom=0.2,
            maxZoom=1,
            layout={'name': 'preset'},
            boxSelectionEnabled = True,
            style={'width': '100%', 'height': '500px'},
            elements={'nodes': [], 'edges': []},
            stylesheet=default_stylesheet
        )
# -------------------------------------------------------

# ----- Modals fixed position to allow the user to see the graph while he's updating it -----
modals_position = {
                    "position": "absolute",
                    "top": "0",
                    "right": "0",
                    "bottom": "0",
                    "left": "50%",
                    "z-index": "10040",
                    "overflow": "auto",
                    "overflow-y": "auto"
                }
# -------------------------------------------------------

# ----- Modal to edit nodes -----
edit_nodes_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Edit Nodes"),
                dbc.ModalBody(
                   id="edit-nodes-modal-body-network"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-nodes-modal-network", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-nodes-modal-network", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-nodes-modal-network",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=False, 
            fade=True,
            style=modals_position
        )
    ]
)
# -------------------------------------------------------
edit_edges_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Edit edge"),
                dbc.ModalBody(
                   id="edit-edges-modal-body-network"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-edges-modal-network", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-edges-modal-network", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-edges-modal-network",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=False, 
            fade=True,
            style=modals_position
        )
    ]
)

# ----- Modal to select source and sink nodes -----
select_source_and_sink_nodes_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Select Source And Sink Nodes"),
                dbc.ModalBody(
                   id="select-source-and-sink-nodes-modal-body"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-select-source-and-sink-nodes-modal", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-select-source-and-sink-nodes-modal", className="ml-auto")
                        ]
                    )
                )
            ],
            id="select-source-and-sink-nodes-modal",
            is_open=False,
            size="lg", #sm, lg, xl
            backdrop=True, # to be or not to be closed by clicking on backdrop
            scrollable=True, # Scrollable if modal has a lot of text
            centered=False, 
            fade=True,
            style=modals_position
        )
    ]
)


# ----- MAIN LAYOUT -----
layout = html.Div(children=[
    # ----- Store objects to store nodes and edges information -----
    dcc.Store(
        id='nodes-info-network', data=[['a', 1]] # The first element is the first node name that we will use
    ),

    dcc.Store(
        id='network-copy', data=None
    ),
 
    # 1- No nodes selected when edit node button is clicked
    # 2- No nodes selected when remove node button is clicked
    # 3- No nodes selected when add edge button is clicked
    # 4- More than two nodes selected when add edge button is clicked
    dcc.Store(
        id='alert-info-network', data=None
    ),

    # Object to store a flag to run simplex algorithm. the only one which doesn't need to show
    # the source and sink nodes selection modal
    dcc.Store(
        id='info-run-simplex', data=None
    ),

    # ----- Div to display nodes errors -----
    html.Div(id="edit-nodes-alert-network", children=[]),

    edit_nodes_modal,
    
    edit_edges_modal,
    
    select_source_and_sink_nodes_modal,

    dbc.Row([
        # Left column
        dbc.Col([
            html.Div([
                dbc.Alert(id="alert-network", is_open=False, dismissable=True, color="warning"),
                canvas,
            ], className="border border-secondary rounded"),

            html.Br(),

            dbc.Row([
                html.H4("Controls"),
            ], justify="center"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H5("Nodes", className="text-muted"),   
                        dbc.Button("Add", id="add-node-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-nodes-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-nodes-btn-network", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),

                dbc.Col([
                    html.Div([
                        html.H5("Edges", className="text-muted"),   
                        dbc.Button("Add", id="add-edge-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-edges-btn-network", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-edges-btn-network", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Row([
                dcc.Upload([
                    dbc.Button("Upload transport network from file", className="mr-1", color="success"),
                ], id="upload-network-obj")
                
            ], justify="center")
        ], md=6),

        # Right Column
        dbc.Col([
            html.Div([
                    html.H4('Select Algorithm'),
                html.Table([

                    html.Tr([
                        html.Td([
                            select_algorithm_dropdown
                        ]),
                        html.Td([
                            dbc.Button("Run", id="run-algorithm-btn-network",size="sm", className="btn btn-warning mr-1"),
                            dbc.Button("Clear", id="clear-result-btn-network",size="sm", className="btn btn-success mr-1"),
                        ], style={"padding":"1em"}),
                        
                    ])
                ]), 
            ]),

            html.Br(),

            html.Div([
                    html.H4('Result'),
                    html.P(id="result-text-network"),
            ], id="result-div-network", style={'display':'None'}),

            html.Br(),
            html.Br(),
            html.Br(),

            html.Div([
                html.H4('Transport Network Information'),

                html.Table([

                    html.Tr([
                        html.Td([
                            html.Label("Number of nodes:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-nodes-label-network", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.Label("Number of edges:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-edges-label-network", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ])
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([
                html.H4("Nodes Information"),
            ], justify="center"),

            html.Div([
                dbc.Table([
                
                    # Head of the table
                    html.Thead([
                        html.Tr([
                            html.Th([
                                html.H5("Node", className="text-muted"),   
                            ], style={"text-align":"center", "width":"16.6%"}),

                            html.Th([
                                html.H5("Positive Degree", className="text-muted"),   
                            ], style={"text-align":"center", "width":"16.6%"}),

                            html.Th([
                                html.H5("Negative Degree", className="text-muted"),   
                            ], style={"text-align":"center", "width":"16.6%"}),

                            html.Th([
                                html.H5("Min. Restriction", className="text-muted"),   
                            ], style={"text-align":"center", "width":"16.6%"}),

                            html.Th([
                                html.H5("Max. Restriction", className="text-muted"),   
                            ], style={"text-align":"center", "width":"16.6%"}),

                            html.Th([
                                html.H5("Supply/Demand", className="text-muted"),   
                            ], style={"text-align":"center", "width":"16.6%"}),
                        ])
                    ]),
                        
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"width":"100%"}),

            
            html.Div([
                dbc.Table([
                    # Body of the table
                    html.Tbody(id="nodes-degrees-table-network", children=[])
                ],bordered=False, responsive=False),
                

            ], style={"position":"relative", "height":"200px", "overflow":"auto", "display":"block", "justify":"center"}),
            
        ], md=6)

    ]),    
])

# ----- Callback to update the graph -----
@app.callback(
    [Output("network", "elements"), Output("nodes-degrees-table-network", "children"), 
     Output("number-of-nodes-label-network", "children"), Output("alert-info-network", "data"), 
     Output("number-of-edges-label-network", "children"), Output('nodes-info-network', 'data'), 
     Output('upload-network-obj', 'contents'),
     Output('result-text-network', 'children'), Output('result-div-network', 'style'),
     Output('network-copy', 'data')],

    [Input("add-node-btn-network", "n_clicks"), Input("done-btn-edit-nodes-modal-network", "n_clicks"),
     Input("remove-nodes-btn-network", "n_clicks"), Input("edit-nodes-btn-network", "n_clicks"),
     Input("add-edge-btn-network", "n_clicks"), Input("done-btn-edit-edges-modal-network", "n_clicks"),
     Input("edit-edges-btn-network", "n_clicks"), Input('remove-edges-btn-network', 'n_clicks'), 
     Input('upload-network-obj', 'contents'), Input('run-algorithm-btn-network', 'n_clicks'),
     Input('clear-result-btn-network', 'n_clicks'), Input("done-btn-select-source-and-sink-nodes-modal", "n_clicks")],
    
    [State("network", "elements"), State("nodes-degrees-table-network", "children"), 
     State("number-of-nodes-label-network", "children"), State("edit-nodes-modal-body-network", "children"), 
     State("network", "selectedNodeData"), State("number-of-edges-label-network", "children"), 
     State("edit-edges-modal-body-network", "children"), State("network", "selectedEdgeData"), 
     State('nodes-info-network', 'data'), State('select-algorithm-dropown-network', 'value'),
     State('result-text-network', 'children'), State('result-div-network', 'style'),
     State('network-copy', 'data'), State("select-source-and-sink-nodes-modal-body", "children")]
)
def updateNetwork(add_node_btn_n_clicks, done_btn_edit_nodes_modal, remove_nodes_btn, edit_nodes_btn,
    add_edge_btn, done_btn_edit_edges_modal, edit_edges_btn, remove_edges_btn, upload_graph_contents,
    run_algorithm_btn, clear_result_btn, done_btn_select_source_and_sink_nodes, graph_elements, nodes_degrees_table_children, number_of_nodes, 
    edit_nodes_modal_body_childrens, selected_node_data, number_of_edges, edit_edges_modal_body_childrens, 
    selected_edge_data, nodes_info, select_algorithm_dropdown, result_text_children, result_div_style,
    graph_copy,select_source_and_sink_nodes_modal_body_children):
    # Getting the callback context to know which input triggered this callback
    ctx = dash.callback_context

    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        btn_triggered = ctx.triggered[0]['prop_id'].split('.')[0]

        # ----- Add node case -----
        if btn_triggered == "add-node-btn-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None

            # Getting an unique initial name
            while True:
                node_name = nodes_info[0][0] * nodes_info[0][1]
                repeated_name = False

                for node in graph_elements['nodes']:
                    if node['data']['label'] == node_name:
                        repeated_name = True
                        # Updating the node label if it's necesary
                        if node_name[-1] == 'z':    
                            nodes_info[0][0] = 'a'
                            nodes_info[0][1] += 1
                        else:    
                            nodes_info[0][0] = chr(ord(nodes_info[0][0]) + 1)
                        break
                
                if not repeated_name:
                    break
            
            # Getting a unique node id
            node_id = str(uuid.uuid1())

            # Adding the node to the graph_elements
            node = {'data': {'id': node_id, 'label': node_name, 'positive_degree':0, 'negative_degree':0,
                    'min_restriction':0, 'max_restriction':"Inf", 'supply/demand':0},
                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                    'classes':'node'}
            
            graph_elements['nodes'].append(node)

            # Adding the node to the node_degrees_table
            nodes_degrees_table_children.append(html.Tr([
                html.Td(node_name, style={"text-align":"center"}), 
                html.Td(node['data']['positive_degree'],  style={"text-align":"center", "width":"16.6%"}),
                html.Td(node['data']['negative_degree'],  style={"text-align":"center", "width":"16.6%"}),
                html.Td(node['data']['min_restriction'],  style={"text-align":"center", "width":"16.6%"}),
                html.Td("Inf",  style={"text-align":"center", "width":"16.6%"}),
                html.Td(node['data']['supply/demand'],  style={"text-align":"center", "width":"16.6%"}),
            ], className="table-primary")),
                

            # Updating the node label if it's necesary
            if node_name[-1] == 'z':    
                nodes_info[0][0] = 'a'
                nodes_info[0][1] += 1
            else:    
                nodes_info[0][0] = chr(ord(nodes_info[0][0]) + 1)
            
            print("ADD NODE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes+1, None, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ----- Edit nodes case -----
        elif btn_triggered == "done-btn-edit-nodes-modal-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None

            # Excluding the H3 elements
            edit_nodes_modal_body_childrens = [c for c in edit_nodes_modal_body_childrens if edit_nodes_modal_body_childrens.index(c) % 2 == 1]

            for children in edit_nodes_modal_body_childrens:
                # Getting the new label
                try:
                    # if exists, get it 
                    new_label = children['props']['children'][0]['props']['children'][3]['props']['value']

                    # Checking if the new label is repeated or not
                    repeated_label = False
                    for node in graph_elements['nodes']:
                        if node['data']['label'] == new_label:
                            repeated_label = True
                            break
                    # If the label is repeated, then keep the current label for the node
                    if repeated_label:
                        new_label = children['props']['children'][0]['props']['children'][1]['props']['children']
                    
                except:
                    # If no new label exists, get the current label as new and current label
                    new_label = children['props']['children'][0]['props']['children'][1]['props']['children']
                
                # Getting the current label
                current_label = children['props']['children'][0]['props']['children'][1]['props']['children']


                # Getting the new min restriction
                try:
                    # if exists, get it
                    new_min_restriction = children['props']['children'][1]['props']['children'][3]['props']['value']
                except:
                    # If doesn't exists, new min restriction will be as same as current min restriction
                    new_min_restriction = children['props']['children'][1]['props']['children'][1]['props']['children']
                
                # Getting the current restriction as number (this always be possible because it is inicially 0)
                current_min_restriction = float(children['props']['children'][1]['props']['children'][1]['props']['children'])

                # validate if new min restriction is a numbrer
                try:
                    # if it is, then cast it to float EXCEPT IF ITS INFINITE
                    new_min_restriction = float(new_min_restriction)
                    if new_min_restriction == math.inf:
                        new_min_restriction = current_min_restriction    
                except:
                    # If it isn't, do new min restriction = current min restriction
                    new_min_restriction = current_min_restriction
                
                

                # Getting the new max restriction
                try:
                    # if exists, get it
                    new_max_restriction = children['props']['children'][2]['props']['children'][3]['props']['value']
                except:
                    # If doesn't exists, new max restriction will be as same as current max restriction
                    new_max_restriction = children['props']['children'][2]['props']['children'][1]['props']['children']
                
                # Getting the current max restriction as number (inicially "Inf")
                current_max_restriction = float(children['props']['children'][2]['props']['children'][1]['props']['children'])
                
                # validate if new max restriction is a numbrer
                try:
                    # if it is, then cast it to float
                    new_max_restriction = float(new_max_restriction)    
                except:
                    # If it isn't, do new min restriction = current min restriction
                    new_max_restriction = current_max_restriction
                
                # Getting the new supply/demand
                try:
                    # if exists, get it
                    new_supply_demand = children['props']['children'][3]['props']['children'][3]['props']['value']
                    # Validate if is a number
                    new_supply_demand = float(new_supply_demand)
                    # Validate if is not +inf or -inf
                    if new_supply_demand == math.inf or new_supply_demand == -math.inf:
                        raise Exception()
                except:
                    # If doesn't exists, new supply_demand will be as same as current supply demand
                    new_supply_demand = float(children['props']['children'][3]['props']['children'][1]['props']['children'])
                

                
                # Validate if new min restriction is at least 0. If it isn't, then new min restriction
                # will be as same as current min restriction which alway is greater or equal than 0
                # The same will happen if new_min_restriction is greater than new_max_restriction
                if new_min_restriction < 0 or new_min_restriction > new_max_restriction:
                    new_min_restriction = current_min_restriction

                # Validate if new max restriction is equal or greater than min restriction
                # If new max restriction is Inf, then always min restriction is ok
                if new_max_restriction != math.inf:
                    if new_max_restriction < new_min_restriction:
                        new_max_restriction = current_max_restriction

                # Editing the node in graph_elements
                for node in graph_elements['nodes']:
                    if node['data']['label'] == current_label:
                        # Updating the label
                        node['data']['label'] = new_label
                        # Updating the min restriction
                        node['data']['min_restriction'] = new_min_restriction
                        # Updating the max restriction
                        if new_max_restriction == math.inf:
                            node['data']['max_restriction'] = "Inf"
                        else:
                            node['data']['max_restriction'] = new_max_restriction
                        
                        # Updating the supply/emand
                        node['data']['supply/demand'] = new_supply_demand
                        break
            
                # Editing edges in graph_elements (only if node label has changed)
                if new_label != current_label:
                    for edge in graph_elements['edges']:
                        # Editing edges elements
                        if edge['data']['source_node'] == current_label:
                            edge['data']['source_node'] = new_label
                            
                        if edge['data']['target_node'] == current_label:
                            edge['data']['target_node'] = new_label

            
                # Editing the nodes in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == current_label:
                        # Updating the name
                        children['props']['children'][0]['props']['children'] = new_label
                        # Updating the min restriction
                        children['props']['children'][3]['props']['children'] = new_min_restriction
                        # Updating the max restriction
                        if new_max_restriction == math.inf:
                            children['props']['children'][4]['props']['children'] = "Inf"
                        else:
                            children['props']['children'][4]['props']['children'] = new_max_restriction
                        # Updating the supply/demand
                        children['props']['children'][5]['props']['children'] = new_supply_demand
                        break

            print("EDIT NODE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, None, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ---- Edit nodes button alert handle -----
        elif btn_triggered == "edit-nodes-btn-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            print("Selected node data")
            print(selected_node_data)
            if not selected_node_data:
                alert = 1
                print("NADA SELECCIONADO")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy

        # ----- Remove nodes case ------
        elif btn_triggered == "remove-nodes-btn-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            if selected_node_data:
                # The ids of the nodes to remove are in selected node data
                selected_ids = [selectedNode['id'] for selectedNode in selected_node_data]
                selected_labels = [selectedNode['label'] for selectedNode in selected_node_data]

                # Keeping the non selected nodes in graph_elements['nodes']
                graph_elements['nodes'] = [n for n in graph_elements['nodes'] if n['data']['id'] not in selected_ids]
                # Removing all edges in graph_elements['edges'] if one of their vertices is a selected node
                graph_elements['edges'] = [e for e in graph_elements['edges'] if e['data']['source'] not in selected_ids and e['data']['target'] not in selected_ids]

                #Removing deleted nodes from nodes degrees table
                nodes_degrees_table_children = [c for c in nodes_degrees_table_children if c['props']['children'][0]['props']['children'] not in selected_labels]


                # Updating the degrees of remaining nodes in the nodes degrees table
                degrees = {c['props']['children'][0]['props']['children']:{'positive_degree':0, 'negative_degree':0} for c in nodes_degrees_table_children}

                for edge in graph_elements['edges']:
                    degrees[edge['data']['source_node']]['positive_degree'] += 1
                    degrees[edge['data']['target_node']]['negative_degree'] += 1

                for c in nodes_degrees_table_children:
                    node_name = c['props']['children'][0]['props']['children'] 
                    c['props']['children'][1]['props']['children'] = str(degrees[node_name]['positive_degree'])
                    c['props']['children'][2]['props']['children'] = str(degrees[node_name]['negative_degree'])

                # Updating number of nodes and number of edges
                number_of_nodes -= len(selected_ids)
                number_of_edges = len(graph_elements['edges'])
            else:
                alert = 2
            
            print("REMOVE NODE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ----- Add Edge case -----
        elif btn_triggered == "add-edge-btn-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            # When no node is selected
            if not selected_node_data:
                alert = 3
            # When more than two nodes are selected
            elif len(selected_node_data) > 2:
                alert = 4
            # When exactly one node is selected (loop)
            elif len(selected_node_data) == 1:
                node = selected_node_data[0]['id']
                node_label = selected_node_data[0]['label']
                loop_id = str(uuid.uuid1())

                # Restrictions are: [min_restriction, flow, max_restriction, cost]
                loop = {'data': {'source': node, 
                            'target': node, 'restrictions': [0,0,"Inf", 0], 'id':loop_id, 'source_node':node_label, 'target_node':node_label},
                            'classes':'edge'}
                graph_elements['edges'].append(loop)

                # Updating the node degree in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == node_label:
                        current_positive_degree = int(children['props']['children'][1]['props']['children'])
                        children['props']['children'][1]['props']['children'] = str(current_positive_degree + 1)
                        current_negative_degree = int(children['props']['children'][2]['props']['children'])
                        children['props']['children'][2]['props']['children'] = str(current_negative_degree + 1)
                        
                        break

                number_of_edges += 1
            # When exactly two nodes are selected (edge)
            elif len(selected_node_data) == 2:

                # Node1 is the source, Node2 is the target
                node1 = selected_node_data[0]['id']
                node2 = selected_node_data[1]['id']

                node1_label = selected_node_data[0]['label']
                node2_label = selected_node_data[1]['label']

                edge_id = str(uuid.uuid1())
                edge = {'data': { 'source': node1, 
                                'target': node2, 'restrictions': [0,0,"Inf", 0], 'id':edge_id, 'source_node':node1_label, 'target_node':node2_label},
                                'classes':'edge'}
                graph_elements['edges'].append(edge)

                # Updating the node degree in the nodes degrees table
                n_edited_nodes = 0
                for children in nodes_degrees_table_children:
                    # Updating the positive degree of the source node (node1)
                    if children['props']['children'][0]['props']['children'] == node1_label:
                        current_positive_degree = int(children['props']['children'][1]['props']['children'])
                        children['props']['children'][1]['props']['children'] = str(current_positive_degree + 1)
                        n_edited_nodes += 1
                    
                    # Updating the negative degree of the target node
                    if children['props']['children'][0]['props']['children'] == node2_label:
                        current_negative_degree = int(children['props']['children'][2]['props']['children'])
                        children['props']['children'][2]['props']['children'] = str(current_negative_degree + 1)
                        n_edited_nodes += 1
                    
                    if n_edited_nodes == 2:
                        break

                number_of_edges += 1

            print("ADD EDGE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ----- Edit edges case -----
        elif btn_triggered == "done-btn-edit-edges-modal-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            radio_buttons = [c for c in edit_edges_modal_body_childrens if edit_edges_modal_body_childrens.index(c) % 2 == 0]
            edit_edges_modal_body_childrens = [c for c in edit_edges_modal_body_childrens if c not in radio_buttons]
            
            for r in radio_buttons:
                continue
                # Button checked
                
            
            for c,r in zip(edit_edges_modal_body_childrens, radio_buttons):
                print(c, "\n\n")
                # Getting hidden input Object with edge data
                edge_data = c['props']['children'][0]['props']['children'][0]['props']['value']
                
                #Getting the edge's id
                edge_id = edge_data[0]
                #Getting the edge's source node
                node1 = edge_data[1]
                #Getting the edge's target node
                node2 = edge_data[2]

                # trying to get radio button value to know if we need to chenage edge's direction
                try:
                    change_direction = r['props']['children'][1]['props']['checked']
                except:
                    change_direction = False
                
                # Getting current min restriction
                current_min_restriction = float(c['props']['children'][0]['props']['children'][2]['props']['children'])

                # Trying to get new min restriction 
                try:
                    new_min_restriction = c['props']['children'][0]['props']['children'][4]['props']['value']
                    # Validate if it is a number, not infinite and greater or equal than 0
                    new_min_restriction = float(new_min_restriction)
                    if new_min_restriction == math.inf or new_min_restriction < 0:
                        raise Exception()
                except:
                    # If there isn't new min restriction, or new min restriction is not a number or
                    # it's infinite, or is len than 0, then new min restriction = current min restriction
                    new_min_restriction = current_min_restriction
                
                # Getting current flow
                current_flow = float(c['props']['children'][1]['props']['children'][1]['props']['children'])

                # Trying to get new flow
                try:
                    new_flow = c['props']['children'][1]['props']['children'][3]['props']['value']
                    # Validate if it is a number, not infinite and greater or equal than 0
                    new_flow = float(new_flow)
                    if new_flow == math.inf or new_flow < 0:
                        raise Exception()
                except:
                    # If there isn't new flow, or new flow is not a number or
                    # it's infinite, or is less than 0, then new flow = current flow
                    new_flow = current_flow
                
                # Getting current capacity
                current_capacity = float(c['props']['children'][2]['props']['children'][1]['props']['children'])

                # Trying to get new capacity
                try:
                    new_capacity = c['props']['children'][2]['props']['children'][3]['props']['value']
                    # Validate if it's a number (can be infinite) and if it is greater than 0
                    new_capacity = float(new_capacity)
                    if new_capacity < 0:
                        raise Exception()
                except:
                    # If there isn't new capacity, or new capactity is 
                    # less than 0, then new capacity = current capacity
                    new_capacity = current_capacity
                
                # Getting current cost
                current_cost = float(c['props']['children'][3]['props']['children'][1]['props']['children'])
                
                # Trying to get new cost
                try:
                    new_cost = c['props']['children'][3]['props']['children'][3]['props']['value']
                    # Validate if it's a number (can not be infinite) and if it is greater than 0
                    new_cost = float(new_cost)
                    if new_cost == math.inf:
                        raise Exception()
                except:
                    # If there isn't new cost, or new cost is 
                    # infinite, then new cost = current cost
                    new_cost = current_cost
                
                # Validate min_restriction
                if new_min_restriction > new_capacity:
                    new_min_restriction = current_min_restriction
                
                # Validate new flow
                if new_flow > new_capacity:
                    new_flow = current_flow
                
                # Validate new capacity
                if new_capacity < new_min_restriction or new_capacity < new_flow:
                    new_capacity = current_capacity
                
                # *New cost doesn't need validation since it is independent of others restrictions*
                
                # Change direction if it is needed
                if change_direction:
                    # Swap source and target in the edge and update its weight
                    for edge in graph_elements['edges']:
                        if edge['data']['id'] == edge_id:
                            # Swap the source and target (ids and labels)
                            tmp = edge['data']['source']
                            edge['data']['source'] = edge['data']['target']
                            edge['data']['target'] = tmp

                            tmp = edge['data']['source_node']
                            edge['data']['source_node'] = edge['data']['target_node']
                            edge['data']['target_node'] = tmp

                            # update restrictions
                            # min restriction
                            edge['data']['restrictions'][0] = new_min_restriction
                            # flow
                            edge['data']['restrictions'][1] = new_flow
                            # capacity
                            if new_capacity == math.inf:
                                edge['data']['restrictions'][2] = "Inf"
                            else:
                                edge['data']['restrictions'][2] = new_capacity
                            break
                    
                    # Update the degrees of the nodes
                    nodes_updated = 0
                    for node in graph_elements['nodes']:
                        if nodes_updated == 2:
                            break

                        if node['data']['label'] == node1:
                            node['data']['positive_degree'] -= 1
                            node['data']['negative_degree'] += 1
                            nodes_updated += 1
                            continue
                        elif node['data']['label'] == node2:
                            node['data']['positive_degree'] += 1
                            node['data']['negative_degree'] -= 1
                            nodes_updated += 1
                            continue

                    
                    # Update the degrees in the nodes degrees table
                    nodes_updated = 0
                    for c in nodes_degrees_table_children:
                        if nodes_updated == 2:
                            break

                        node_name = c['props']['children'][0]['props']['children'] 
                        positive_degree = c['props']['children'][1]['props']['children']
                        negative_degree = c['props']['children'][2]['props']['children']

                        if node_name == node1:
                            c['props']['children'][1]['props']['children'] = str(int(positive_degree) -1)
                            c['props']['children'][2]['props']['children'] = str(int(negative_degree) + 1)
                            nodes_updated += 1
                            continue
                        elif node_name == node2:
                            c['props']['children'][1]['props']['children'] = str(int(positive_degree) + 1)
                            c['props']['children'][2]['props']['children'] = str(int(negative_degree) - 1)
                            nodes_updated += 1
                            continue
                
                # If we dont need to change the direction of the edge, then just update its restrictions
                for edge in graph_elements['edges']:
                    if edge['data']['id'] == edge_id:
                        # min restriction
                        edge['data']['restrictions'][0] = new_min_restriction
                        # flow
                        edge['data']['restrictions'][1] = new_flow
                        # capacity
                        if new_capacity == math.inf:
                            edge['data']['restrictions'][2] = "Inf"
                        else:
                            edge['data']['restrictions'][2] = new_capacity
                        # Cost
                        edge['data']['restrictions'][3] = new_cost
                        break

            print("EDIT EDGE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, None, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ---- Edit edges button alert handle -----
        elif btn_triggered == "edit-edges-btn-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            if not selected_edge_data:
                alert = 5
            
            
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ----- Remove edges case -----
        elif btn_triggered == "remove-edges-btn-network":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            if not selected_edge_data:
                alert = 6
            else:
                # Getting ids of selected edges
                ids = [e['id'] for e in selected_edge_data]

                # Keeping only the unselected edges in graph_elements
                graph_elements['edges'] = [e for e in graph_elements['edges'] if e['data']['id'] not in ids]

                # Updating the number of edges
                number_of_edges -= len(ids)

                # Updating the degrees of remaining nodes in the nodes degrees table
                degrees = {c['props']['children'][0]['props']['children']: {'positive_degree':int(c['props']['children'][1]['props']['children']), 'negative_degree':int(c['props']['children'][2]['props']['children']),} for c in nodes_degrees_table_children}

                for edge in selected_edge_data:
                    degrees[edge['source_node']]['positive_degree'] -= 1
                    degrees[edge['target_node']]['negative_degree'] -= 1

                for c in nodes_degrees_table_children:
                    node_name = c['props']['children'][0]['props']['children'] 
                    c['props']['children'][1]['props']['children'] = str(degrees[node_name]['positive_degree'])
                    c['props']['children'][2]['props']['children'] = str(degrees[node_name]['negative_degree'])
            
            print("REMOVE EDGE CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
    
        # ----- Upload Graph Case -----
        elif btn_triggered == 'upload-network-obj':
            nodes_info = [['a',1]]
            # Read the file and convert it to list of elements
            content_type, content_string = upload_graph_contents.split(',')
            graph = [x.replace(" ", "").split(",") for x in base64.b64decode(content_string).decode('ascii').strip().split("\n") if x] 
            print(graph)

            alert = None
            nodes = [e for e in graph if len(e) == 4]
            edges = [e for e in graph if len(e) == 6]

            # Validate non repetitions in nodes labels
            labels = []
            for n in nodes:
                if n[0] not in labels:
                    labels.append(n[0])
                else:
                    # Repetition in nodes label
                    alert = 11
                    break
            # Validate if each node of an edge exists
            if not alert:
                for e in edges:
                    if e[0] not in labels or e[1] not in labels:
                        # Edge with nonexistent node
                        alert = 12
                        break

            # Validate the data format
            if not alert:
                for element in graph:
                    # Just accept edges: [a,b,min_res,flow,capacity,cost]
                    # or nodes: [a,min_res,max_res, cost]
                    if len(element) != 6 and len(element) != 4: 
                        alert = 7
                        break

                    # Nodes validation
                    if len(element) == 4:
                        # Validate if node restrictions are non negative numbers
                        try:
                            for i in range(1,3):
                                element[i] = float(element[i])
                                if element[i] < 0:
                                    raise Exception()
                        except:
                            # Restrictions aren't numbers or are negative numbers
                            alert = 8 
                            break
                        # Validate min restriction. As max_restriction just need to be greater than min_restriction,
                        # this case will also validate max_restriction
                        if element[1] == math.inf or element[1] > element[2]:
                            # Inconsistent node restrictions
                            alert = 9 
                            break

                    # Edges validation
                    if len(element) == 6:
                        # Validate if node restrictions (min_restriction, flow, max_restriction)are non negative numbers
                        try:
                            for i in range(2,5):
                                element[i] = float(element[i])
                                if element[i] < 0:
                                    raise Exception()
                        except:
                            # Restrictions aren't numbers or are negative numbers
                            alert = 8 
                            break

                        # Validate if cost is not infinite
                        try:
                            element[5] = float(element[5])
                            if element[i] == math.inf:
                                raise Exception()
                        except:
                            # Invalid cost.
                            alert = 13
                            break

                        # Validate min_restriction
                        if element[2] > element[4]:
                            # Inconsistent edges restrictions
                            alert = 10
                            break
                        
                        # Validate new flow
                        if element[3] > element[4]:
                            alert = 10
                            break
                        
                        # Validate new capacity
                        if element[4] < element[2] or element[4] < element[3]:
                            alert = 10
                            break

                        # *********** Cost need no validation since it is independent **********

            
            # If file format is ok, then we proceed to create the graph in the interface
            if not alert:
                # Resetting all variables
                new_nodes = []
                new_edges = []
                number_of_edges = 0
                number_of_nodes = 0
                data_info = ['a', 1]

                # To store nodes degrees and then create the table
                nodes_degrees = {}

                # Check if the elements are nodes or edges and add it to UI and data structure
                for element in graph:
                    element_splitted = element
                    # When it's a node
                    if len(element_splitted) == 4:
                        # Check if max restriction is Inf to store it as string
                        if element_splitted[2] == math.inf:
                            element_splitted[2] = 'Inf'

                        # Add it to the new nodes
                        node = {'data': {'id': str(uuid.uuid1()), 'label': element_splitted[0], 'positive_degree':0, 'negative_degree':0,
                                'min_restriction':element_splitted[1], 'max_restriction':element_splitted[2],
                                'supply/demand':element_splitted[3]},
                                'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                                'classes':'node'}

                        new_nodes.append(node)

                        # Adding the node to the degrees dict
                        nodes_degrees[element_splitted[0]] = {'positive_degree':0, 'negative_degree':0, 
                                                              'min_restriction':element_splitted[1],
                                                              'max_restriction':element_splitted[2],
                                                              'supply/demand':element_splitted[3]}
                        number_of_nodes += 1

                    # When it's an edge
                    else:
                        # To store nodes ids
                        node1_id = None
                        node2_id = None
                        
                        # add the edge between the nodes

                        # Find the node1 id
                        for n in new_nodes:
                            if n['data']['label'] == element_splitted[0]:
                                node1_id = n['data']['id']
                                break
                        
                        # Find the node2 id
                        for n in new_nodes:
                            if n['data']['label'] == element_splitted[1]:
                                node2_id = n['data']['id']
                                break

                        # Create the edge
                        edge_id = str(uuid.uuid1())
                        # Getting min restriction
                        min_restriction = element_splitted[2]
                        # Getting flow
                        flow = element_splitted[3]
                        # Getting cost
                        cost = element_splitted[5]
                        # Getting max restriction
                        if element_splitted[4] == math.inf:
                            max_restriction = "Inf"
                        else:
                            max_restriction = element_splitted[4]
                        
                        edge = {'data': { 'source': node1_id, 
                                'target': node2_id, 'restrictions': [min_restriction,flow,max_restriction,cost], 
                                'id':edge_id, 'source_node':element_splitted[0], 
                                'target_node':element_splitted[1]},
                                'classes':'edge'}

                        new_edges.append(edge)
                        number_of_edges += 1

                        # Update the edge nodes degrees
                        nodes_degrees[element_splitted[0]]['positive_degree'] += 1
                        nodes_degrees[element_splitted[1]]['negative_degree'] += 1
                
                # Updating the graph elements
                graph_elements['nodes'] = new_nodes
                graph_elements['edges'] = new_edges

                # Creating the table
                nodes_degrees_table_children = []
                for node in nodes_degrees .items():   
                    nodes_degrees_table_children.append(html.Tr(
                        [
                            html.Td(node[0], style={"text-align":"center", "width":"16.6%"}), 
                            html.Td(node[1]['positive_degree'],  style={"text-align":"center", "width":"16.6%"}),
                            html.Td(node[1]['negative_degree'],  style={"text-align":"center", "width":"16.6%"}),
                            html.Td(node[1]['min_restriction'],  style={"text-align":"center", "width":"16.6%"}),
                            html.Td(node[1]['max_restriction'],  style={"text-align":"center", "width":"16.6%"}),
                            html.Td(node[1]['supply/demand'],  style={"text-align":"center", "width":"16.6%"}),
                        ], className="table-primary"))
            
            # Clean the upload content so we can upload a diferent file
            upload_graph_contents = ""

            print("READ GRAPH CASE")
            print("Nodes")
            for n in graph_elements['nodes']:
                print(n)
            print("\n\nEdges")
            for e in graph_elements['edges']:
                print(e)
            print("------------------------------\n")

            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, None
        
        # ************** RUN ALGORITHMS LOGIC *******************
        elif btn_triggered == 'done-btn-select-source-and-sink-nodes-modal':
            
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)

            graph_elements_copy = copy.deepcopy(graph_elements)
            alert = None

            # Read sources and sinks nodes
            sources = []
            sinks = []
            for c in select_source_and_sink_nodes_modal_body_children:
                try:
                    node = c['props']['children'][0]['props']['value']
                    node_type = c['props']['children'][2]['props']['value']
                    if node_type == "source":
                        sources.append(node)
                    elif node_type == "sink":
                        sinks.append(node)
                except:
                    continue
            
            # Getting target flow
            target_flow = None
            try:
                target_flow = select_source_and_sink_nodes_modal_body_children[-1]['props']['children'][1]['props']['value']
                # If it exists, validate if it is a positive number less than infinity
                target_flow = float(target_flow)
                if target_flow < 0 or target_flow == math.inf:
                    raise Exception()
            except:
                target_flow = None
            
            # Alert if there are not sources or sinks
            if (not sources or not sinks) and select_algorithm_dropdown != "Find total minimum-cost flow using Simplex algorithm":
                # Incorrect number of sources or sinks
                alert = 16

            # Alert if target flow is needed and it is incorrect or unexistent
            if (target_flow == None and select_algorithm_dropdown != "Find maximum flow using Ford-Fulkerson algorithm"
                and select_algorithm_dropdown != "Find total minimum-cost flow using Simplex algorithm"):
                # Target flow is needed 
                alert = 17
                
            if not alert:    
                result_div_style = {'display':''}
                # Creat a red object
                g = Red()
                # Adding all nodes
                for node in graph_elements['nodes']:
                    g.agregar_nodo(node['data']['label'],node['data']['min_restriction'],node['data']['max_restriction'],node['data']['supply/demand'])
                # Adding all edges
                for edge in graph_elements['edges']:
                    g.agregar_arco(edge['data']['source_node'], edge['data']['target_node'],
                                   edge['data']['restrictions'][0],edge['data']['restrictions'][1],
                                   edge['data']['restrictions'][2], edge['data']['restrictions'][3],
                                   edge['data']['id'])
                
                # ----- ALGORITHM TO RUN -----
                # Ford-Fulkerson
                if select_algorithm_dropdown == "Find maximum flow using Ford-Fulkerson algorithm":
                    # Getting result
                    max_flow = g.flujo_maximo(sources, sinks)
                    edges = g.arcos()
                    print(type(max_flow))
                    
                    if max_flow:
                        # Updating edges flows
                        for edge in edges:
                            for e in graph_elements['edges']:
                                if edge.Id == e['data']['id']:
                                    if edge.flujo == math.inf:
                                        e['data']['restrictions'][1] = "Inf"
                                    else:
                                        e['data']['restrictions'][1] = edge.flujo
                                    break
                        
                        # Coloring sources (red) and sinks (blue) nodes
                        updated_nodes = 0
                        nodes_to_update = len(sources) + len(sinks)
                        for node in sources + sinks:
                            if updated_nodes == nodes_to_update:
                                break
                            for n in graph_elements['nodes']:
                                if node == n['data']['label']:
                                    if node in sources:
                                        n['classes'] = 'red_nodes'
                                    else:
                                        n['classes'] = 'blue_nodes'
                                    updated_nodes += 1
                                    break


                        txt = f"Maximum flow of {max_flow} units has beeen found from "
                        if len(sources) == 1:
                            txt += f"source {[s for s in sources]} to "
                        else:
                            txt += f"sources {[s for s in sources]} to "
                        
                        if len(sinks) == 1:
                            txt += f"sink {[s for s in sinks]}"
                        else:
                            txt += f"sinks {[s for s in sinks]}"
                        result_text_children = html.P([txt])
                    elif max_flow == 0:
                        txt = f"Current restrictions could not be satisfied. The problem has no solution."
                        result_text_children = html.P([txt])
                
                elif select_algorithm_dropdown == "Find minimum-cost flow using Primal algorithm":
                    # Getting the cost
                    cost = g.algoritmo_primal(sources, sinks, target_flow)

                    # If not cost, do nothing but write the result
                    if not cost:
                        txt = f"Target flow of {target_flow} units could not be reached due current restrictions. The problem has no solution."
                    # If there are cost, show the final flow distribution
                    else:
                        # Updating edges flows
                        edges = g.arcos()
                        for edge in edges:
                            for e in graph_elements['edges']:
                                if edge.Id == e['data']['id']:
                                    if edge.flujo == math.inf:
                                        e['data']['restrictions'][1] = "Inf"
                                    else:
                                        e['data']['restrictions'][1] = edge.flujo
                                    break

                        # Coloring sources (red) and sinks (blue) nodes
                        updated_nodes = 0
                        nodes_to_update = len(sources) + len(sinks)
                        for node in sources + sinks:
                            if updated_nodes == nodes_to_update:
                                break
                            for n in graph_elements['nodes']:
                                if node == n['data']['label']:
                                    if node in sources:
                                        n['classes'] = 'red_nodes'
                                    else:
                                        n['classes'] = 'blue_nodes'
                                    updated_nodes += 1
                                    break
                        
                        # Written result
                        txt = f"Target flow of {target_flow} units have been reached with cost {cost} from "
                        if len(sources) == 1:
                            txt += f"source {[s for s in sources]} to "
                        else:
                            txt += f"sources {[s for s in sources]} to "
                        
                        if len(sinks) == 1:
                            txt += f"sink {[s for s in sinks]}"
                        else:
                            txt += f"sinks {[s for s in sinks]}"
                        
                    result_text_children = html.P([txt])
                
                elif select_algorithm_dropdown == "Find minimum-cost flow using Dual algorithm":
                    # Getting the cost
                    cost = g.algoritmo_dual(sources, sinks, target_flow)

                    # If not cost, do nothing but write the result
                    if not cost:
                        txt = f"Target flow of {target_flow} units could not be reached due current restrictions. The problem has no solution."
                    # If there are cost, show the final flow distribution
                    else:
                        # Updating edges flows
                        edges = g.arcos()
                        for edge in edges:
                            for e in graph_elements['edges']:
                                if edge.Id == e['data']['id']:
                                    if edge.flujo == math.inf:
                                        e['data']['restrictions'][1] = "Inf"
                                    else:
                                        e['data']['restrictions'][1] = edge.flujo
                                    break

                        # Coloring sources (red) and sinks (blue) nodes
                        updated_nodes = 0
                        nodes_to_update = len(sources) + len(sinks)
                        for node in sources + sinks:
                            if updated_nodes == nodes_to_update:
                                break
                            for n in graph_elements['nodes']:
                                if node == n['data']['label']:
                                    if node in sources:
                                        n['classes'] = 'red_nodes'
                                    else:
                                        n['classes'] = 'blue_nodes'
                                    updated_nodes += 1
                                    break
                        
                        # Written result
                        txt = f"Target flow of {target_flow} units have been reached with cost {cost} from "
                        if len(sources) == 1:
                            txt += f"source {[s for s in sources]} to "
                        else:
                            txt += f"sources {[s for s in sources]} to "
                        
                        if len(sinks) == 1:
                            txt += f"sink {[s for s in sinks]}"
                        else:
                            txt += f"sinks {[s for s in sinks]}"
                        
                    result_text_children = html.P([txt])
                
                elif select_algorithm_dropdown == "Find total minimum-cost flow using Simplex algorithm":
                    print("SIMPLEEX")
                    # Getting the cost
                    cost = g.metodo_simplex()

                    # If not cost, do nothing but write the result
                    if not cost:
                        txt = f"The current restrictions could not be satisfied. The problem has no solution."
                    # If there are cost, show the final flow distribution
                    else:
                        # Updating edges flows
                        edges = g.arcos()
                        for edge in edges:
                            for e in graph_elements['edges']:
                                if edge.Id == e['data']['id']:
                                    if edge.flujo == math.inf:
                                        e['data']['restrictions'][1] = "Inf"
                                    else:
                                        e['data']['restrictions'][1] = edge.flujo
                                    break
                        
                        # Written result
                        txt = f"Minimum flow have been reached with cost {cost}"
                        
                    result_text_children = html.P([txt])

            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_elements_copy
        
        elif btn_triggered == "run-algorithm-btn-network":
            print("Algoritmo a correr:", select_algorithm_dropdown)
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None

            alert = None
            if select_algorithm_dropdown != "Find total minimum-cost flow using Simplex algorithm":
                if not selected_node_data:
                    alert = 15
            
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ----- Clear result case -----
        elif btn_triggered == 'clear-result-btn-network':
            alert = None
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            result_text_children = []
            result_div_style = {'display':'None'}

            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy

    else:
        return dash.no_update


# ----- Callback to manage "Edit nodes" modal -----
@app.callback(
    [Output("edit-nodes-modal-network", "is_open"), Output("edit-nodes-modal-body-network", "children")],
    [Input("edit-nodes-btn-network", "n_clicks"), Input("cancel-btn-edit-nodes-modal-network", "n_clicks"), 
     Input('done-btn-edit-nodes-modal-network', 'n_clicks')],
    [State("network", "selectedNodeData"), State("edit-nodes-modal-network", "is_open")]
)
def toggleModal(edit_nodes_btn, cancel_btn_edit_nodes_modal, done_btn_edit_nodes_modal, 
    selected_node_data, is_modal_open):
    if edit_nodes_btn:
        if not selected_node_data:
            return False, []
        else:
            node_forms = []
            for node in selected_node_data:
                node_label = node['label']
                node_forms.append(html.H3(f"Node {node_label}"))
                node_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Current label: ", style={"padding":"1em"}),
                                    dbc.Label(node_label),
                                    dbc.Label("New label: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                    
                                    
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                   
                                    dbc.Label("Current Min. Restriction: ", style={"padding":"1em"}),
                                    dbc.Label(node['min_restriction']),
                                    dbc.Label("New Min. Restriction: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),

                                ]
                            ),

                            dbc.FormGroup(
                                [
                             
                                    dbc.Label("Current Max. Restriction: ", style={"padding":"1em"}),
                                    dbc.Label(node['max_restriction']),
                                    dbc.Label("New Max Restriction: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ]
                            ),

                            dbc.FormGroup(
                                [
                             
                                    dbc.Label("Current Supply/Demand: ", style={"padding":"1em"}),
                                    dbc.Label(node['supply/demand']),
                                    dbc.Label("New Supply/Demand: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text")
                                ]
                            ),
                            
                        ], inline=True
                    )
                )

            return not is_modal_open, node_forms
    return is_modal_open, []

# ----- Callback to manage "Edit edge" modal -----
@app.callback(
    [Output("edit-edges-modal-network", "is_open"), Output("edit-edges-modal-body-network", "children")],
    [Input("edit-edges-btn-network", "n_clicks"), Input("cancel-btn-edit-edges-modal-network", "n_clicks"), 
     Input('done-btn-edit-edges-modal-network', 'n_clicks')],
    [State("network", "selectedEdgeData"), State("edit-edges-modal-network", "is_open")]
)
def toggleModal(edit_edges_btn, cancel_btn_edit_edges_modal, done_btn_edit_edges_modal, 
    selected_edge_data, is_modal_open):
    if edit_edges_btn:
        if not selected_edge_data:
            return False, []
        else:
            edges_forms = []
            for edge in selected_edge_data:
                node1 = edge['source_node']
                node2 = edge['target_node']
                if node1 != node2:
                    radioButton = dbc.RadioButton()
                    label_change_direction = dbc.Label(f"Change direction", style={"padding":"1em"})
                else:
                    radioButton = None
                    label_change_direction = None

                
                edges_forms.append(dbc.FormGroup([
                                                    html.H3(f"Edge({node1},{node2})"),
                                                    radioButton,
                                                    label_change_direction                
                                                ], style={"padding-left":"1em"})
                                    )

                edges_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Input(type="hidden", value=[edge['id'], node1, node2]),
                                    dbc.Label("Current Min. Restriction: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][0]),
                                    dbc.Label("New Min. Restriction: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Current Flow: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][1]),
                                    dbc.Label("New Flow: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Current Capacity: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][2]),
                                    dbc.Label("New Capacity: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("Current Cost: ", style={"padding":"1em"}),
                                    dbc.Label(edge['restrictions'][3]),
                                    dbc.Label("New Cost: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text"),
                                ]
                            ),

                            
                        ],
                        inline=True
                    )
                )
            
            return not is_modal_open, edges_forms

    return is_modal_open, []

# ----- Callback to manage "Select Source And Sink Nodes" modal -----
@app.callback(
    [Output("select-source-and-sink-nodes-modal", "is_open"), Output("select-source-and-sink-nodes-modal-body", "children")],
    [Input("run-algorithm-btn-network", "n_clicks"), Input("cancel-btn-select-source-and-sink-nodes-modal", "n_clicks"), 
     Input("done-btn-select-source-and-sink-nodes-modal", 'n_clicks')],
    [State("network", "selectedNodeData"), State("select-source-and-sink-nodes-modal", "is_open"),
     State('select-algorithm-dropown-network', 'value')]
)
def toggleModal(run_algorithm_btn, cancel_btn_select_source_and_sink_nodes_modal, 
                done_btn_select_source_and_sink_nodes_modal, selected_node_data, is_modal_open,
                select_algorithm_dropdown):
    if run_algorithm_btn:
        if not selected_node_data and select_algorithm_dropdown != "Find total minimum-cost flow using Simplex algorithm":
            return False, []
        else:
            node_forms = []
            if select_algorithm_dropdown != "Find total minimum-cost flow using Simplex algorithm":
                for node in selected_node_data:
                    node_forms.append(
                        dbc.FormGroup([
                            dbc.Input(type="hidden", value=node['label']),
                            html.H3(f"Node {node['label']}"),
                            dcc.RadioItems(
                                options=[
                                    {'label':'Source', 'value':'source'},
                                    {'label':'Sink', 'value':'sink'}
                                ],labelStyle={'display':'inline-block', "padding-left":"1em"}
                            )                
                        ], style={"padding-left":"1em"})
                    )
                
                if select_algorithm_dropdown != "Find maximum flow using Ford-Fulkerson algorithm":
                    node_forms.append(
                        dbc.Form(
                            [
                                html.H6("Target Flow: ", className="mr-2", style={"padding":"2em"}),
                                dbc.Input(type="text"),
                                
                                
                            ], inline=True
                        )

                    )
            else:
                node_forms.append(html.H5('No sink or sources needed to run this algorithm.'))
                
            return not is_modal_open, node_forms
    return is_modal_open, []


# ----- Chained callback to display an alert if it is necesary
@app.callback(
    [Output('alert-network', "children"), Output('alert-network', "is_open")],
    Input('alert-info-network', 'data')
)
def manageAlert(alert_info):
    print(alert_info)
    text = ""
    show = False
    if alert_info == 1:
        text = "No node selected to edit. Please, select at least one node and try again"
        show = True
    elif alert_info == 2:
        text = "No node selected to remove. Please, select at least one node and try again"
        show = True
    elif alert_info == 3:
        text = "No nodes selected to add an edge. Please, select one or two nodes and try again"
        show = True
    elif alert_info == 4:
        text = "More than two nodes selected to add an edge. Please, select one or two nodes and try again"
        show = True
    elif alert_info == 5:
        text = "No edge selected to edit. Please, select at least one edge and try again"
        show = True
    elif alert_info == 6:
        text = "No edge selected to remove. Please, select at least one edge and try again"
        show = True
    elif alert_info == 7:
        text = "Error. Invalid file format. Please, check it and try again"
        show = True
    elif alert_info == 8:
        text = "Error. Some restrictions are not numbers, or negative numbers. Please, check it and try again"
        show = True
    elif alert_info == 9:
        text = "Error. Inconsistency in some node restrictions. Please, check it and try again"
        show = True
    elif alert_info == 10:
        text = "Error. Inconsistency in some edge restrictions. Please, check it and try again"
        show = True
    elif alert_info == 11:
        text = "Error. There are some different nodes with same label. Please, check it and try again"
        show = True
    elif alert_info == 12:
        text = "Error. There are some edge from/to nonexistent node. Please, check it and try again"
        show = True
    elif alert_info == 13:
        text = "Error. There are some edge with invalid cost (infinite or not a number). Please, check it and try again"
        show = True
    elif alert_info == 14:
        text = "Error. No transport network. Please, create or upload a transport network and try again"
        show = True
    elif alert_info == 15:
        text = "No nodes selected to choose sources and sinks. Please, select at least two different nodes and try again"
        show = True
    elif alert_info == 16:
        text = "Error. Sources or sinks nodes not encountered. Please, select at least one source node and one sink node and try again"
        show = True
    elif alert_info == 17:
        text = "Error. Incorrect target flow. Please, check it and try again"
        show = True
    return text, show
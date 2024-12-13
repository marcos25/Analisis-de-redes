import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import pandas as pd  # pip install pandas
import plotly.express as px
import random
from grafica import *
import base64
import digraph
import uuid

from main import app


# ----- Dropdown menu for data structure selection -----
data_structures = ['Graph', "Directed Graph"]
select_data_structure_dropdown = dcc.Dropdown(
    id='select-data-structure-dropdown',
    value='Graph',
    clearable=False,
    options=[ {'label': name.capitalize(), 'value': name} for name in data_structures],
    style={"width":"14em"}
)
# -------------------------------------------------------

# ----- Dropdown menu for algorithm selection -----
algorithms = ['Check if the graph is bipartite', 'Search for Euler walks', 
              'Search for a spanning tree by Breadth First Search', 
              'Search for a spanning tree by Depth First Search', 
              "Search for a minimum spanning tree using Kruskal's algorithm",
              "Search for a minimum spanning tree using Prim's algorithm"]
select_algorithm_dropdown = dcc.Dropdown(
    id='select-algorithm-dropown',
    value='Check if the graph is bipartite',
    clearable=False,
    options=[ {'label': name, 'value': name} for name in algorithms],
    style={"width":"32em"}
)
# -------------------------------------------------------
default_stylesheet =[{
                        'selector': '.edge',
                        'style':{
                            'curve-style': 'bezier',
                            'label': 'data(weight)',
                        }
                    },

                    {
                        'selector': '.red_edges',
                        'style':{
                            'curve-style': 'bezier',
                            'label': 'data(weight)',
                            'line-color': '#FF8080'
                        }
                    },

                    {
                        'selector': '.blue_edges',
                        'style':{
                            'curve-style': 'bezier',
                            'label': 'data(weight)',
                            'line-color': '#80B7FF'
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
            id='graph',
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
                   id="edit-nodes-modal-body"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-nodes-modal", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-nodes-modal", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-nodes-modal",
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
                   id="edit-edges-modal-body"
                ),
                dbc.ModalFooter(
                    html.Div(
                        [
                            dbc.Button("Done", id="done-btn-edit-edges-modal", color="primary", 
                                    style={'margin':"1em"},), 
                            dbc.Button("Cancel", id="cancel-btn-edit-edges-modal", className="ml-auto")
                        ]
                    )
                )
            ],
            id="edit-edges-modal",
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
        id='nodes-info', data=[['a', 1]] # The first element is the first node name that we will use
    ),
    dcc.Store(
        id='graph-copy', data=None
    ),
    

    # 1- No nodes selected when edit node button is clicked
    # 2- No nodes selected when remove node button is clicked
    # 3- No nodes selected when add edge button is clicked
    # 4- More than two nodes selected when add edge button is clicked
    dcc.Store(
        id='alert-info', data=None
    ),

    # ----- Div to display nodes errors -----
    html.Div(id="edit-nodes-alert", children=[]),

    edit_nodes_modal,
    
    edit_edges_modal,

    dbc.Row([
        # Left column
        dbc.Col([
            html.Div([
                dbc.Alert(id="alert", is_open=False, dismissable=True, color="warning"),
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
                        dbc.Button("Add", id="add-node-btn", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-nodes-btn", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-nodes-btn", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),

                dbc.Col([
                    html.Div([
                        html.H5("Edges", className="text-muted"),   
                        dbc.Button("Add", id="add-edge-btn", className="mr-1", color="primary"),
                        dbc.Button("Edit", id="edit-edges-btn", className="mr-1", color="primary"),
                        dbc.Button("Remove", id="remove-edges-btn", className="mr-1", color="primary"),
                    ], className="col-xs-1 text-center"),
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),
            
            dbc.Row([
                dcc.Upload([
                    dbc.Button("Upload graph from file", className="mr-1", color="success"),
                ], id="upload-graph-obj")
                
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
                            dbc.Button("Run", id="run-algorithm-btn",size="sm", className="btn btn-warning mr-1"),
                            dbc.Button("Clear", id="clear-result-btn",size="sm", className="btn btn-success mr-1"),
                        ], style={"padding":"1em"}),
                        
                    ])
                ]), 
            ]),

            html.Br(),


            html.Div([
                    html.H4('Result'),
                    html.P(id="result-text")
            ], id="result-div", style={'display':'None'}),

            html.Br(),
            html.Br(),
            html.Br(),

            html.Div([
                html.H4('Graph Information'),

                html.Table([

                    html.Tr([
                        html.Td([
                            html.Label("Number of nodes:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-nodes-label", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ]),
                    html.Tr([
                        html.Td([
                            html.Label("Number of edges:")
                        ]),
                        html.Td([
                            dbc.Label(0, id="number-of-edges-label", color="primary")
                        ], style={"padding":"1em"}),
                        
                    ])
                ]),
            ]),

            html.Br(),
            html.Br(),
            html.Br(),

            dbc.Row([
                html.H4("Nodes Degrees"),
            ], justify="center"),

            html.Div([
                dbc.Table([
                
                    # Head of the table
                    html.Thead([
                        html.Tr([
                            html.Th([
                                html.H5("Node", className="text-muted"),   
                            ], style={"text-align":"center"}),

                            html.Th([
                                html.H5("Degree", className="text-muted"),   
                            ], style={"text-align":"center"})
                        ])
                    ]),
                        
                ], className="table table-bordered table-striped", bordered=True, responsive=True),
                

            ], style={"width":"100%"}),

            
            html.Div([
                dbc.Table([
                    # Body of the table
                    html.Tbody(id="nodes-degrees-table", children=[])
                ],bordered=False, responsive=False),
                

            ], style={"position":"relative", "height":"200px", "overflow":"auto", "display":"block", "justify":"center"}),
            
        ], md=6)

    ]),    
])

# ----- Callback to update the graph -----
@app.callback(
    [Output("graph", "elements"), Output("nodes-degrees-table", "children"), 
     Output("number-of-nodes-label", "children"), Output("alert-info", "data"), 
     Output("number-of-edges-label", "children"), Output('nodes-info', 'data'), 
     Output('upload-graph-obj', 'contents'), 
     Output('result-text', 'children'), Output('result-div', 'style'),
     Output('graph-copy', 'data')],

    [Input("add-node-btn", "n_clicks"), Input("done-btn-edit-nodes-modal", "n_clicks"),
     Input("remove-nodes-btn", "n_clicks"), Input("edit-nodes-btn", "n_clicks"),
     Input("add-edge-btn", "n_clicks"), Input("done-btn-edit-edges-modal", "n_clicks"),
     Input("edit-edges-btn", "n_clicks"), Input('remove-edges-btn', 'n_clicks'), 
     Input('upload-graph-obj', 'contents'), Input('run-algorithm-btn', 'n_clicks'),
     Input('clear-result-btn', 'n_clicks')],
    
    [State("graph", "elements"), State("nodes-degrees-table", "children"), 
     State("number-of-nodes-label", "children"), State("edit-nodes-modal-body", "children"), 
     State("graph", "selectedNodeData"), State("number-of-edges-label", "children"), 
     State("edit-edges-modal-body", "children"), State("graph", "selectedEdgeData"), 
     State('nodes-info', 'data'), State('select-algorithm-dropown', 'value'),
     State('result-text', 'children'), State('result-div', 'style'), State('graph-copy', 'data')]
)
def updateGraph(add_node_btn_n_clicks, done_btn_edit_nodes_modal, remove_nodes_btn, edit_nodes_btn,
    add_edge_btn, done_btn_edit_edges_modal, edit_edges_btn, remove_edges_btn, upload_graph_contents,
    run_algorithm_btn, clear_result_btn, graph_elements, nodes_degrees_table_children, number_of_nodes, 
    edit_nodes_modal_body_childrens, selected_node_data, number_of_edges, edit_edges_modal_body_childrens, 
    selected_edge_data, nodes_info, select_algorithm_dropdown, 
    result_text_children, result_div_style, graph_copy):
    # Getting the callback context to know which input triggered this callback
    ctx = dash.callback_context

    if ctx.triggered:
        # Getting the id of the object which triggered the callback
        btn_triggered = ctx.triggered[0]['prop_id'].split('.')[0]

        # ----- Add node case -----
        if btn_triggered == "add-node-btn":
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
            node = {'data': {'id': node_id, 'label': node_name},
                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                    'classes':'node'}
            
            graph_elements['nodes'].append(node)

            # Adding the node to the node_degrees_table
            nodes_degrees_table_children.append(html.Tr([
                html.Td(node_name, style={"text-align":"center"}), 
                html.Td(0,  style={"text-align":"center"})
                ], className="table-primary"))

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
        elif btn_triggered == "done-btn-edit-nodes-modal":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            for children in edit_nodes_modal_body_childrens:
                # Getting the new label
                try:
                    new_label = children['props']['children'][1]['props']['children'][1]['props']['value']
                except:
                    continue
                
                # Getting the current label
                current_label = children['props']['children'][0]['props']['children'][1]['props']['children']

                # Do nothing if new label == current label
                if new_label == current_label:
                    continue

                # Checking if the new label is repeated or not
                repeated_label = False
                for node in graph_elements['nodes']:
                    if node['data']['label'] == new_label:
                        repeated_label = True
                        break
                if repeated_label:
                    continue
                
                # Editing the node in graph_elements
                for node in graph_elements['nodes']:
                    if node['data']['label'] == current_label:
                        node['data']['label'] = new_label
                        break
                
                # Editing edges in graph_elements and edges_info
                for edge in graph_elements['edges']:
                    new_source_label = None
                    new_target_label = None
                    # Editing edges elements
                    if edge['data']['source_node'] == current_label:
                        edge['data']['source_node'] = new_label
                        
                    if edge['data']['target_node'] == current_label:
                        edge['data']['target_node'] = new_label

                
                # Editing the nodes in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == current_label:
                        children['props']['children'][0]['props']['children'] = new_label
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
        elif btn_triggered == "edit-nodes-btn":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            if not selected_node_data:
                alert = 1
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy

        # ----- Remove nodes case ------
        elif btn_triggered == "remove-nodes-btn":
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
                degrees = {c['props']['children'][0]['props']['children']:0 for c in nodes_degrees_table_children}

                for edge in graph_elements['edges']:
                    degrees[edge['data']['source_node']] += 1
                    degrees[edge['data']['target_node']] += 1

                for c in nodes_degrees_table_children:
                    node_name = c['props']['children'][0]['props']['children'] 
                    c['props']['children'][1]['props']['children'] = str(degrees[node_name])

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
        elif btn_triggered == "add-edge-btn":
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

                loop = {'data': {'source': node, 
                            'target': node, 'weight': "0", 'id':loop_id, 'source_node':node_label, 'target_node':node_label},
                        'classes':'edge'}
                graph_elements['edges'].append(loop)

                # Updating the node degree in the nodes degrees table
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == node_label:
                        current_degree = int(children['props']['children'][1]['props']['children'])
                        children['props']['children'][1]['props']['children'] = str(current_degree + 2)
                        break

                number_of_edges += 1
            # When exactly two nodes are selected (edge)
            elif len(selected_node_data) == 2:
                node1 = selected_node_data[0]['id']
                node2 = selected_node_data[1]['id']

                node1_label = selected_node_data[0]['label']
                node2_label = selected_node_data[1]['label']

                edge_id = str(uuid.uuid1())
                edge = {'data': { 'source': node1, 
                                'target': node2, 'weight': "0", 'id':edge_id, 'source_node':node1_label, 'target_node':node2_label},
                        'classes':'edge'}
                graph_elements['edges'].append(edge)

                # Updating the node degree in the nodes degrees table
                n_edited_nodes = 0
                for children in nodes_degrees_table_children:
                    if children['props']['children'][0]['props']['children'] == node1_label or children['props']['children'][0]['props']['children'] == node2_label:
                        current_degree = int(children['props']['children'][1]['props']['children'])
                        children['props']['children'][1]['props']['children'] = str(current_degree + 1)
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
        elif btn_triggered == "done-btn-edit-edges-modal":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            for c in edit_edges_modal_body_childrens:
                # Getting the info of the edges
                # First node
                node1 = c['props']['children'][0]['props']['children'][1]['props']['children'][:-1]
                # Second node
                node2 = c['props']['children'][0]['props']['children'][2]['props']['children'][:-1]
                # Edge id
                edge_id = c['props']['children'][0]['props']['children'][3]['props']['value']

                # Trying to get a new weight and validate if it is a number
                try:
                    new_weight = c['props']['children'][1]['props']['children'][1]['props']['value']
                    float(new_weight)
                except:
                    continue

                # If everything goes correctly, then proceed to update the edges
                
                # Update the edge in graph elements:
                for edge in graph_elements['edges']:
                    if edge['data']['id'] == edge_id:
                        edge['data']['weight'] = new_weight


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
        elif btn_triggered == "edit-edges-btn":
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)
                graph_copy = None
            alert = None
            if not selected_edge_data:
                alert = 5
            
            
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_copy
        
        # ----- Remove edges case -----
        elif btn_triggered == "remove-edges-btn":
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
                degrees = {c['props']['children'][0]['props']['children']: int(c['props']['children'][1]['props']['children']) for c in nodes_degrees_table_children}

                for edge in selected_edge_data:
                    degrees[edge['source_node']] -= 1
                    degrees[edge['target_node']] -= 1

                for c in nodes_degrees_table_children:
                    node_name = c['props']['children'][0]['props']['children'] 
                    c['props']['children'][1]['props']['children'] = str(degrees[node_name])
            
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
        elif btn_triggered == 'upload-graph-obj':
            # Read the file and convert it to list of elements
            content_type, content_string = upload_graph_contents.split(',')
            graph = [x.replace(" ", "").split(",") for x in base64.b64decode(content_string).decode('ascii').strip().split("\n") if x] 
            print(graph)

            alert = None
            # Validate the data format
            for element in graph:
                # Just accept edges (a,b) or single nodes (a)
                if len(element) > 3:
                    alert = 7
                    break
                # validate if  weight is a number in case the element is an edge
                if len(element) == 3:
                    try:
                        float(element[2])
                    except:
                        alert = 7
                        break

            
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
                    # When it's a single node
                    if len(element_splitted) == 1:
                        # Check if node name is already in use
                        for node in new_nodes:
                            if element_splitted[0] == node['data']['label']:
                                continue
                        
                        # If node doesn't exist, then add it to the new nodes
                        node = {'data': {'id': str(uuid.uuid1()), 'label': element_splitted[0]},
                                         'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                                         'classes':'node'}
                        new_nodes.append(node)

                        # Adding the node to the degrees dict
                        nodes_degrees[element_splitted[0]] = 0
                        number_of_nodes += 1

                    # When it's an edge
                    else:
                        # To store nodes ids
                        node1_id = None
                        node2_id = None

                        # Check if node1 name is already in use
                        node_already_exists = False
                        for node in new_nodes:
                            if node['data']['label'] == element_splitted[0]:
                                node_already_exists = True
                                node1_id = node['data']['id']
                                break
                        
                        # If node 1 doesn't exists, then add it to the new nodes
                        if not node_already_exists:
                            node1_id = str(uuid.uuid1())
                            node = {'data': {'id': node1_id, 'label': element_splitted[0]},
                                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                                    'classes':'node'}
                            new_nodes.append(node)
                            number_of_nodes += 1

                            # Adding it to the degrees dict
                            nodes_degrees[element_splitted[0]] = 0
                        
                        # Check if node2 name is already in use
                        node_already_exists = False
                        for node in new_nodes:
                            if node['data']['label'] == element_splitted[1]:
                                node_already_exists = True
                                node2_id = node['data']['id']
                                break
                        
                        # If node 1 doesn't exists, then add it to the new nodes
                        if not node_already_exists:
                            node2_id = str(uuid.uuid1())
                            node = {'data': {'id': node2_id, 'label': element_splitted[1]},
                                    'position': {'x':random.uniform(0,500),'y':random.uniform(0,500)},
                                    'classes':'node'}
                            new_nodes.append(node)
                            number_of_nodes += 1

                            # Adding it to the degrees dict
                            nodes_degrees[element_splitted[1]] = 0
                        
                        # After nodes managing, add the edge between them
                        edge_id = str(uuid.uuid1())
                        try:
                            weight = element_splitted[2]
                        except:
                            weight = 0

                        edge = {'data': { 'source': node1_id, 
                                'target': node2_id, 'weight': weight, 'id':edge_id, 
                                'source_node':element_splitted[0], 'target_node':element_splitted[1]},
                                'classes':'edge'}
                        new_edges.append(edge)
                        number_of_edges += 1

                        # Update the edge nodes degrees
                        nodes_degrees[element_splitted[0]] += 1
                        nodes_degrees[element_splitted[1]] += 1
                
                # Updating the graph elements
                graph_elements['nodes'] = new_nodes
                graph_elements['edges'] = new_edges

                # Creating the table
                nodes_degrees_table_children = []
                for node in nodes_degrees .items():   
                    nodes_degrees_table_children.append(html.Tr(
                        [
                            html.Td(node[0], style={"text-align":"center"}), 
                            html.Td(node[1],  style={"text-align":"center"})
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
        elif btn_triggered == 'run-algorithm-btn':
            if graph_copy:
                graph_elements = copy.deepcopy(graph_copy)

            graph_elements_copy = copy.deepcopy(graph_elements)
            alert = None
            if len(graph_elements['nodes']) == 0 and len(graph_elements['edges']) == 0:
                alert = 8

            if not alert:    
                result_div_style = {'display':''}

                # Creat a Grafica object
                g = Grafica()
                # Adding all nodes
                for node in graph_elements['nodes']:
                    g.agregar_nodo(node['data']['label'])
                # Adding all edges
                for edge in graph_elements['edges']:
                    g.agregar_arista(edge['data']['source_node'], edge['data']['target_node'],
                                    edge['data']['id'], edge['data']['weight'])
                
                # ----- ALGORITHM TO RUN -----
                # Check if the graph is bipartite
                if select_algorithm_dropdown == "Check if the graph is bipartite":
                    
                    # Getting the partitions
                    partition1, partition2 = None, None
                    partition1, partition2 = g.es_bipartita()
                    
                    # Result text to display
                    result_text_children = None
                    

                    if partition1 == -1:
                        result_text_children = html.P("Graph is disconnected. No partitions found.")
                    elif partition1 == None:
                        result_text_children = html.P("No partitions found. Graph is not bipartite.")
                    else:

                        partition1 = [n.nombre for n in partition1]
                        partition2 = [n.nombre for n in partition2]

                        # Adding a class color to the nodes of each partition
                        for node in graph_elements['nodes']:
                            if node['data']['label'] in partition1:
                                node['classes'] = 'red_nodes'
                            elif node['data']['label'] in partition2:
                                node['classes'] = 'blue_nodes'
                        
                        txt = "Graph is bipartite. Following partitions were found:"
                        result_text_children = html.P([txt, html.Br(), f"Partition 1: {partition1}",
                                                       html.Br(), f"Partition 2: {partition2}"])
                
                # Find Eulerian Paths
                elif select_algorithm_dropdown == 'Search for Euler walks':
                    # Running algorithm
                    eulerian_walk = g.paseo_euler()

                    if eulerian_walk == False:
                        result_text_children = html.P("No Eulerian walk found.")
                    elif eulerian_walk == -1:
                            result_text_children = html.P("Graph is disconnected. No Eulerian walk found.")

                    else:
                        # To avoid problems with edges labels, we do all weights == -1
                        for e in graph_elements['edges']:
                            e['data']['weight'] = -1

                        # Labeling the edges according to their order in eulerian walk
                        for i in range(len(eulerian_walk) - 1):
                            node1 = eulerian_walk[i]
                            node2 = eulerian_walk[i+1]
                            for e in graph_elements['edges']:
                                if (((e['data']['source_node'] == node1 and e['data']['target_node'] == node2) or
                                   (e['data']['source_node'] == node2 and e['data']['target_node'] == node1)) and
                                   e['data']['weight'] == -1):
                                   e['data']['weight'] = i+1
                                   break
                        
                        # Coloring the first and last node of the path
                        # Case when it's a circuid
                        if eulerian_walk[0] == eulerian_walk[-1]:
                            txt = "The following Euler Circuit has been found:"
                            for n in graph_elements['nodes']:
                                if n['data']['label'] == eulerian_walk[0]:
                                    n['classes'] = 'red_nodes'
                                    break
                        # Case when it isn't a circuit
                        else:
                            txt = "The following Euler Path has been found:"
                            colored_nodes = 0
                            for n in graph_elements['nodes']:
                                if colored_nodes == 2:
                                    break
                                if n['data']['label'] == eulerian_walk[0]:
                                    n['classes'] = 'red_nodes'
                                    colored_nodes += 1
                                    continue
                                if n['data']['label'] == eulerian_walk[-1]:
                                    n['classes'] = 'blue_nodes'
                                    colored_nodes += 1
                                    continue
                        # Creating the result string
                        result_text_children = html.P([txt, html.Br(), f"{eulerian_walk}"])
                
                # Spanning tree with BFS
                elif select_algorithm_dropdown == 'Search for a spanning tree by Breadth First Search':
                    # Running algorithm
                    spanning_forest = g.busqueda_a_lo_ancho()

                    # Checking if result is a forest or single tree
                    if len(spanning_forest) == 1:
                        result_text_children = html.P("A single spanning tree has been found.")
                    else:
                        result_text_children = html.P(f"A spanning forest with {len(spanning_forest)} spanning trees has been found.")
                    
                    # Check every single tree in the fores
                    for tree in spanning_forest:
                        # Check if it is an empty tree (just one node) and coloring it with blue
                        if len(tree) == 1 and type(tree[0]) == Nodo:
                            for n in graph_elements['nodes']:
                                if n['data']['label'] == tree[0].nombre:
                                    n['classes'] = 'blue_nodes'
                                    break
                        else:
                            for edge in tree:
                                for e in graph_elements['edges']:
                                    if e['data']['id'] == edge.Id:
                                        e['classes'] = 'red_edges'
                                        break
                
                # Spanning tree with DFS
                elif select_algorithm_dropdown == 'Search for a spanning tree by Depth First Search':
                    # Running algorithm
                    spanning_forest = g.busqueda_a_profundidad()

                    # Checking if result is a forest or single tree
                    if len(spanning_forest) == 1:
                        result_text_children = html.P("A single spanning tree has been found.")
                    else:
                        result_text_children = html.P(f"A spanning forest with {len(spanning_forest)} spanning trees has been found.")
                    
                    # Check every single tree in the fores
                    for tree in spanning_forest:
                        # Check if it is an empty tree (just one node) and coloring it with blue
                        if len(tree) == 1 and type(tree[0]) == Nodo:
                            for n in graph_elements['nodes']:
                                if n['data']['label'] == tree[0].nombre:
                                    n['classes'] = 'blue_nodes'
                                    break
                        else:
                            for edge in tree:
                                for e in graph_elements['edges']:
                                    if e['data']['id'] == edge.Id:
                                        e['classes'] = 'red_edges'
                                        break
                
                elif select_algorithm_dropdown == "Search for a minimum spanning tree using Kruskal's algorithm":
                    # Running algorithm
                    spanning_forest = g.algoritmo_kruskal()
                    # Checking if result is a forest or single tree
                     
                    if g.es_conexa():
                        txt = "A minimum spanning tree with weight"
                    else:
                        txt ="A minimum spanning forest with weight"
                    
                    # Check every edge in spanning forest and getting the weight
                    weight = 0
                    for edge in spanning_forest:
                        # Check if it is an empty tree (just one node) and coloring it with blue
                        if type(edge) == Nodo:
                            for n in graph_elements['nodes']:
                                if n['data']['label'] == edge.nombre:
                                    n['classes'] = 'blue_nodes'
                                    break
                        else:
                            for e in graph_elements['edges']:
                                if e['data']['id'] == edge.Id:
                                    e['classes'] = 'red_edges'
                                    weight += float(e['data']['weight'])
                                    break
                    
                    txt += f" {weight} has been found."
                    result_text_children = html.P(txt)
                
                # PRIM'S ALGORITHM
                else:
                    # Running algorithm
                    spanning_forest = g.algoritmo_prim()

                    # Checking if result is a forest or single tree
                    if len(spanning_forest) == 1:
                        txt = "A minimum spanning tree with weight"
                    else:
                        txt = f"A minimum spanning forest with {len(spanning_forest)} spanning trees and weight"
                    
                    # Check every single tree in the fores
                    weight = 0
                    for tree in spanning_forest:
                        # Check if it is an empty tree (just one node) and coloring it with blue
                        if len(tree) == 1 and type(tree[0]) == Nodo:
                            for n in graph_elements['nodes']:
                                if n['data']['label'] == tree[0].nombre:
                                    n['classes'] = 'blue_nodes'
                                    break
                        else:
                            for edge in tree:
                                for e in graph_elements['edges']:
                                    if e['data']['id'] == edge.Id:
                                        e['classes'] = 'red_edges'
                                        weight += float(e['data']['weight'])
                                        break
                    
                    txt += f" {weight} has been found."
                    result_text_children = html.P(txt)
            
            return graph_elements, nodes_degrees_table_children, number_of_nodes, alert, number_of_edges, nodes_info, "",result_text_children, result_div_style, graph_elements_copy
        
        # ----- Clear result case -----
        elif btn_triggered == 'clear-result-btn':
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
    [Output("edit-nodes-modal", "is_open"), Output("edit-nodes-modal-body", "children")],
    [Input("edit-nodes-btn", "n_clicks"), Input("cancel-btn-edit-nodes-modal", "n_clicks"), 
     Input('done-btn-edit-nodes-modal', 'n_clicks')],
    [State("graph", "selectedNodeData"), State("edit-nodes-modal", "is_open")]
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
                node_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Current label: ", style={"padding":"1em"}),
                                    dbc.Label(node_label)
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("New label: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text", placeholder="Type the new label")
                                ],
                                className="mr-3"
                            )
                        ],
                        inline=True
                    )
                )

            return not is_modal_open, node_forms
    return is_modal_open, []

# ----- Callback to manage "Edit edge" modal -----
@app.callback(
    [Output("edit-edges-modal", "is_open"), Output("edit-edges-modal-body", "children")],
    [Input("edit-edges-btn", "n_clicks"), Input("cancel-btn-edit-edges-modal", "n_clicks"), 
     Input('done-btn-edit-edges-modal', 'n_clicks')],
    [State("graph", "selectedEdgeData"), State("edit-edges-modal", "is_open")]
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
                edges_forms.append(
                    dbc.Form(
                        [
                            dbc.FormGroup(
                                [
                                    dbc.Label("Edge ("),
                                    dbc.Label(f"{node1},"),
                                    dbc.Label(f"{node2})"),
                                    dbc.Input(type="hidden", value=edge['id']),
                                    dbc.Label("current weight: ", style={"padding":"1em"}),
                                    dbc.Label(edge['weight'])
                                ]
                            ),

                            dbc.FormGroup(
                                [
                                    dbc.Label("New weight: ", className="mr-2", style={"padding":"2em"}),
                                    dbc.Input(type="text", placeholder="Type the new weight")
                                ],
                                className="mr-3"
                            )
                        ],
                        inline=True
                    )
                )
            
            return not is_modal_open, edges_forms

    return is_modal_open, []

# ----- Chained callback to display an alert if it is necesary
@app.callback(
    [Output('alert', "children"), Output('alert', "is_open")],
    Input('alert-info', 'data')
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
        text = "Error. No graph. Please, create or upload a graph and try again"
        show = True
    return text, show
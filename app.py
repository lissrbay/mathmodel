import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import networkx as nx
import numpy as np
import pandas as pd


def generate_graph(n_vertices=20):
    G = nx.random_geometric_graph(n_vertices, 0.25)


    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text'
    )


    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: '+str(len(adjacencies[1])))

    #node_trace.marker.color = node_adjacencies
    node_trace.text = node_text


    fig = go.Figure(data=[edge_trace, node_trace])
    return fig


fig = generate_graph()
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='graph', figure=fig),
    dcc.Slider(
        id='slider',
        min=1,
        max=10,
        value=1,
        marks={str(step): str(step) for step in range(1, 11)},
        step=None
    ),
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])

graphs = [generate_graph(i) for i in range(1, 11)]

@app.callback(Output('graph', 'figure'),
                [Input('slider', 'value')],
              #[Input('submit-button-state', 'n_clicks')],
              [State('my-input', 'value')])
def update_output(step, input):
    return graphs[step-1]


app.run_server(debug=True, port=8080)
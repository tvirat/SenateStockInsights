"""The major vizualization components of our Project"""
from __future__ import annotations
import json
from plotly.graph_objs import Scatter, Figure
import plotly
import plotly.express as px
import pandas as pd
import networkx as nx
from Data_and_Functions import _StockVertex, Graph, get_no_trans

LINE_COLOUR = 'rgb(210,210,210)'
VERTEX_BORDER_COLOUR = 'rgb(50, 50, 50)'
LOW_COLOUR = 'rgb(89, 205, 105)'
MID_COLOUR = 'rgb(255, 255, 0)'
HIGH_COLOUR = 'rgb(255, 0 , 0)'
STOCK_COLOUR = 'rgb(0, 0, 139)'
USER_COLOUR = 'rgb(105, 89, 205)'

########################################################################################################
# Data
########################################################################################################

DFNAME = pd.read_csv('Senator Stock Trades updated.csv', encoding='ISO-8859-1')
DFNAME["Last_Name"] = DFNAME["Office_FilerType"].apply(lambda x: x.split(',')[0])
DFNAME["First_Name"] = DFNAME["Office_FilerType"].apply(lambda x: x.split(' ')[1])

########################################################################################################
# Graph vizualization tools
########################################################################################################


def setup_graph(graph: Graph,
                layout: str = 'spring_layout',
                max_vertices: int = 5000) -> list:
    """Use plotly and networkx to setup the visuals for the given graph.

    Optional arguments:
        - weighted: True when weight data should be visualized
    """

    graph_nx = graph.to_networkx(max_vertices)

    pos = getattr(nx, layout)(graph_nx)

    x_values = [pos[k][0] for k in graph_nx.nodes]
    y_values = [pos[k][1] for k in graph_nx.nodes]
    labels = list(graph_nx.nodes)
    weights = nx.get_edge_attributes(graph_nx, 'weight')
    colours = []
    sizes = []
    for node in graph_nx.nodes:
        sizes.append(5 + 2 * sum(1 / x for x in range(1, get_no_trans(graph_nx.nodes[node]['value']))))
        if isinstance(graph_nx.nodes[node]['value'], _StockVertex):
            colours.append(STOCK_COLOUR)
        else:
            if graph_nx.nodes[node]['value'].sus_type == "high":
                colours.append(HIGH_COLOUR)
            elif graph_nx.nodes[node]['value'].sus_type == "mid":
                colours.append(MID_COLOUR)
            else:
                colours.append(LOW_COLOUR)

    x_edges = []
    y_edges = []
    weight_positions = []

    for edge in graph_nx.edges:
        x1, x2 = pos[edge[0]][0], pos[edge[1]][0]
        x_edges += [x1, x2, None]
        y1, y2 = pos[edge[0]][1], pos[edge[1]][1]
        y_edges += [y1, y2, None]

        weight_positions.append(((x1 + x2) / 2, (y1 + y2) / 2, weights[(edge[0], edge[1])]))
    trace1 = Scatter(x=x_edges,
                     y=y_edges,
                     mode='lines+text',
                     name='edges',
                     line={"color": LINE_COLOUR, "width": 2},
                     )

    trace2 = Scatter(x=x_values,
                     y=y_values,
                     mode='markers',
                     name='nodes',
                     marker={"symbol": 'circle-dot', "size": sizes, "color": colours,
                             "line": {"color": VERTEX_BORDER_COLOUR, "width": 1}},
                     text=labels,
                     hovertemplate='%{text}',
                     hoverlabel={'namelength': 0}
                     )

    data = [trace1, trace2]

    return [weight_positions, data]


def visualize_graph(graph: Graph,
                    layout: str = 'spring_layout',
                    max_vertices: int = 5000,
                    output_file: str = '') -> None:
    """Use plotly and networkx to visualize the given weighted graph.

    Optional arguments:
        - layout: which graph layout algorithm to use
        - max_vertices: the maximum number of vertices that can appear in the graph
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
    """

    weight_positions, data = setup_graph(graph, layout, max_vertices)
    draw_graph(data, weight_positions, output_file)


def draw_graph(data: list, weight_positions: list, output_file: str = '') -> None:
    """
    Draw graph based on given data.

    Optional arguments:
        - output_file: a filename to save the plotly image to (rather than displaying
            in your web browser)
        - weight_positions: weights to draw on edges for a weighted graph
    """

    fig = Figure(data=data)
    fig.update_layout({'showlegend': False})
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)

    if weight_positions:
        for w in weight_positions:
            fig.add_annotation(
                x=w[0], y=w[1],  # Text annotation position
                xref="x", yref="y",  # Coordinate reference system
                text=w[2],  # Text content
                showarrow=False  # Hide arrow
            )
    if output_file == '':
        fig.show()
    else:
        fig.write_image(output_file)


##############################################################################################
# State Based Computations
##############################################################################################


def state_data(state_file: str, given_name: str, last_name: str) -> str:
    """
    Returns the state name of the senator with given given_name and last_name.

    >>> state_data('search.json', 'Thomas', 'Carper')
    'DE'

    """
    with open(state_file) as f:
        data = json.load(f)

        for lst in data:
            if lst['givenName'] == given_name and lst['familyName'] == last_name:
                for sublist in lst['congresses']:
                    if sublist['position'] == 'Senator':
                        state_name = sublist['stateName']
                        return state_name
        else:
            return ''


def state_data_all_senators(state_file: str) -> None:
    """
    Goes through all the senator data in data and adds a row to the data with each senator state.
    """
    DFNAME['Senator_State'] = DFNAME['First_Name']
    for i in range(len(DFNAME)):
        first_name = DFNAME['First_Name'].iloc[i]
        last_name = DFNAME['Last_Name'].iloc[i]
        DFNAME['Senator_State'].iloc[i] = state_data(state_file, first_name, last_name)


def visualize_states(number: int) -> plotly.graph_objects.Figure:
    """ Returns a Plotly graph to visualise the number of transcations by state.
    """
    number = min(number, len(DFNAME))
    fig = plotly.express.bar(DFNAME['Senator_State'].value_counts().head(number))
    fig.show()


def visualize_senators(number: int) -> plotly.graph_objects.Figure:
    """ Returns a Plotly graph to visualise the number of transcations by Senators.
    """
    number = min(number, len(DFNAME))
    fig = plotly.express.bar(DFNAME['Office_FilerType'].value_counts().head(number))
    fig.show()


def visualize_stocks(number: int) -> plotly.graph_objects.Figure:
    """ Returns a Plotly graph to visualise the n most transacted stocks.
    """
    number = min(number, len(DFNAME))
    fig = plotly.express.bar(DFNAME['Ticker'].value_counts().head(number))
    fig.show()

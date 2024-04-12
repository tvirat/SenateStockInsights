"""File containing all our data and functions for Project 2"""
from __future__ import annotations
import datetime
from typing import Any
import pandas as pd
import yfinance
import networkx as nx
from Variables import DICTOFSENS

########################################################################################################
# Data
########################################################################################################

DFNAME = pd.read_csv('Senator Stock Trades updated.csv', encoding='ISO-8859-1')
DFNAME["Last_Name"] = DFNAME["Office_FilerType"].apply(lambda x: x.split(',')[0])
DFNAME["First_Name"] = DFNAME["Office_FilerType"].apply(lambda x: x.split(' ')[1])

#################################################################################################################
# Dataclasses
################################################################################################################


class _Vertex:
    """
    This is the general class vertex which stores the functions executed by both the different kinds of vertices.

    Instance Attributes:
    - name: The name of the senator or the stock
    - neighbours: It is a dict mapping the item to its vertex object

    Representation Invariants:
    - name != ''
    - neighbours != {}
    """
    name: str
    neighbours: dict


class _SenatorVertex(_Vertex):
    """
    This is the senator vertex which stores the different kinds of data that senators can have

    Instance Attributes:
    - name: the name of the senator
    - transaction_numbers: The list of the transactions done by the senators
    - neighbours: It's a dict mapping the SenatorVertex to its transaction numbers
    - yearly_return: It is a list of annual return on investment of senators. Yearly return can be an empty list
    if the senator has only traded for a year
    - sus_type: It is a str categrory out of high, low, medium that classifies senators based upon how suspicious
    their ROI is

    Representation Invariants:
    - name != ''
    - neighbours != {}
    - sus_type != ''
    """
    name: str
    neighbours: dict[_StockVertex, list[int]]
    yearly_return: list[float]
    sus_type: str

    def __init__(self, name: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.
        """
        self.name = name
        self.neighbours = {}
        self.yearly_return = []
        self.sus_type = "low"

    def calculate_mean_yearly_return(self) -> float:
        """
        places the senator on how suspicious they are insider information
        """
        if self.yearly_return:
            return sum(self.yearly_return) / len(self.yearly_return)
        else:
            return 0


class _StockVertex(_Vertex):
    """
    This is the vertex that will store all the stock data

    Instance Attributes:
    name: The symbol of the stock on Stock Market like 'MSFT'
    neighbours: It's a dict mapping the StockVertex to transcation numbers

    Representation Invariants:
    - name != ''
    - neighbours != {}
    """
    name: str
    neighbours: dict[_SenatorVertex, list[int]]

    def __init__(self, name: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.
        """
        self.name = name
        self.neighbours = {}


class Graph:
    """
    This is the class for the graph mapping the stocks to the senators.

    # Private Instance Attributes:
    # - _vertices: It is a dictionary that maps the items to their respective Stock or Senator Vertex

    # Representation Invariants:
    # - _vertices != {}
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_edge(self, item1: Any, item2: Any, trans: int) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            if v1 in v2.neighbours.keys() and v2 in v1.neighbours.keys():
                v1.neighbours[v2].append(trans)
                v2.neighbours[v1].append(trans)
            else:
                v1.neighbours[v2] = [trans]
                v2.neighbours[v1] = [trans]
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.name == item2 for v2 in v1.neighbours.keys())
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.name for neighbour in v.neighbours.keys()}
        else:
            raise ValueError

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        >>> g = Graph()
        >>> senator_1 = _SenatorVertex("Johnny")
        >>> senator_2 = _SenatorVertex("Hello")
        >>> stock_1 = _StockVertex("Apple")
        >>> g._vertices["Johnny"] = senator_1
        >>> g._vertices["Hello"] = senator_2
        >>> g._vertices["Apple"] = stock_1
        >>> g.add_edge("Johnny", "Apple", 1)
        >>> g.add_edge("Hello", "Apple", 2)
        >>> graph_nx1 = g.to_networkx()
        >>> isinstance(graph_nx1.nodes["Hello"]['value'], _SenatorVertex)
        True
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.name, value=v)
            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.name, value=u)
                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(v.name, u.name, weight=len(v.neighbours[u]))
            if graph_nx.number_of_nodes() >= max_vertices:
                break
        return graph_nx

    def load_graph(self, data: str = 'Senator Stock Trades Updated.csv', calc_file: str = 'bro') -> None:

        """Makes a graph using the given data."""

        df = pd.read_csv(data)

        df = df.loc[df['Ticker'] != '--']

        for i in df.Ticker.unique():
            self._vertices[i] = _StockVertex(i)
        for k in df.Office_FilerType.unique():
            self._vertices[k] = _SenatorVertex(k)
            if not calc_file:
                self._vertices[k].yearly_return = calc_roi_per_year(k, df)
                # Can do this since we are only accessing Senator Vertex which has this attribute
            else:
                self._vertices[k].yearly_return = DICTOFSENS[k]

        for j in range(df.shape[0]):
            self.add_edge(df.iloc[j].Office_FilerType, df.iloc[j].Ticker, df.iloc[j].Transaction_Number)

        self.sus_level_calculator()

    def sus_level_calculator(self) -> None:
        """
        This is used to calculate how suspicious the senator is
        """

        total_transaction_counter = 0
        counter = 0
        loss_bro = [v for v in self._vertices.values() if isinstance(v, _SenatorVertex)]
        for vertex in loss_bro:
            total_transaction_counter += vertex.calculate_mean_yearly_return()
            counter += 1
        if counter != 0:
            mean = total_transaction_counter / counter
            for vertex in loss_bro:
                senator_mean = vertex.calculate_mean_yearly_return()
                if senator_mean > (3 / 2) * mean:
                    vertex.sus_type = "high"
                elif senator_mean > mean:
                    vertex.sus_type = "mid"
                else:
                    continue

###############################################################################################################
# Functions
###############################################################################################################


def open_price_date(ticker: str, date: str) -> float:
    """
    Returns the open stock price of the given stock ticker.

    >>> round(open_price_date('MSFT', '22-03-2023'), 2)
    271.17
    """
    split_date = date.split('-')
    dte, mon, year = int(split_date[0]), int(split_date[1]), int(split_date[2])
    ticker = yfinance.Ticker(ticker)
    date = datetime.date(year, mon, dte)
    next_date = date + datetime.timedelta(days=1)
    t = True
    data = ticker.history(start=date, end=next_date)
    x = []
    while t and len(x) < 2:
        t = False
        try:
            data['Open'].loc[data.index[0]]
        except:
            date = date - datetime.timedelta(days=1)
            next_date = next_date + datetime.timedelta(days=1)
            data = ticker.history(start=date, end=next_date)
            t = True
            x.append(1)
    try:
        return data['Open'].loc[data.index[0]]
    except:
        return 30.0
        # We are inputting 30 as a mean value of stocks that cannot be found by yfinance even after shifting dates
        # for the next available market open date


def calc_roi_per_year(name: str, df: pd.DataFrame) -> list[float]:
    """Given the senator name and dataframe, this function returns their return on investment per year"""
    df = df[df.Ticker != '--']
    df1 = df[df.Office_FilerType == name]
    if df1.shape[0] == 0:
        return [0.0]
    df2 = df1.iloc[::-1]
    stock_counter = []
    balance_counter = []
    year_counter = []
    num_years = int(df2.iloc[-1].Transaction_Date[-2:]) - int(df2.iloc[0].Transaction_Date[-2:])
    index = 0
    k = int(df2.iloc[index].Transaction_Date[-2:])
    for _ in range(num_years):
        stock = {}
        balance = 0

        if stock_counter:
            stock = stock_counter[-1]

        if balance_counter:
            balance = balance_counter[-1]

        while int(df2.iloc[index].Transaction_Date[-2:]) == k:
            if df2.iloc[index].Transaction_Type == 'Purchase':
                st = df2.iloc[index].Amount / open_price_date(df2.iloc[index].Ticker, df2.iloc[index].Transaction_Date)
                if df2.iloc[index].Ticker not in stock.keys():
                    stock[df2.iloc[index].Ticker] = st
                else:
                    stock[df2.iloc[index].Ticker] += st
                balance = balance - float(df2.iloc[index].Amount)

            elif df2.iloc[index].Transaction_Type == 'Sale (Full)':
                if df2.iloc[index].Ticker in stock:
                    balance += df2.iloc[index].Amount
                    stock[df2.iloc[index].Ticker] = 0
                else:
                    balance += df2.iloc[index].Amount

            else:
                if df2.iloc[index].Ticker in stock:
                    num_stock = df2.iloc[index].Amount / open_price_date(df2.iloc[index].Ticker,
                                                                         df2.iloc[index].Transaction_Date)
                    if (stock[df2.iloc[index].Ticker] - num_stock) > 0:
                        stock[df2.iloc[index].Ticker] -= num_stock
                    else:
                        stock[df2.iloc[index].Ticker] = 0
                    balance += df2.iloc[index].Amount
                else:
                    balance += df2.iloc[index].Amount

            index += 1
        stock_counter.append(stock.copy())
        balance_counter.append(balance)
        year_counter.append(k)
        k += 1

    bala = [
        [stock_counter[x][y] * open_price_date(y, '31-12-20' + str(year_counter[x])) for y in stock_counter[x].keys()]
        for x in range(len(stock_counter))]
    bala2 = [sum(bro) for bro in bala]
    effective_bal = [bala2[numm] + balance_counter[numm] for numm in range(len(balance_counter))]
    if len(effective_bal) == 1:
        return []
    else:
        return [((effective_bal[x] - effective_bal[x - 1]) / effective_bal[x - 1]) * 100 for x in
                range(1, len(effective_bal))]


def small_test_for_calc(names: list[str], df: pd.DataFrame = pd.read_csv("Senator Stock Trades updated.csv")) -> list:
    """A small test to check the logical soundness of the calc_roi_per_year. Accepts a list of Senator names and
    calculates their return on investment based on the dataset provided(by default set to the entire transaction data)
    In order to accurately test the function, please use senators who have more than 1 year of stock trading history
    The following are some senators that have more than 1 year of history -
    'Sullivan, Dan (Senator)'
    'McConnell, A. Mitchell Jr. (Senator)'
    'Peters, Gary (Senator)'
    'Collins, Susan M. (Senator)'
    'King, Angus (Senator)'
    'Capito, Shelley Moore (Senator)'
    'Carper, Thomas R. (Senator)'
    """
    final = []
    for name in names:
        final.append(calc_roi_per_year(name, df))
    return final


def get_no_trans(vert: _Vertex) -> int:
    """
    Returns the number of transactions associatied with the vertex
    """

    a = list(vert.neighbours.values())
    b = sum([sum(x) for x in a])
    return b

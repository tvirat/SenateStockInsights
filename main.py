"""The Main File for our Project"""

import pandas as pd
from Vizualization import visualize_graph, visualize_senators, visualize_stocks, visualize_states
from Data_and_Functions import Graph, small_test_for_calc

df = pd.read_csv("Senator Stock Trades updated.csv")
G = Graph()
G.load_graph()
cont = True
while cont:
    print("What would you like to do?")
    print("1 Vizualize the Graph")
    print("2 Test the return on investment function")
    print("3 Vizualize top 10 stocks")
    print("4 Vizualize top 10 states")
    print("5 Vizualize top 10 senators")
    print("Choose(1/2/3/4/5)")
    x = input()
    if x == "1":
        visualize_graph(G)
    if x == "2":
        print(small_test_for_calc(['McConnell, A. Mitchell Jr. (Senator)'], df))
    if x == "3":
        visualize_stocks(10)
    if x == "4":
        visualize_states(10)
    if x == "5":
        visualize_senators(10)
    print("would you like to continue? (Y/N)")
    y = input()
    if y == "N":
        cont = False

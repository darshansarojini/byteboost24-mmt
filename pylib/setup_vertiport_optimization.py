import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from pyomo.environ import (
    ConcreteModel,
    Var,
    Objective,
    Constraint,
    Set,
    Param,
    SolverFactory,
    Binary,
)

from pylib.decide_trips import (
    decide_trips,
)


def edge_constraint(model):
    return sum(model.x[e] for e in model.edges) >= 2


def linear_cost(model):
    return sum(model.costs[e] * model.x[e] for e in model.edges)


def vertiport_route_optimization(trips, vertiports, routes, params):
    # Create a model
    model = ConcreteModel()

    # Define nodes and edges
    nodes = list(vertiports["nodeid"])
    edges = [(int(edge[0]), int(edge[1])) for edge in routes.to_numpy()]

    model.edges = Set(initialize=edges)
    model.nodes = Set(initialize=nodes)

    # Define decision variables
    model.x = Var(model.edges, domain=Binary)

    # Define objective function
    def edge_costs(model, i, j):
        this_edge_route = pd.DataFrame(
            data=np.array([[i, j]]), columns=["source nodeid", "target nodeid"]
        )
        res = decide_trips(trips, vertiports, this_edge_route, params)

        cost = res.loc[res["cost sensitive"], "trip cost"]
        time = res.loc[~res["cost sensitive"], "trip duration"]

        return np.sum(cost) + np.sum(time)


    model.costs = Param(model.edges, initialize=edge_costs)
    model.obj = Objective(rule=linear_cost, sense="minimize")

    # Define constraints
    model.edge_constraint = Constraint(rule=edge_constraint)

    # Solve the problem
    solver = SolverFactory("cbc")  # Use appropriate solver
    result = solver.solve(model, tee=True)

    # Print results
    print("Results:")
    for e in model.edges:
        print(f"Edge {e} selected: {model.x[e].value}")
    print(f"Total Cost: {model.obj.expr()}")

    # Create a graph for visualization
    G = nx.Graph()

    # Add nodes with positions
    for node in nodes:
        node_df = vertiports.loc[vertiports["nodeid"] == node]
        x = float(node_df["latitude"])
        y = float(node_df["longitude"])
        G.add_node(node, pos=(x, y))

    # Add edges based on the solution
    for e in edges:
        if model.x[e].value == 1:
            G.add_edge(e[0], e[1])

    # Get positions from the graph
    pos = nx.get_node_attributes(G, "pos")

    # Draw the graph
    plt.figure(figsize=(10, 7))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=500,
        node_color="lightblue",
        edge_color="gray",
        font_size=16,
        font_weight="bold",
        width=2,
    )
    plt.title("Optimal Network Visualization")
    plt.show()

    return

from pyomo.environ import ConcreteModel, Var, Objective, Constraint, Binary, Set, Param, SolverFactory
import math
import networkx as nx
# import matplotlib.pyplot as plt

# Define coordinates for 10 nodes in an irregular layout
node_coordinates = {
    1: (1, 2),
    2: (3, 5),
    3: (6, 1),
    4: (8, 7),
    5: (9, 2),
    6: (2, 8),
    7: (5, 6),
    8: (7, 3),
    9: (4, 4),
    10: (8, 1)
}

# Define the maximum flying range
MAX_RANGE = 40  # Example maximum range

# Define a fixed cost and a proportional cost factor
FIXED_COST = 5
PROPORTIONAL_COST_FACTOR = 1  # Cost per unit distance

# Function to compute Euclidean distance between two nodes
def compute_distance(node1, node2):
    x1, y1 = node_coordinates[node1]
    x2, y2 = node_coordinates[node2]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# Function to compute weighted cost based on distance
def compute_cost(node1, node2):
    distance = compute_distance(node1, node2)
    return FIXED_COST + PROPORTIONAL_COST_FACTOR * distance

# Create a model
model = ConcreteModel()

# Define nodes and edges
nodes = list(node_coordinates.keys())
edges = [(i, j) for i in nodes for j in nodes if i < j]  # Create edges (i < j to avoid duplicates)

model.edges = Set(initialize=edges)
model.nodes = Set(initialize=nodes)

# Define parameters
def edge_costs(model, i, j):
    return compute_cost(i, j)

def edge_distances(model, i, j):
    return compute_distance(i, j)

model.costs = Param(model.edges, initialize=edge_costs)
model.distances = Param(model.edges, initialize=edge_distances)

# Define decision variables
model.x = Var(model.edges, domain=Binary)

# Define the linear cost function
def linear_cost(model):
    return sum(model.costs[e] * model.x[e] for e in model.edges)

model.obj = Objective(rule=linear_cost, sense='minimize')

# Define constraints
def edge_constraint(model):
    return sum(model.x[e] for e in model.edges) >= 4

model.edge_constraint = Constraint(rule=edge_constraint)

# Add constraint for maximum flying range
def max_range_constraint(model, i, j):
    if model.distances[i, j] > MAX_RANGE:
        return model.x[i, j] == 0
    return Constraint.Skip
    # return model.x[i, j] <= (model.distances[i, j] / MAX_RANGE)

model.max_range_constraint = Constraint(model.edges, rule=max_range_constraint)

# Define degree constraint: maximum of 3 connections per node
def degree_constraint(model, node):
    return sum(model.x[e] for e in model.edges if node in e) <= 3

model.degree_constraint = Constraint(model.nodes, rule=degree_constraint)

# Solve the problem
solver = SolverFactory('cbc')  # Use appropriate solver
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
    G.add_node(node, pos=node_coordinates[node])

# Add edges based on the solution
for e in edges:
    if model.x[e].value == 1:
        G.add_edge(e[0], e[1])

# Get positions from the graph
pos = nx.get_node_attributes(G, 'pos')

# # Draw the graph
# plt.figure(figsize=(10, 7))
# nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', edge_color='gray', font_size=16, font_weight='bold', width=2)
# plt.title("Optimal Network Visualization")
# plt.show()

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node("sadasd1")

node_list = [
    "node1",
    "node2"
]
G.add_nodes_from(node_list)
print(G.nodes)

G.add_edge("node1", "node2")
G.add_edge("node1", "node6")

edges_only = [
    ["node1", "node3"],
    ["node1", "node6"]
]

G.add_edges_from(edges_only)

edges_with_properties = [
    ("node1", "node5", {"weight": 3}),
    ("node2", "node4", {"weight": 5})
]

G.add_edges_from(edges_with_properties)

weights = [1 if 'weight' not in G[u][v] else G[u][v]['weight'] for u, v in G.edges()]

print(weights)
nx.draw(G, width=weights)
plt.show()

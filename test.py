from graphviz import Digraph


dot = Digraph()


dot.node('A', 'Node A')
dot.node('B', 'Node B')
dot.node('C', 'Node C')

# Add edges
dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'A')

# Display the graph
dot.render('test_graph', format='png', cleanup=False)  # This will save and remove the .dot file

print(dot.source)  # Print the DOT source for verification


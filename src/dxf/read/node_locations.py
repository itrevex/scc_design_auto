import numpy as np

class NodeLocations():
    CORNER_NODES = 2
    CENTER_NODES = 4 
    EDGE_NODES = 3

    def __init__(self, conns_array):
        nodes = conns_array.flatten()
        unique, counts = np.unique(nodes, return_counts=True)
        self.node_counts = dict(zip(unique, counts))


    def getCornerNodes(self):
        corner_nodes = [key for key, value in self.node_counts.items() \
            if value == NodeLocations.CORNER_NODES ]

        return np.array(corner_nodes)

    def getCenterNodes(self):
        center_nodes = [key for key, value in self.node_counts.items() \
            if value == NodeLocations.CENTER_NODES ]
        return np.array(center_nodes)

    def getEdgeNodes(self):
        edge_nodes = [key for key, value in self.node_counts.items() \
            if value == NodeLocations.EDGE_NODES ]
        return np.array(edge_nodes)
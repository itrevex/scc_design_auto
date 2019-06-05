import numpy as np

class NodeLocations():
    CORNER_NODES = 2
    CENTER_NODES = 4 
    EDGE_NODES = 3

    def __init__(self, conns_array, **kw):
        nodes = conns_array.flatten()
        self.conns_array = conns_array
        unique, counts = np.unique(nodes, return_counts=True)
        self.node_counts = dict(zip(unique, counts))
        self.nodes_array = kw.get('nodes_array', None)


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


    def getStartNode(self):
        '''
        This is the node located at the bottom left corner of the geometery
        '''
        corner_nodes = self.getCornerNodes().tolist()
        left_bottom_corner_nodes = []

        for node in corner_nodes:
            node_lines = self.getNodeLines(node)
            end_nodes = self.getOppositeEndNodes(node, node_lines)
            bottom_node = self.getNodeBottomNode(node, end_nodes)
            left_node = self.getNodeLeftNode(node, end_nodes)

            if left_node == None and bottom_node == None:
                left_bottom_corner_nodes.append(node)

        return self.getExtremeLeftNode(left_bottom_corner_nodes)

    def getExtremeLeftNode(self, nodes):
        min_x = self.nodes_array[nodes[0], 0]
        extreme_node = nodes[0]
        for node in nodes:
            node_x = self.nodes_array[node, 0]
            if node_x < min_x:
                extreme_node = node
        return extreme_node

    def getNodeLines(self, node):
        return np.where(self.conns_array==node)[0]

    def getOppositeEndNodes(self, node, lines):
        '''
        node is the node in questions
        lines are the lines connected to node

        Method return the end nodes of the 'node' in question using the
        lines connected to the node
        '''
        opposite_end_nodes = []
        for line in lines:
            line_nodes = self.conns_array[line].tolist()
            line_nodes.remove(node)
            opposite_end_nodes.append(line_nodes[0])
        return opposite_end_nodes

    def getNodeTopNode(self, node, end_nodes):
        base_y = self.nodes_array[node, 1]
        higher_nodes = []
        for end_node in end_nodes:
            end_node_y = self.nodes_array[end_node, 1]
            if end_node_y > base_y:
                higher_nodes.append(end_node)
        if len(higher_nodes)== 0:
            return None
        return max(higher_nodes)

    def getNodeRightNode(self, node, end_nodes):
        base_x = self.nodes_array[node, 0]
        higher_nodes = []
        for end_node in end_nodes:
            end_node_x = self.nodes_array[end_node, 0]
            if end_node_x > base_x:
                higher_nodes.append(end_node)
        if len(higher_nodes)== 0:
            return None
        return max(higher_nodes)
  
    def getNodeBottomNode(self, node, end_nodes):
        base_y = self.nodes_array[node, 1]
        lower_nodes = []
        for end_node in end_nodes:
            end_node_y = self.nodes_array[end_node, 1]
            if end_node_y < base_y:
                lower_nodes.append(end_node)
        if len(lower_nodes)== 0:
            return None
        return min(lower_nodes)

    def getNodeLeftNode(self, node, end_nodes):
        base_x = self.nodes_array[node, 0]
        lower_nodes = []
        for end_node in end_nodes:
            end_node_x = self.nodes_array[end_node, 0]
            if end_node_x < base_x:
                lower_nodes.append(end_node)
        if len(lower_nodes)== 0:
            return None
        return min(lower_nodes)

    def getBottomEdgeNodes(self):
        bottom_edge_nodes = []
        all_edge_nodes = []
        all_edge_nodes.extend(self.getEdgeNodes())
        all_edge_nodes.extend(self.getCornerNodes())
        for node in all_edge_nodes:
            lines = self.getNodeLines(node)
            end_nodes = self.getOppositeEndNodes(node, lines)
            bottom_node = self.getNodeBottomNode(node, end_nodes)

            if bottom_node == None:
                bottom_edge_nodes.append(node)
        return set(bottom_edge_nodes)

    def getLeftEdgeNodes(self):
        left_edge_nodes = []
        all_edge_nodes = []
        all_edge_nodes.extend(self.getEdgeNodes())
        all_edge_nodes.extend(self.getCornerNodes())
        for node in all_edge_nodes:
            lines = self.getNodeLines(node)
            end_nodes = self.getOppositeEndNodes(node, lines)
            left_edge_node = self.getNodeLeftNode(node, end_nodes)

            if left_edge_node == None:
                left_edge_nodes.append(node)
        return set(left_edge_nodes)
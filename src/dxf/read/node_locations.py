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
            bottom_node = self.getNodeBottomNode(node)
            left_node = self.getNodeLeftNode(node)

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

    def getNodeEndNodes(self, node):
        '''
        node is the node in questions
        lines are the lines connected to node

        Method return the end nodes of the 'node' in question using the
        lines connected to the node
        '''
        lines = self.getNodeLines(node)
        opposite_end_nodes = []
        for line in lines:
            line_nodes = self.conns_array[line].tolist()
            line_nodes.remove(node)
            opposite_end_nodes.append(line_nodes[0])
        return opposite_end_nodes

    def getNodeTopNode(self, node):
        end_nodes = self.getNodeEndNodes(node)
        base_y = self.nodes_array[node, 1]
        higher_nodes = []
        for end_node in end_nodes:
            end_node_y = self.nodes_array[end_node, 1]
            if end_node_y > base_y:
                higher_nodes.append(end_node)
        if len(higher_nodes)== 0:
            return None
        return max(higher_nodes)

    def getNodeRightNode(self, node):
        end_nodes = self.getNodeEndNodes(node)
        base_x = self.nodes_array[node, 0]
        higher_nodes = []
        for end_node in end_nodes:
            end_node_x = self.nodes_array[end_node, 0]
            if end_node_x > base_x:
                higher_nodes.append(end_node)
        if len(higher_nodes)== 0:
            return None
        return max(higher_nodes)
  
    def getNodeBottomNode(self, node):
        end_nodes = self.getNodeEndNodes(node)
        base_y = self.nodes_array[node, 1]
        lower_nodes = []
        for end_node in end_nodes:
            end_node_y = self.nodes_array[end_node, 1]
            if end_node_y < base_y:
                lower_nodes.append(end_node)
        if len(lower_nodes)== 0:
            return None
        return min(lower_nodes)

    def getNodeLeftNode(self, node):
        end_nodes = self.getNodeEndNodes(node)
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
            bottom_node = self.getNodeBottomNode(node)

            if bottom_node == None:
                bottom_edge_nodes.append(node)
        return set(bottom_edge_nodes)

    def getLeftEdgeNodes(self):
        left_edge_nodes = []
        all_edge_nodes = []
        all_edge_nodes.extend(self.getEdgeNodes())
        all_edge_nodes.extend(self.getCornerNodes())
        for node in all_edge_nodes:
            left_edge_node = self.getNodeLeftNode(node)

            if left_edge_node == None:
                left_edge_nodes.append(node)
        return set(left_edge_nodes)

    def getBottomEdgeLines(self):
        bottom_edge_nodes = self.getBottomEdgeNodes()
        bottom_edge_lines = []
        for index in range(self.conns_array.shape[0]):
            line = set(self.conns_array[index].tolist())
            if line.issubset(bottom_edge_nodes):
                bottom_edge_lines.append(index)

        return set(bottom_edge_lines)

    def getIntersectedLine(self, total_length):
        '''
        Gets line along edge in between which the point is located.
        Total length is distance from bottom edge node along the x axis
        to the point that when the loads portition stops
        '''
        lines = self.getBottomEdgeLines()
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_x = self.nodes_array[start_node, 0]
            end_node_x = self.nodes_array[end_node, 0]
            if self.isPointWithinPoints(total_length, [start_node_x, end_node_x]):
                return line

    def isPointWithinPoints(self, point, points):
        start_point = points[0]
        end_point = points[1]
        if start_point < point and end_point > point:
            return True
        #this is done in case points have been interchanged
        if end_point < point and start_point > point:
            return True
        return False

    def isPointLeftToThePoints(self, point, points):
        start_point = points[0]
        end_point = points[1]
        if start_point < point and end_point < point:
            return True
        #no need to check interchangeability since both points are less
        #than the point
        return False

    def selectNearerNode(self, total_length, line, in_start_node):
        end_node_1 = self.conns_array[line,0]
        end_node_2 = self.conns_array[line, 1]
        end_node_1_x = self.nodes_array[end_node_1, 0]
        end_node_2_x = self.nodes_array[end_node_2, 0]

        start_node = end_node_1
        end_node = end_node_2
        if end_node_1_x > total_length:
            start_node = end_node_2
            end_node = end_node_1

        start_node_x = self.nodes_array[start_node, 0]

        #module is the distance between nodes
        module = abs(end_node_1_x - end_node_2_x)
        #find portion towards the start node. If this portion is greater than or equal
        #0.5 use end line node and end node other use start node as line node
        percentage_portion = (total_length - start_node_x) / module

        if percentage_portion >= 0.5 or start_node == in_start_node:
            return end_node

        return start_node

    def getNodesAlongNodeInY(self, node, nodes_along=set()):
        '''
        Function finds nodes a long a node towards a specified direction,
        say y or x directions.
        '''
        nodes_along.add(node)
        top_node = self.getNodeTopNode(node)
        if top_node != None:
            self.getNodesAlongNodeInY(top_node, nodes_along)

        return nodes_along

    def getBottomNodesWithinSelectedPortion(self, start_node, end_node):
        nodes = [start_node, end_node]
        nodes_within_portion = set(nodes)
        bottom_nodes = self.getBottomEdgeNodes()
        for node in bottom_nodes:
            if self.isNodeInBetweenNodes(node, nodes):
                nodes_within_portion.add(node)
        return nodes_within_portion

    def isNodeInBetweenNodes(self, node, nodes):
        point = self.nodes_array[node, 0]
        end_1 = self.nodes_array[nodes[0], 0]
        end_2 = self.nodes_array[nodes[1], 0]

        return self.isPointWithinPoints(point, [end_1, end_2])

    def getNodesWithinPortition(self, start_node, total_length):
        #1. get portion end node
        #a) get intersected line
        cut_line = self.getIntersectedLine(total_length)
        #b) get neaer node of line which is end node of portion
        end_node =  self.selectNearerNode(total_length, cut_line, start_node)
        #2. get nodes along bottom edge
        portion_bottom_nodes = \
            self.getBottomNodesWithinSelectedPortion(start_node, end_node)
        #3. get all top nodes for nodes along bottom edge
        portion_nodes = set()
        for node in portion_bottom_nodes:
            node_top_nodes = self.getNodesAlongNodeInY(node, set())
            portion_nodes.update(node_top_nodes)
        #return these nodes as nodes within portion
        return portion_nodes
    
    def getLinesWithinPortition(self, start_node, total_length):
        nodes_in_portion = self.getNodesWithinPortition(start_node, total_length)
        lines = set()
        for node in nodes_in_portion:
            node_lines = self.getNodeLines(node)
            for line in node_lines:
                if self.isLineInNodePool(line, nodes_in_portion):
                    lines.add(line)
        print(lines)
        return lines

    def isLineInNodePool(self, line, node_pool):
        line_nodes = self.conns_array[line].tolist()
        for node in line_nodes:
            if node not in node_pool:
                return False

        return True
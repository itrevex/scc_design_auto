import numpy as np
from sympy import Plane, Point3D
import random

class NodeLocations():
    CORNER_NODES = 2
    CENTER_NODES = 4 
    EDGE_NODES = 3

    def __init__(self, conns_array, **kw):
        nodes = conns_array.flatten() #make conns a 1d array
        self.conns_array = conns_array
        #get how mnay times each node appears in array
        unique, counts = np.unique(nodes, return_counts=True)
        #create dictionary of nodes with their counts
        self.node_counts = dict(zip(unique, counts))
        self.nodes_array = kw.get('nodes_array', None)


    def getCornerNodes(self, region_lines=[]):
        if len(region_lines) == 0:
            node_counts = self.node_counts
        else:
            region_conns_array = self.getRegionConnsArray(region_lines)
            node_counts = self.getRegionNodeCounts(region_conns_array)
        
        corner_nodes = [key for key, value in node_counts.items() \
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


    def getStartNode(self, region_lines=[]):
        '''
        This is the node located at the bottom left corner of the geometery
        '''
        corner_nodes = self.getCornerNodes(region_lines).tolist()
        left_bottom_corner_nodes = []

        for node in corner_nodes:
            bottom_node = self.getNodeBottomNode(node, region_lines)
            left_node = self.getNodeLeftNode(node, region_lines)
            #if no has no bottom node and node left node, then it is most likely
            #to be in a bottom left corner
            if left_node == None and bottom_node == None:
                left_bottom_corner_nodes.append(node)

        return self.getExtremeLeftNode(left_bottom_corner_nodes)

    def getEndNode(self):
        '''
        This is the node located at the bottom left corner of the geometery
        '''
        corner_nodes = self.getCornerNodes().tolist()
        right_bottom_corner_nodes = []

        for node in corner_nodes:
            bottom_node = self.getNodeBottomNode(node)
            right_node = self.getNodeRightNode(node)
            #if no has no bottom node and node right node, then it is most likely
            #to be in a bottom right corner
            if right_node == None and bottom_node == None:
                right_bottom_corner_nodes.append(node)

        return self.getExtremeRightNode(right_bottom_corner_nodes)

    def getLeftTopNode(self):
        '''
        Returns top left corner node (end node for y direction)
        '''
        corner_nodes = self.getCornerNodes().tolist()
        left_edge_corner_nodes = []

        for node in corner_nodes:
            top_node = self.getNodeTopNode(node)
            left_node = self.getNodeLeftNode(node)
            #if no has no top node and node left node, then it is most likely
            #to be in a top left corner
            if top_node == None and left_node == None:
                left_edge_corner_nodes.append(node)

        return self.getExtremeLeftNode(left_edge_corner_nodes)
    
    def getExtremeRightNode(self, nodes):
        max_x = self.nodes_array[nodes[0], 0]
        extreme_node = nodes[0]
        for node in nodes:
            node_x = self.nodes_array[node, 0]
            if node_x > max_x:
                extreme_node = node
        return extreme_node

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

    def getPortoinNodeLines(self, node, region_lines):
        lines = self.getNodeLines(node).tolist()
        portion_lines = []
        for line in lines:
            if line in region_lines:
                portion_lines.append(line)
    
        return portion_lines

    def getNodeEndNodes(self, node, region_lines=[]):
        '''
        node is the node in questions
        lines are the lines connected to node

        Method return the end nodes of the 'node' in question using the
        lines connected to the node
        '''

        if len(region_lines) == 0:
            lines = self.getNodeLines(node)
        else:
            lines = self.getPortoinNodeLines(node, region_lines)

        
        opposite_end_nodes = []
        for line in lines:
            line_nodes = self.conns_array[line].tolist()
            line_nodes.remove(node)
            opposite_end_nodes.append(line_nodes[0])

        return opposite_end_nodes

    def getNodeTopNode(self, node, region_lines=[]):

        end_nodes = self.getNodeEndNodes(node, region_lines)

        base_y = self.nodes_array[node, 1]
        higher_nodes = []
        for end_node in end_nodes:
            end_node_y = self.nodes_array[end_node, 1]
            if end_node_y > base_y:
                higher_nodes.append(end_node)
        if len(higher_nodes)== 0:
            return None
        return max(higher_nodes)

    def getNodeRightNode(self, node, region_lines=[]):
        end_nodes = self.getNodeEndNodes(node, region_lines)
        base_x = self.nodes_array[node, 0]
        higher_nodes = []
        for end_node in end_nodes:
            end_node_x = self.nodes_array[end_node, 0]
            if end_node_x > base_x:
                higher_nodes.append(end_node)
        if len(higher_nodes)== 0:
            return None
        return max(higher_nodes)
  
    def getNodeBottomNode(self, node, region_lines=[]):
        end_nodes = self.getNodeEndNodes(node, region_lines)
        base_y = self.nodes_array[node, 1]
        lower_nodes = []
        for end_node in end_nodes:
            end_node_y = self.nodes_array[end_node, 1]
            if end_node_y < base_y:
                lower_nodes.append(end_node)
        if len(lower_nodes)== 0:
            return None
        return min(lower_nodes)

    def getNodeLeftNode(self, node, region_lines=[]):
        end_nodes = self.getNodeEndNodes(node, region_lines)
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
        '''
        Return value: set()
        Gets all bottom edge lines
        '''
        bottom_edge_nodes = self.getBottomEdgeNodes()
        bottom_edge_lines = []
        for index in range(self.conns_array.shape[0]):
            line = set(self.conns_array[index].tolist())
            if line.issubset(bottom_edge_nodes):
                bottom_edge_lines.append(index)

        return set(bottom_edge_lines)

    def getLeftEdgeLines(self):
        '''
        Return value: set()
        Gets all left edge lines
        '''
        left_edge_nodes = self.getLeftEdgeNodes()
        left_edge_lines = []
        for index in range(self.conns_array.shape[0]):
            line = set(self.conns_array[index].tolist())
            if line.issubset(left_edge_nodes):
                left_edge_lines.append(index)
        # for line in left_edge_lines:
        #     print(line, self.conns_array[line])
        return set(left_edge_lines)

    def getIntersectedLine(self, total_length):
        '''
        Gets line along edge in between which the point is located.
        Total length is distance from bottom edge node along the x axis
        to the point that when the loads portition stops
        '''
        length = self.getLengthFromStartNode(total_length)
        lines = self.getBottomEdgeLines()
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_x = self.nodes_array[start_node, 0]
            end_node_x = self.nodes_array[end_node, 0]
            if self.isPointWithinPoints(length, [start_node_x, end_node_x]):
                return line
        #find line that does not cut any point, right line equal to none
        if total_length < 0:
            return self.extremeLeftBottomLine(lines)
        return self.extremeRightBottomLine(lines)

    def getIntersectedVerticalLine(self, total_height):
        '''
        Gets line along edge in between which the point is located.
        Total height is distance from bottom edge node along the y axis
        to the point that when the loads portition stops
        '''
        height = self.getHeightFromTopLeftNode(total_height)
        lines = self.getLeftEdgeLines()
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_y = self.nodes_array[start_node, 1]
            end_node_y = self.nodes_array[end_node, 1]
            if self.isPointWithinPoints(height, [start_node_y, end_node_y]):
                return line
        #find line that does not cut any point, right line equal to none
        if total_height < 0:
            return self.extremeBottomLeftLine(lines)
        return self.extremeTopLeftLine(lines)
        

    def getLengthFromStartNode(self, total_length):
        length = total_length
        if total_length < 0:
            extreme_node = self.getEndNode()
            extreme_node_x = self.nodes_array[extreme_node, 0]
            #extreme_node_x is L, the length of drawing
            length = extreme_node_x - abs(total_length)
        if length < 0:
            return 0
        return length

    def getHeightFromTopLeftNode(self, total_height):
        height = total_height
        if total_height < 0:
            extreme_node = self.getLeftTopNode()
            extreme_node_y = self.nodes_array[extreme_node, 1]
            #extreme_node_y is H, the height of drawing
            height = extreme_node_y - abs(total_height)
        if height < 0:
            return 0
        return height

    def extremeTopLeftLine(self, lines):
        extreme_line = list(lines)[0]
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_y = self.nodes_array[start_node, 1]
            end_node_y = self.nodes_array[end_node, 1]

            end_node = end_node_y
            if start_node_y > end_node:
                end_node = start_node_y

            ext_start_node = self.conns_array[extreme_line,0]
            ext_end_node = self.conns_array[extreme_line, 1]
            ext_start_node_y = self.nodes_array[ext_start_node, 1]
            ext_end_node_y = self.nodes_array[ext_end_node, 1]

            ext_end_node = ext_end_node_y
            if ext_start_node_y > ext_end_node:
                ext_end_node = ext_start_node_y

            if end_node > ext_end_node:
                extreme_line = line
            
        return extreme_line

    def extremeRightBottomLine(self, lines):
        extreme_line = list(lines)[0]
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_x = self.nodes_array[start_node, 0]
            end_node_x = self.nodes_array[end_node, 0]

            end_node = end_node_x
            if start_node_x > end_node:
                end_node = start_node_x

            ext_start_node = self.conns_array[extreme_line,0]
            ext_end_node = self.conns_array[extreme_line, 1]
            ext_start_node_x = self.nodes_array[ext_start_node, 0]
            ext_end_node_x = self.nodes_array[ext_end_node, 0]

            ext_end_node = ext_end_node_x
            if ext_start_node_x > ext_end_node:
                ext_end_node = ext_start_node_x

            if end_node > ext_end_node:
                extreme_line = line
            
        return extreme_line

    def extremeLeftBottomLine(self, lines):
        extreme_line = list(lines)[0]
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_x = self.nodes_array[start_node, 0]
            end_node_x = self.nodes_array[end_node, 0]

            start_node = start_node_x
            if end_node_x < start_node:
                start_node = end_node_x

            #find extreme line for comparisons
            ext_start_node = self.conns_array[extreme_line,0]
            ext_end_node = self.conns_array[extreme_line, 1]
            ext_end_node_x = self.nodes_array[ext_end_node, 0]

            #find actual end_node in this mix
            ext_start_node = end_node_x
            if ext_end_node_x < ext_start_node:
                ext_start_node = ext_end_node_x

            if start_node < ext_start_node:
                extreme_line = line
            
        return extreme_line

    def extremeBottomLeftLine(self, lines):
        '''
        Extreme bottom left meaning in relation to vertical lines, 
        line at the bottom of the left lines
        '''
        extreme_line = list(lines)[0]
        for line in lines:
            start_node = self.conns_array[line,0]
            end_node = self.conns_array[line, 1]
            start_node_y = self.nodes_array[start_node, 1]
            end_node_y = self.nodes_array[end_node, 1]

            start_node = start_node_y
            if end_node_y < start_node:
                start_node = end_node_y

            #find extreme line for comparisons
            ext_start_node = self.conns_array[extreme_line, 1]
            ext_end_node = self.conns_array[extreme_line, 1]
            ext_end_node_y = self.nodes_array[ext_end_node, 1]

            #find actual end_node in this mix
            ext_start_node = end_node_y
            if ext_end_node_y < ext_start_node:
                ext_start_node = ext_end_node_y

            if start_node < ext_start_node:
                extreme_line = line
            
        return extreme_line

    def isPointWithinPoints(self, total_length, points):
        start_point = points[0]
        end_point = points[1]
        if start_point < total_length and end_point > total_length:
            return True
        #this is done in case points have been interchanged
        if end_point < total_length and start_point > total_length:
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

    def selectNearerNodeY(self, total_height, line, in_start_node):
        if total_height < 0:
            return self.selectNearerNodeEndNodeY(total_height, line, in_start_node)

        end_node_1 = self.conns_array[line,0]
        end_node_2 = self.conns_array[line, 1]
        end_node_1_y = self.nodes_array[end_node_1, 1]
        end_node_2_y = self.nodes_array[end_node_2, 1]

        start_node = end_node_1
        end_node = end_node_2
        if end_node_1_y > total_height:
            start_node = end_node_2
            end_node = end_node_1

        start_node_y = self.nodes_array[start_node, 1]

        #module is the distance between nodes
        module = abs(end_node_1_y - end_node_2_y)
        #find portion towards the start node. If this portion is greater than or equal
        #0.5 use end line node and end node other use start node as line node
        percentage_portion = (total_height - start_node_y) / module

        #if portion greater than or equal 50% or the start node is the same as what
        #is passed
        if percentage_portion >= 0.5 or start_node == in_start_node:
            return end_node

        return start_node

    def selectNearerNode(self, total_length, line, in_start_node):
        if total_length < 0:
            return self.selectNearerNodeEndNode(total_length, line, in_start_node)

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

        #if portion greater than or equal 50% or the start node is the same as what
        #is passed
        if percentage_portion >= 0.5 or start_node == in_start_node:
            return end_node

        return start_node

    def selectNearerNodeEndNode(self, total_length, line, in_end_node):
        '''
        This is for getting nearer node for end nodes in the negative direction
        '''
        end_node_1 = self.conns_array[line,0]
        end_node_2 = self.conns_array[line, 1]
        end_node_1_x = self.nodes_array[end_node_1, 0]
        end_node_2_x = self.nodes_array[end_node_2, 0]

        start_node = end_node_1
        end_node = end_node_2
        length = self.getLengthFromStartNode(total_length)
        if end_node_1_x > length:
            start_node = end_node_2
            end_node = end_node_1

        start_node_x = self.nodes_array[start_node, 0]

        #module is the distance between nodes
        module = abs(end_node_1_x - end_node_2_x)
        #find portion towards the start node. If this portion is greater than or equal
        #0.5 use end line node and end node other use start node as line node
        percentage_portion = (length - start_node_x) / module

        #if portion greater than or equal 50% or the start node is the same as what
        #is passed
        if percentage_portion < 0.5 or end_node == in_end_node: 
            return start_node

        return end_node

    def selectNearerNodeEndNodeY(self, total_height, line, in_end_node):
        '''
        This is for getting nearer node for end nodes in the negative direction
        '''
        end_node_1 = self.conns_array[line,0]
        end_node_2 = self.conns_array[line, 1]
        end_node_1_y = self.nodes_array[end_node_1, 1]
        end_node_2_y = self.nodes_array[end_node_2, 1]

        start_node = end_node_1
        end_node = end_node_2
        height = self.getHeightFromTopLeftNode(total_height)
        if end_node_1_y > height:
            start_node = end_node_2
            end_node = end_node_1

        start_node_y = self.nodes_array[start_node, 1]

        #module is the distance between nodes
        module = abs(end_node_1_y - end_node_2_y)
        #find portion towards the start node. If this portion is greater than or equal
        #0.5 use end line node and end node other use start node as line node
        percentage_portion = (height - start_node_y) / module

        #if portion greater than or equal 50% or the start node is the same as what
        #is passed
        if percentage_portion < 0.5 or end_node == in_end_node: 
            return start_node

        return end_node

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

    def getNodesAlongNodeInX(self, node, nodes_along=set()):
        '''
        Function finds nodes a long a node towards a specified direction,
        say y or x directions.
        '''
        nodes_along.add(node)
        right_node = self.getNodeRightNode(node)
        if right_node != None:
            self.getNodesAlongNodeInX(right_node, nodes_along)

        return nodes_along

    def getBottomNodesWithinSelectedPortion(self, start_node, end_node):
        nodes = [start_node, end_node]
        nodes_within_portion = set(nodes)
        bottom_nodes = self.getBottomEdgeNodes()
        for node in bottom_nodes:
            if self.isNodeInBetweenNodes(node, nodes):
                nodes_within_portion.add(node)
        return nodes_within_portion

    def getLeftNodesWithinSelectedPortion(self, start_node, end_node):
        nodes = [start_node, end_node]
        nodes_within_portion = set(nodes)
        left_nodes = self.getLeftEdgeNodes()
        for node in left_nodes:
            if self.isNodeInBetweenNodesY(node, nodes):
                nodes_within_portion.add(node)
        return nodes_within_portion

    def isNodeInBetweenNodes(self, node, nodes):
        point = self.nodes_array[node, 0]
        end_1 = self.nodes_array[nodes[0], 0]
        end_2 = self.nodes_array[nodes[1], 0]

        return self.isPointWithinPoints(point, [end_1, end_2])

    def isNodeInBetweenNodesY(self, node, nodes):
        point = self.nodes_array[node, 1]
        end_1 = self.nodes_array[nodes[0], 1]
        end_2 = self.nodes_array[nodes[1], 1]

        return self.isPointWithinPoints(point, [end_1, end_2])

    def getNodesWithinPortitionY(self, start_node, total_height):
        #1. get portion end node
        #a) get intersected line
        cut_line = self.getIntersectedVerticalLine(total_height)
        #b) get neaer node of line which is end node of portion
        end_node =  self.selectNearerNodeY(total_height, cut_line, start_node)
        portion_end_node = self.getExtremeEndNodeY(end_node, total_height)
        
        #2. get nodes along bottom edge
        portion_left_nodes = \
            self.getLeftNodesWithinSelectedPortion(start_node, end_node)
        #3. get all top nodes for nodes along bottom edge
        portion_nodes = set()
        for node in portion_left_nodes:
            node_right_nodes = self.getNodesAlongNodeInX(node, set())
            portion_nodes.update(node_right_nodes)
        #return these nodes as nodes within portion
        return portion_end_node, portion_nodes

    def getNodesWithinPortition(self, start_node, total_length):
        #1. get portion end node
        #a) get intersected line
        cut_line = self.getIntersectedLine(total_length)
        #b) get neaer node of line which is end node of portion
        end_node =  self.selectNearerNode(total_length, cut_line, start_node)
        portion_end_node = self.getExtremeEndNode(end_node, total_length)
        
        #2. get nodes along bottom edge
        portion_bottom_nodes = \
            self.getBottomNodesWithinSelectedPortion(start_node, end_node)
        #3. get all top nodes for nodes along bottom edge
        portion_nodes = set()
        for node in portion_bottom_nodes:
            node_top_nodes = self.getNodesAlongNodeInY(node, set())
            portion_nodes.update(node_top_nodes)
        #return these nodes as nodes within portion
        return portion_end_node, portion_nodes
    
    def getLinesWithinPortition(self, start_node, total_length, y_direction=False):
        if y_direction:
            end_node, nodes_in_portion = self.getNodesWithinPortitionY(start_node, total_length)
        else:
            end_node, nodes_in_portion = self.getNodesWithinPortition(start_node, total_length)

        lines = set()
        for node in nodes_in_portion:
            node_lines = self.getNodeLines(node)
            for line in node_lines:
                if self.isLineInNodePool(line, nodes_in_portion):
                    lines.add(line)
        return end_node, lines

    def isLineInNodePool(self, line, node_pool):
        line_nodes = self.conns_array[line].tolist()
        for node in line_nodes:
            if node not in node_pool:
                return False
        return True

    def getLineEndNode(self, line):
        '''
        Finds return node number for line node with maximum
        value of x.
        Assumption is node are number from left to right
        '''
        line_nodes = self.conns_array[line].tolist()
        start_node = line_nodes[0]
        end_node = line_nodes[1]

        if self.nodes_array[start_node, 0] > self.nodes_array[end_node, 0]:
            return start_node

        return end_node

    def getExtremeEndNode(self, node, total_length):
        if total_length < 0:
            if node == self.getStartNode():
                return None
        else:
            if node == self.getEndNode():
                return None

        return node

    def getExtremeEndNodeY(self, node, total_length):
        if total_length < 0:
            if node == self.getStartNode():
                return None
        else:
            if node == self.getLeftTopNode():
                return None
        return node

    
    def getRegionNodes(self, region_lines):
        region_nodes = set()
        for line in region_lines:
            start_node = self.conns_array[line, 0]
            end_node = self.conns_array[line, 1]
            region_nodes.add(start_node)
            region_nodes.add(end_node)
        return region_nodes

    def getRandomNode(self, region_nodes):
        return random.choice(list(region_nodes))

    def getRegionBottomEndNode(self, region_lines):
        '''
        return node number in the bottom right corner of the 
        nodes in the passed in region lines
        '''
        #1. find nodes base nodes of region
        corner_nodes = self.getCornerNodes(region_lines).tolist()
        region_bottom_end_nodes  = []

        for node in corner_nodes:
            bottom_node = self.getNodeBottomNode(node, region_lines)
            right_node = self.getNodeRightNode(node, region_lines)
            if bottom_node == None and right_node == None:
                region_bottom_end_nodes.append(node)
        return self.getExtremeLeftNode(region_bottom_end_nodes)

    
    def getTopRightCornerNode(self, region_lines=[]):
        '''
        Returns top right corner node of region nodes
        '''
        corner_nodes = self.getCornerNodes(region_lines).tolist()
        right_edge_corner_nodes = []

        for node in corner_nodes:
            top_node = self.getNodeTopNode(node, region_lines)
            right_node = self.getNodeRightNode(node, region_lines)
            #if no has no top node and node left node, then it is most likely
            #to be in a top left corner
            if top_node == None and right_node == None:
                right_edge_corner_nodes.append(node)
        return self.getExtremeRightNode(right_edge_corner_nodes)

    def getRegionNodeCounts(self, region_conns):
        unique, counts = np.unique(region_conns.flatten(), return_counts=True)
        return dict(zip(unique, counts))

    def getRegionConnsArray(self, region_lines):
        lines = []
        for line in region_lines:
            lines.append(self.conns_array[line].tolist())
        return np.array(lines)

    def getNodesNormalVector(self, nodes, gravity_load=False):
        if gravity_load:
            return (0., 0., 1.)
        points = []
        for node in nodes:
            point = Point3D(self.nodes_array[node].tolist())
            points.append(point)
        
        return Plane(points[0], points[1], points[2]).normal_vector

    def getLoadLine(self, region_lines, height=9000, height_factor=1, gravity_load=False):
        '''
        Returns start and end load load node for loading region
        load line
        '''

        region_nodes = self.getRegionNodes(region_lines)
        random_node = self.getRandomNode(region_nodes)
        corner_nodes = self.getNonCollinearPoints(region_lines)
        normal_vector = self.getNodesNormalVector(corner_nodes, gravity_load)
        point = self.nodes_array[random_node]
        
        distance = (height * height_factor) / normal_vector[2] 

        x = point[0] + normal_vector[0] * distance
        y = point[1] + normal_vector[1] * distance
        z = point[2] + normal_vector[2] * distance
        
        start_node = self.nodes_array[random_node].tolist()

        return [start_node, [x,y,z]]

    def getNonCollinearPoints(self, region_lines):
        start_node = self.getStartNode(region_lines)
        top_top_right_node = self.getTopRightCornerNode(region_lines)
        bottom_right_node = self.getRegionBottomEndNode(region_lines)

        return (start_node, top_top_right_node, bottom_right_node)


        

    
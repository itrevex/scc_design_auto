import sys, pytest
import numpy as np
from unittest.mock import Mock, patch
from dxf.read.dxf_input import DxfInput
from dxf.read.node_locations import NodeLocations
from libs.load_data import LoadData

@pytest.fixture(scope="module")
def locations():
    nodes = [[0.,0.,0.],
        [0.,2.,0.],
        [2.,2.,0.],
        [2.,0.,0.],
        [0.,1.,0.],
        [1.,2.,0.],
        [2.,1.,0.],
        [1.,0.,0.],
        [1.,1.,0.]]
        
    conns = [[4,1],[1,5],[5,2],[2,6],[6,3],[3,7],   
    [7,0],[0,4],[4,8],[8,6],[7,8],[8,5]]
    conns_array = np.array(conns)
    nodes_array = np.array(nodes)
    return NodeLocations(conns_array, nodes_array=nodes_array)

@patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"])
class TestNodeLocations:
    def test_getCornerNodes(self, locations):
        items = locations.getCornerNodes().tolist()
        assert items == [0,1,2,3]

    def test_getCenterNodes(self, locations):
        items = locations.getCenterNodes().tolist()
        assert items == [8] 
        pass

    def test_getEdgeNodes(self, locations):
        items = locations.getEdgeNodes().tolist()
        assert items == [4,5,6,7] 
        
    def test_getStartNode(self, locations):
        assert locations.getStartNode() == 0
        pass


    def test_getNodeLines(self, locations):
        assert locations.getNodeLines(4).tolist() == [0,7,8]
 
    def test_getNodeEndNodes(self, locations):
        assert set(locations.getNodeEndNodes(4)).issubset((0,1,8)) 

    def test_getNodeTopNode(self, locations):
        assert locations.getNodeTopNode(4) == 1

    def test_getNodeTopNode1(self, locations):
        assert locations.getNodeTopNode(0) == 4
    
    def test_getNodeTopNode2(self, locations):
        assert locations.getNodeTopNode(1) == None

    def test_getNodeBottomNode(self, locations):
        assert locations.getNodeBottomNode(4) == 0

    def test_getNodeRightNode(self, locations):
        assert locations.getNodeRightNode(4) == 8
        pass

    def test_getNodeLeftNode(self, locations):
        assert locations.getNodeLeftNode(4) == None
        pass

    def test_center_getNodeLeftNode(self, locations):
        assert locations.getNodeLeftNode(8) == 4
        pass

    def test_getExtremeLeftNode(self, locations):
        nodes = [5,6]
        assert locations.getExtremeLeftNode(nodes) == 5
        pass

    def test_getBottomEdgeNodes(self, locations):
        assert locations.getBottomEdgeNodes().issubset((0, 7, 3))

    def test_getLeftEdgeNodes(self, locations):
        assert locations.getLeftEdgeNodes().issubset((0, 4, 1))

    def test_getBottomEdgeLines(self, locations):
        assert locations.getBottomEdgeLines().issubset((6,5))

    def test_getIntersectedLine(self, locations):
        assert locations.getIntersectedLine(0.45) == 6
    
    def test_getIntersectedLine_2(self, locations):
        assert locations.getIntersectedLine(1.45) == 5

    def test_is_pointWithinPoints(self, locations):
        points = [1.,0.]
        assert locations.isPointWithinPoints(0.45, points) == True

    def test_is_not_pointWithinPoints(self, locations):
        points = [0.,1.]
        assert locations.isPointWithinPoints(1.1, points) == False

    def test_is_pointLeftToThePoints(self, locations):
        points = [1., 0.]
        assert locations.isPointLeftToThePoints(1.1, points) == True

    def test_is_not_pointLeftToThePoints(self, locations):
        points = [0., 1.]
        assert locations.isPointLeftToThePoints(-0.1, points) == False

    def test_selectNearerNode(self, locations):
        point = 0.45
        line = 6
        assert locations.selectNearerNode(point, line, 0) == 7

    def test_selectNearerNode2(self, locations):
        point = 0.5
        line = 6
        assert locations.selectNearerNode(point, line, 0) == 7

    def test_selectNearerNode3(self, locations):
        point = 1.5
        line = 5
        assert locations.selectNearerNode(point, line, 0) == 3

    def test_selectNearerNode4(self, locations):
        point = 1.45
        line = 5
        assert locations.selectNearerNode(point, line, 0) == 7

    def test_getNodesAlongNodeInY(self, locations):
        #call method with an empty set to reintiate the nodes along set
        assert locations.getNodesAlongNodeInY(7, set()).issubset((7,8,5))

    def test_getNodesAlongNodeInY1(self, locations):
        assert locations.getNodesAlongNodeInY(3, set()).issubset((3,6,2))

    def test_getNodesAlongNodeInY2(self, locations):
        assert locations.getNodesAlongNodeInY(0, set()).issubset((0,4,1))

    def test_bottom_nodes_with_in_between_selected_portion(self, locations):
        portion_start_node = 0
        portion_end_node = 3
        assert locations.getBottomNodesWithinSelectedPortion(portion_start_node, portion_end_node)\
            .issubset((0,7,3))

    def test_bottom_nodes_with_in_between_selected_portion1(self, locations):
        portion_start_node = 3
        portion_end_node = 0
        assert locations.getBottomNodesWithinSelectedPortion(portion_start_node, portion_end_node)\
            .issubset((0,7,3))

    def test_bottom_nodes_with_in_between_selected_portion2(self, locations):
        portion_start_node = 3
        portion_end_node = 7
        assert locations.getBottomNodesWithinSelectedPortion(portion_start_node, portion_end_node)\
            .issubset((7,3))

    def test_node_is_in_between_nodes(self, locations):
        node = 7
        nodes = [0,3]
        assert locations.isNodeInBetweenNodes(node, nodes) == True

    def test_node_is_in_between_nodes1(self, locations):
        node = 7
        nodes = [3,0]
        assert locations.isNodeInBetweenNodes(node, nodes) == True

    def test_node_is_in_between_nodes2(self, locations):
        node = 7
        nodes = [1,0]
        assert locations.isNodeInBetweenNodes(node, nodes) == False

    def test_nodes_for_selection_portition(self, locations):
        nodes_in_portion = {0,4,1,7,8,5}
        start_node = 0
        length = 0.55
        calculated_nodes = locations.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)
    
    def test_nodes_for_selection_portition1(self, locations):
        nodes_in_portion = {0,4,1,7,8,5}
        start_node = 0
        length = 0.25
        calculated_nodes = locations.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)

    def test_nodes_for_selection_portition2(self, locations):
        nodes_in_portion = {2,6,3,7,8,5}
        start_node = 0
        length = 1.6
        calculated_nodes = locations.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)

    def test_lines_for_selection_portion(self, locations):
        lines_in_portion = {7,0,1,11,10,6,8}
        start_node = 0
        length = 0.6
        calculated_lines = locations.getLinesWithinPortition(start_node, length)
        assert calculated_lines.issubset(lines_in_portion)

    def test_line_is_within_node_pool(self, locations):
        node_pool = {0,4,1,5,8,7}
        line = 9
        assert not locations.isLineInNodePool(line, node_pool)

    def test_line_is_within_node_pool2(self, locations):
        node_pool = {0,4,1,5,8,7}
        line = 8
        assert locations.isLineInNodePool(line, node_pool)

    def test_line_has_no_right_end_line(self, locations):
        lines = locations.getBottomEdgeLines()
        assert locations.extremeBottomLine(lines) == 5

    def test_find_end_node_within_region_lines(self, locations):
        region_lines = {7,0,1,11,10,6,8}
        assert locations.getRegionBottomEndNode(region_lines) == 7

    def test_find_end_node_within_region_lines1(self, locations):
        region_lines = {7,0,1,11,10,6,8,5}
        assert locations.getRegionBottomEndNode(region_lines) == 3

    def test_find_end_node_line(self, locations):
        line = 5
        assert locations.getLineEndNode(line) == 3
    
    def test_find_end_node_line1(self, locations):
        line = 1
        assert locations.getLineEndNode(line) == 5

    def test_gets_right_end_node(self, locations):
        assert locations.getEndNode() == 3

    def test_get_extreme_right_corner_node(self, locations):
        corneer_nodes = [0,7,3]
        assert locations.getExtremeRightNode(corneer_nodes) == 3

    def test_returns_right_cutline_for_negative_total_length(self, locations):
        assert locations.getIntersectedLine(-0.45) == 5

    
    

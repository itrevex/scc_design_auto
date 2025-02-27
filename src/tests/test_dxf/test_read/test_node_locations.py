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

@pytest.fixture(scope="module")
def locations_dxf():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"]):
        app_data = LoadData()
        dxfInput = DxfInput(app_data)
        return NodeLocations(dxfInput.conns, nodes_array=dxfInput.nodes)


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

    def test_getIntersectedLine1(self, locations_dxf):
        assert locations_dxf.getIntersectedLine(-28800.) == 12
    
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
        end_node, calculated_nodes = locations.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)
        assert end_node == 7
    
    def test_nodes_for_selection_portition1(self, locations):
        nodes_in_portion = {0,4,1,7,8,5}
        start_node = 0
        length = 0.25
        end_node, calculated_nodes = locations.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)
        assert end_node == 7

    def test_nodes_for_selection_portition2(self, locations):
        nodes_in_portion = {2,6,3,7,8,5}
        start_node = 0
        length = 1.6
        end_node, calculated_nodes = locations.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)
        assert end_node == None

    def test_lines_for_selection_portion(self, locations):
        lines_in_portion = {7,0,1,11,10,6,8}
        start_node = 0
        length = 0.6
        end_node, calculated_lines = locations.getLinesWithinPortition(start_node, length)
        assert calculated_lines.issubset(lines_in_portion)
        assert end_node == 7

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
        assert locations.extremeRightBottomLine(lines) == 5

    def test_find_end_node_within_region_lines(self, locations):
        region_lines = {7,0,1,11,10,6,8}
        assert locations.getRegionBottomEndNode(region_lines) == 7

    def test_find_end_node_within_region_lines1(self, locations):
        region_lines = {7,0,1,11,10,6,8,5,4}
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

    def test_get_length_from_start_point(self, locations):
        total_length = -0.45
        assert locations.getLengthFromStartNode(total_length) == 1.55

    def test_get_length_from_start_point1(self, locations_dxf):
        total_length = -28800.
        assert locations_dxf.getLengthFromStartNode(total_length) <= 0

    def test_get_length_from_top_left_node(self, locations):
        total_length = -0.45
        assert locations.getHeightFromTopLeftNode(total_length) == 1.55

    def test_get_end_node_in_y_direction(self, locations):
        assert locations.getLeftTopNode() == 1

    def test_get_nearer_node_for_end_node(self, locations):
        point = -0.5
        line = 5
        assert locations.selectNearerNodeEndNode(point, line, 3) == 7

    def test_get_nearer_node_for_end_node1(self, locations):
        point = -0.45
        line = 5
        assert locations.selectNearerNodeEndNode(point, line, 3) == 7

    def test_get_nearer_node_for_end_node2(self, locations):
        point = -1.45
        line = 6
        assert locations.selectNearerNodeEndNode(point, line, 3) == 7

    def test_get_nearer_node_for_end_node3(self, locations):
        point = -1.8
        line = 6
        assert locations.selectNearerNodeEndNode(point, line, 3) == 0

    def test_get_nearer_node_for_end_node4(self, locations):
        point = -1.8
        line = 6
        assert locations.selectNearerNode(point, line, 3) == 0

    def test_returns_none_for_extreme_nodes(self, locations):
        assert locations.getExtremeEndNode(7, 1.1) == 7

    def test_returns_none_for_extreme_nodes1(self, locations):
        assert locations.getExtremeEndNode(0, -1.55) == None

    def test_returns_none_for_extreme_nodes2(self, locations):
        assert locations.getExtremeEndNode(3, 1.5) == None

    def test_nodes_for_selection_portition3(self, locations_dxf):
        nodes_in_portion = {0,20,40,60,80,100}
        start_node = 100
        length = -28800.
        end_node, calculated_nodes = locations_dxf.getNodesWithinPortition(start_node, length)
        assert nodes_in_portion.issubset(calculated_nodes)
        assert end_node == None

    def test_returns_extreme_left_bottom_lines(self, locations_dxf):
        lines = locations_dxf.getBottomEdgeLines()
        assert locations_dxf.extremeLeftBottomLine(lines) == 12

    def test_get_edge_lines(self, locations):
        assert locations.getLeftEdgeLines().issubset([0,7])

    def test_get_line_at_the_bottom_of_the_left_lines(self, locations):
        lines = (0,7)
        assert locations.extremeBottomLeftLine(lines) == 7

    def test_get_line_at_the_top_of_the_left_lines(self, locations):
        lines = (0,7)
        assert locations.extremeTopLeftLine(lines) == 0

    def test_get_right_y_direction_intersected_line(self, locations):
        assert locations.getIntersectedVerticalLine(-0.45) == 0

    def test_get_right_y_direction_intersected_line1(self, locations):
        assert locations.getIntersectedVerticalLine(0.45) == 7

    def test_returns_correct_nearer_node_in_y_direction(self, locations):
        assert locations.selectNearerNodeY(1.2, 0, 0) == 4

    def test_returns_correct_nearer_node_in_y_direction1(self, locations):
        assert locations.selectNearerNodeY(1.6, 0, 0) == 1

    def test_selects_correct_nearer_end_node_in_y(self, locations):
        assert locations.selectNearerNodeEndNodeY(-1.2, 0, 0) == 1

    def test_get_extreme_node_in_y_direction(self, locations):
        assert locations.getExtremeEndNodeY(1, 1.6) == None

    def test_get_extreme_node_in_y_direction1(self, locations):
        assert locations.getExtremeEndNodeY(4, 1.2) == 4

    def test_get_extreme_node_in_y_direction2(self, locations):
        assert locations.getExtremeEndNodeY(0, -1.6) == None

    def test_gets_correct_left_nodes_within_selected_portition(self, locations):
        portion_start_node = 1
        portion_end_node = 0
        assert locations.getLeftNodesWithinSelectedPortion(portion_start_node, portion_end_node)\
            .issubset((0,4,1))

    def test_is_node_between_nodes_in_y_direction(self, locations):
        node = 4
        nodes = [0,1]
        assert locations.isNodeInBetweenNodesY(node, nodes) == True

    def test_gets_correct_right_nodes_of_a_single_left_edge_node(self, locations):
        assert locations.getNodesAlongNodeInX(4, set()).issubset((4,8,6))

    def test_get_right_y_direction_intersected_line2(self, locations_dxf):
        assert locations_dxf.getIntersectedVerticalLine(38000) == 474

    def test_get_length_from_top_left_node1(self, locations_dxf):
        total_length = 38000
        assert locations_dxf.getHeightFromTopLeftNode(total_length) == 38000

    def test_get_length_from_top_left_node2(self, locations_dxf):
        total_length = -16000
        assert locations_dxf.getHeightFromTopLeftNode(total_length) == 22000

    def test_is_pointWithinPoints2(self, locations_dxf):
        points = [0.,2000.]
        assert locations_dxf.isPointWithinPoints(38000., points) == False

    def test_is_pointWithinPoints3(self, locations_dxf):
        points = [36000.,38000.]
        assert locations_dxf.isPointWithinPoints(38000., points) == False

    def test_get_line_at_the_top_of_the_left_lines2(self, locations_dxf):
        lines = (240,266,279,474)
        assert locations_dxf.extremeTopLeftLine(lines) == 474

    def test_get_nodes_within_line_group(self, locations):
        region_lines = (6,5,8)
        assert locations.getRegionNodes(region_lines).issubset((0,3,7,8,4))

    def test_get_random_node_with_in_nodes(self, locations):
        region_lines = (6,5,8)
        region_nodes = locations.getRegionNodes(region_lines)
        assert locations.getRandomNode(region_nodes) in [0,3,7,8,4]

    def test_gets_top_right_corner_node_of_region(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        assert locations.getTopRightCornerNode(region_lines) == 5
        assert locations.getTopRightCornerNode() == 2

    def test_get_region_node_counts(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        region_conns = locations.getRegionConnsArray(region_lines)
        region_corner_nodes = {
            0:2, 4:3,1:2,5:2,8:3,7:2
        }
        assert locations.getRegionNodeCounts(region_conns) == region_corner_nodes

    def test_get_region_corner_nodes(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        assert locations.getCornerNodes(region_lines).tolist() == [0,1,5,7]

    def test_get_correct_portion_conns_array(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        region_conns_array = locations.getRegionConnsArray(region_lines)
        assert region_conns_array[3].tolist() == [7,8]
        assert list(region_conns_array.shape)== [7,2]

    def test_return_correct_end_node_of_region_lines(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        assert locations.getNodeEndNodes(8, region_lines) == [4,7,5]

    def test_get_right_portion_node_lines(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        assert locations.getPortoinNodeLines(8, region_lines) == [8,10,11]

    def test_get_region_top_node_for_region_node(self, locations):
        region_lines = (10,6,7, 8)
        assert locations.getNodeTopNode(8, region_lines) == None
        assert locations.getNodeTopNode(8) == 5

    def test_get_region_right_node_for_region_node(self, locations):
        region_lines = (0,1,11,10,6,7, 8)
        assert locations.getNodeRightNode(8, region_lines) == None

    def test_get_region_start_node(self, locations):
        region_lines = (0,1,11,8)
        assert locations.getStartNode(region_lines) == 4
    
    def test_returns_correct_normal_vector(self, locations):
        nodes = [0,7,5]
        assert locations.getNodesNormalVector(nodes) == (0,0,2)

    def test_returns_correct_normal_vector1(self, locations):
        nodes = [0,7,5]
        assert locations.getNodesNormalVector(nodes, True) == (0.,0.,1.)

    def test_calculates_correct_coordinate_for_normal_vector_from_node(self, locations):
        with patch.object(NodeLocations, 'getRandomNode') as mock_random,\
            patch.object(NodeLocations, 'getRegionNodes') as mock_nodes:
            mock_random.side_effect = lambda nodes: 8 
            mock_nodes.return_value = lambda lines: [0,7,5]
            assert locations.getLoadLine((0,1,11,8), 3.)[1] == [1.,1.,3.]

    def test_calculates_correct_coordinate_for_normal_vector_from_node1(self, locations_dxf):
        region_lines = locations_dxf.getLinesWithinPortition(0, 3600.)[1]
        
        with patch.object(NodeLocations, 'getRandomNode') as mock_random:
            mock_random.side_effect = lambda nodes: 14
            assert locations_dxf.getLoadLine(region_lines)[1][1] == 28000.0
            assert locations_dxf.getLoadLine(region_lines)[0][2] == 0.0

    def test_gets_right_non_collinear_corner_points(self, locations):
        region_lines = (0,1,11,8)
        assert locations.getNonCollinearPoints(region_lines) == (4,5,8)

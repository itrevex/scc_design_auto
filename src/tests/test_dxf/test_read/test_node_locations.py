import sys, pytest
import numpy as np
from unittest.mock import Mock, patch
from dxf.read.dxf_input import DxfInput
from dxf.read.node_locations import NodeLocations
from libs.load_data import LoadData

@pytest.fixture(scope="module")
def nodes():
    return [[0.,0.,0.],
        [0.,2.,0.],
        [2.,2.,0.],
        [2.,0.,0.],
        [0.,1.,0.],
        [1.,2.,0.],
        [2.,1.,0.],
        [1.,0.,0.],
        [1.,1.,0.]]
        
@pytest.fixture(scope="module")
def conns():
    return [[4,1],[1,5],[5,2],[2,6],[6,3],[3,7],   
    [7,0],[0,4],[4,8],[8,6],[7,8],[8,5]]

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
 
    def test_getOppositeEndNodes(self, locations):
        nodes = locations.getNodeLines(4).tolist()
        assert set(locations.getOppositeEndNodes(4, nodes)).issubset((0,1,8)) 

    def test_getNodeTopNode(self, locations):
        assert locations.getNodeTopNode(4, (0,1,8)) == 1

    def test_getNodeBottomNode(self, locations):
        assert locations.getNodeBottomNode(4, (0,1,8)) == 0

    def test_getNodeRightNode(self, locations):
        assert locations.getNodeRightNode(4, (0,1,8)) == 8
        pass

    def test_getNodeLeftNode(self, locations):
        assert locations.getNodeLeftNode(4, (0,1,8)) == None
        pass

    def test_center_getNodeLeftNode(self, locations):
        assert locations.getNodeLeftNode(8, (4,5,6,7)) == 4
        pass

    def test_getExtremeLeftNode(self, locations):
        nodes = [5,6]
        assert locations.getExtremeLeftNode(nodes) == 5
        pass

    def test_getBottomEdgeNodes(self, locations):
        assert locations.getBottomEdgeNodes().issubset((0, 7, 3))

    def test_getLeftEdgeNodes(self, locations):
        assert locations.getLeftEdgeNodes().issubset((0, 4, 1))

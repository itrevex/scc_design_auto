import sys
import numpy as np
from unittest.mock import Mock, patch
from dxf.read.dxf_input import DxfInput
from dxf.read.node_locations import NodeLocations
from libs.load_data import LoadData

@patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"])
class TestNodeLocations:
    def setUpClass(self):
        conns = [[5,2],[2,6],[6,3],[3,7],[7,4],[4,8],   
            [8,1],[1,5],[5,9],[9,7],[8,9],[9,6]]
        self.conns_array = np.array(conns)

    def test_getCornerNodes(self):
        #corner nodes have only 2 nodes sharing the meeting point
        conns = [[5,2],[2,6],[6,3],[3,7],[7,4],[4,8],   
            [8,1],[1,5],[5,9],[9,7],[8,9],[9,6]]
        conns_array = np.array(conns)
        items = NodeLocations(conns_array).getCornerNodes().tolist()
        assert items == [1,2,3,4]

    def test_getCenterNodes(self):
        conns = [[5,2],[2,6],[6,3],[3,7],[7,4],[4,8],   
            [8,1],[1,5],[5,9],[9,7],[8,9],[9,6]]
        conns_array = np.array(conns)

        items = NodeLocations(conns_array).getCenterNodes().tolist()
        assert items == [9] 
        pass

    def test_getEdgeNodes(self):
        conns = [[5,2],[2,6],[6,3],[3,7],[7,4],[4,8],   
            [8,1],[1,5],[5,9],[9,7],[8,9],[9,6]]
        conns_array = np.array(conns)

        items = NodeLocations(conns_array).getEdgeNodes().tolist()
        assert items == [5,6,7,8] 
        pass
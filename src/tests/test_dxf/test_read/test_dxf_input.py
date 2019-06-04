import sys
import numpy as np
from unittest.mock import Mock, patch
from dxf.read.dxf_input import DxfInput
from libs.load_data import LoadData

@patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"])
class TestDxfInput:
    def setUpClass(self):
        self.app_data = LoadData()

    def test_inList(self):
        list1 = [1,2]
        list2 = [2,1]
        assert DxfInput(LoadData()).equalLine(list1, list2) == True
        list1 = [1,2]
        list2 = [1,1]
        assert DxfInput(LoadData()).equalLine(list2, list1) == False
        pass
    
    def test_getNodeIndex(self):
        nodes = np.array([[24000.,30000.,0.],
                [24000.,32000.,0.],
                [24000.,34000.,0.],
                [24000.,36000.,0.],
                [24000.,38000.,0.]])
        node = (23999.99999999998, 38000.0, 0.0)

        assert DxfInput(LoadData()).getNodeIndex(node, nodes) == 4

    def test_equalNode(self):
        point1 = (23999.99999999998, 38000.0, 0.0)
        point2 = [24000.,38000.,0.]
        assert DxfInput(LoadData()).equalNode(point1, point2) == True

    def test_removeDuplicates(self):
        conns = [[2,1],[1,1],[1,2],[3,1],[1,3], [1,1], [2,1]]
        new_conns = [[2,1],[1,1],[3,1]]
        assert DxfInput(LoadData()).removeDuplicates(conns) == new_conns
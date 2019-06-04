import sys
from unittest.mock import Mock, patch
from dxf.read.dxf_input import DxfInput
from libs.load_data import LoadData

@patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"])
class TestDxfInput:

    def test_inList(self):
        list1 = [1,2]
        list2 = [2,1]
        # DxfInput(app_data).inList(list1, list2)
        assert DxfInput(LoadData()).inList(list1, list2) == True
        pass
from src.dxf.read.dxf_input import DxfInput
from src.libs.load_data import LoadData
from unittest.mock import Mock

app_data = LoadData()

class TestDxfInput:
    def test_inList(self):
        list1 = [1,2]
        list2 = [2,1]
        assert DxfInput(app_data).inList(list1, list2) == True
        pass
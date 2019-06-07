import sys, pytest
from unittest.mock import patch, Mock
from dxf.write.write_loading_dxf import LoadingsDxf
from libs.load_data import LoadData

@pytest.fixture(scope="module")
def app_data():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"]):
        return LoadData()

@pytest.fixture(scope="module")    
def mock_dwg():
    with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock:
        return mock
class TestLoadingDxf():

    def test_saveas_loading_dxf_file_called(self, app_data, mock_dwg):
        mock_saveas = Mock()
        type(mock_dwg.return_value).saveas = mock_saveas
        LoadingsDxf(app_data)
        mock_saveas.assert_called_once()
        assert mock_saveas.call_count == 1

    def test_gets_right_number_of_loading_region_lines(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        lines = loading_dxf.getLoadingRegionLines(7154.)
        assert len(lines) == 175

    def test_gets_right_number_of_loading_region_lines1(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        lines = loading_dxf.getLoadingRegionLines(6354.)
        assert len(lines) == 136

    def test_gets_right_number_of_loading_region_lines2(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        lines = loading_dxf.getLoadingRegionLines(1000.)
        assert len(lines) == 58
import sys, pytest
from unittest.mock import patch, Mock
from dxf.write.write_loading_dxf import LoadingsDxf
from libs.load_data import LoadData
from gen_desc.gen_desc import GenDesc

@pytest.fixture(scope="module")
def app_data():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"]):
        return LoadData()

@pytest.fixture(scope="module")
def gen_desc():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"]):
        return GenDesc(LoadData())

@pytest.fixture(scope="module")
def gen_desc_open():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project_open.json"]):
        return GenDesc(LoadData())

@pytest.fixture(scope="module")    
def mock_dwg():
    with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock:
        return mock

class TestLoadingDxf():

    def test_saveas_loading_dxf_file_called(self, app_data, gen_desc):
        with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock_dwg:
            mock_saveas = Mock()
            type(mock_dwg.return_value).saveas = mock_saveas
            LoadingsDxf(app_data, gen_desc).saveDxf()
            mock_saveas.assert_called_once()

    def test_gets_right_number_of_loading_region_lines(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(7154.)
        assert len(lines) == 175
        assert end_node == 80

    def test_gets_right_number_of_loading_region_lines1(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(6354.)
        assert len(lines) == 136
        assert end_node == 60

    def test_gets_right_number_of_loading_region_lines2(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(1000.)
        assert len(lines) == 58
        assert end_node == 20

    def test_adds_lines_to_modelspace(self, app_data):
        with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock_dwg:
            mock_msp = Mock()
            type(mock_dwg.return_value).modelspace = mock_msp 
            mock_add_line = Mock()
            type(mock_msp.return_value).add_line = mock_add_line
            loading_dxf = LoadingsDxf(app_data)
            region_lines = loading_dxf.getLoadingRegionLines(6354.)[1]
            loading_dxf.createLines(region_lines, 804)
            mock_msp.assert_called()
            assert mock_add_line.call_count == 136

    def test_get_x_regions_for_drawing_closed_structure(self, app_data, gen_desc):
        loadings_dxf = LoadingsDxf(app_data, gen_desc)
        regions = {
            804: 3600,
            805: 7200,
            806: 14400,
            807: 28800,
            808: -3600,
            809: -7200,
            810: -14400,
            811: -28800
        }
        assert loadings_dxf.getLoadingRegions() == regions

    def test_get_x_regions_for_drawing_open_structure(self, app_data, gen_desc_open):
        
        loadings_dxf = LoadingsDxf(app_data, gen_desc_open)
        regions = {
            804: 7200.,
            805: 7200.,
            806: 14400.,
            807: 14400.,
            808: 28800.,
            809: 28800.,
            810: -7200.,
            811: -7200.,
            812: -14400.,
            813: -14400.,
            814: -28800.,
            815: -28800.
        }
    
        assert loadings_dxf.getLoadingRegions() == regions

    def test_loading_region_lines_for_negative_direction(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(-7200.)
        assert len(lines) == 175
        assert end_node == 160


    def test_loading_region_lines_for_negative_direction1(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(-14400.)
        assert len(lines) == 292
        assert end_node == 100

    def test_loading_region_lines_for_negative_direction2(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(-14400., 160)
        assert len(lines) == 136
        assert end_node == 100

    def test_loading_region_lines_for_negative_direction3(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(14400., 80)
        assert len(lines) == 136
        assert end_node == 140

    def test_loading_region_lines_for_negative_direction4(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(28800.)
        assert len(lines) == 487
        assert end_node == None

    def test_loading_region_lines_for_negative_direction5(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(-28800., 100)
        assert len(lines) == 214
        assert end_node == None

    def test_create_line_called_for_all_loaded_regions(self, app_data, gen_desc):
        with patch.object(LoadingsDxf, 'createLines') as mock_create_lines:
            loadings_dxf = LoadingsDxf(app_data, gen_desc)
            loadings_dxf.writeLoadingLines()
            assert mock_create_lines.call_count == 8

    def test_calls_create_layers(self, app_data, gen_desc):
        with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock_dwg:
            mock_layers = Mock()
            type(mock_dwg.return_value).layers = mock_layers
            mock_new = Mock()
            type(mock_layers.return_value).new = mock_new
            LoadingsDxf(app_data, gen_desc).createLayers()
            mock_new.assert_called()
    
    def test_position_of_last_portion_in_negative_direction(self, app_data, gen_desc):
        LoadingsDxf(app_data, gen_desc).writeLoadingLines()


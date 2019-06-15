import sys, pytest
from unittest.mock import patch, Mock, PropertyMock
from dxf.write.write_loading_dxf import LoadingsDxf
from libs.load_data import LoadData
from wind_design.wind_design import WindDesign

@pytest.fixture(scope="module")
def app_data():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"]):
        return LoadData()

@pytest.fixture(scope="module")
def wind_design():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project.json"]):
        return WindDesign(LoadData())

@pytest.fixture(scope="module")
def wind_design_open():
    with patch.object(sys, 'argv', ["input", "./tests/mocks/project_open.json"]):
        return WindDesign(LoadData())

@pytest.fixture(scope="module")    
def mock_dwg():
    with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock:
        return mock

class TestLoadingDxf():

    def test_saveas_loading_dxf_file_called(self, app_data, wind_design):
        with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock_dwg:
            mock_saveas = Mock()
            type(mock_dwg.return_value).saveas = mock_saveas
            LoadingsDxf(app_data, wind_design).saveDxf()
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

    def test_get_x_regions_for_drawing_closed_structure(self, app_data, wind_design):
        loadings_dxf = LoadingsDxf(app_data, wind_design)
        regions = [
            [804, 3600., '-0.6867'],
            [805, 7200., '-0.6867'],
            [806, 14400., '-0.3815'],
            [807, 24000., '-0.2289'],
            [808, -3600., '-0.6867'],
            [809, -7200., '-0.6867'],
            [810, -14400., '-0.3815'],
            [811, -24000., '-0.2289']
        ]
        assert loadings_dxf.getLoadingRegions() == regions

    def test_get_x_regions_for_drawing_open_structure(self, app_data, wind_design_open):
        
        loadings_dxf = LoadingsDxf(app_data, wind_design_open)
        regions = [
            [804, 7200., '-0.6104'],
            [805, 7200., '0.6104'],
            [806, 14400., '-0.4578'],
            [807, 14400., '0.3815'],
            [808, 24000., '-0.2289'],
            [809, 24000., '0.2289'],
            [810, -7200., '-0.6104'],
            [811, -7200., '0.6104'],
            [812, -14400., '-0.4578'],
            [813, -14400., '0.3815'],
            [814, -24000., '-0.2289'],
            [815, -24000., '0.2289']
        ]
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
        end_node, lines = loading_dxf.getLoadingRegionLines(24000.)
        assert len(lines) == 487
        assert end_node == None

    def test_loading_region_lines_for_negative_direction5(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(-24000., 100)
        assert len(lines) == 214
        assert end_node == None

    def test_create_line_method_called_for_all_loaded_regions(self, app_data, wind_design):
        with patch.object(LoadingsDxf, 'createLines') as mock_create_lines, \
            patch.object(LoadingsDxf, 'createLine') as mock_create_line:
            loadings_dxf = LoadingsDxf(app_data, wind_design)
            loadings_dxf.createLoadingRegionLines()
            assert mock_create_lines.call_count == 19
            assert mock_create_line.call_count == 19

    def test_create_proper_loading_regions(self, app_data, wind_design_open):
        loadings_dxf = LoadingsDxf(app_data, wind_design_open)
        start_nodes = [None,None,80,80,140,140,None,None, 160, 160, 100, 100]
        loading_regions = loadings_dxf.getLoadingRegionContent()
        calc_loadings_start_nodes = [x[1] for x in loading_regions]
        assert start_nodes == calc_loadings_start_nodes

    def test_create_proper_loading_regions_closed(self, app_data, wind_design):
        loadings_dxf = LoadingsDxf(app_data, wind_design)
        start_nodes = [None, 40, 80, 140, None, 200, 160, 100]
        loading_regions = loadings_dxf.getLoadingRegionContent()
        calc_loadings_start_nodes = [x[1] for x in loading_regions]
        assert start_nodes == calc_loadings_start_nodes

    def test_calls_create_layers(self, app_data, wind_design):
        with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock_dwg:
            mock_layers = PropertyMock()
            type(mock_dwg.return_value).layers = mock_layers
            mock_new = Mock()
            type(mock_layers.return_value).new = mock_new
            LoadingsDxf(app_data, wind_design).createLayers()
            mock_new.assert_called()

    def test_gets_right_start_node_for_zone(self, app_data, wind_design_open):
        loadings_dxf = LoadingsDxf(app_data, wind_design_open)
        assert loadings_dxf.getNextNode(7200., 7200., None, 80) == None

    def test_gets_right_start_node_for_zone1(self, app_data, wind_design_open):
        loadings_dxf = LoadingsDxf(app_data, wind_design_open)
        assert loadings_dxf.getNextNode(14400., 7200., None, 80) == 80

    def test_get_y_direction_loading_regions(self, app_data, wind_design):
        loadings_dxf = LoadingsDxf(app_data, wind_design)
        regions = [
            [812, 3600, '-0.6867'],
            [813, 7200, '-0.6867'],
            [814, 14400, '-0.3815'],
            [815, 38000, '-0.2289'],
            [816, -3600, '-0.6867'],
            [817, -7200, '-0.6867'],
            [818, -14400, '-0.3815'],
            [819, -38000, '-0.2289']
        ]
        assert loadings_dxf.getLoadingRegions(True) == regions

    def test_get_y_direction_loading_regions1(self, app_data, wind_design_open):
        loadings_dxf = LoadingsDxf(app_data, wind_design_open)
        regions = [
            [816, 19000., '0.9156'],
            [817, 19000., '-0.8393'],
            [818, 38000., '0.2289'],
            [819, 38000., '-0.0763'],
            [820, -19000., '0.9156'],
            [821, -19000., '-0.8393'],
            [822, -38000., '0.2289'],
            [823, -38000., '-0.0763']
        ]
        assert loadings_dxf.getLoadingRegions(True) == regions

    def test_loading_region_lines_for_y_negative_direction(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(19000., y_direction=True)
        assert len(lines) == 262
        assert end_node == 10
        
    def test_loading_region_lines_for_y_negative_direction1(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(38000., y_direction=True)
        assert len(lines) == 487
        assert end_node == None

    def test_loading_region_lines_for_y_negative_direction2(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        end_node, lines = loading_dxf.getLoadingRegionLines(38000., 10, True)
        assert len(lines) == 237
        assert end_node == None

    def test_gets_right_height_factor(self, app_data):
        loading_dxf = LoadingsDxf(app_data)
        assert loading_dxf.getHeightFactor(-0.8698) ==  1
        assert loading_dxf.getHeightFactor(0.8690) ==  -1

    def test_writes_load_case_load_at_end_of_load_line(self, app_data):
        with patch('dxf.write.write_loading_dxf.ezdxf.new') as mock_dwg:
            mock_msp = Mock()
            type(mock_dwg.return_value).modelspace = mock_msp 
            mock_add_text = Mock()
            type(mock_msp.return_value).add_text = mock_add_text
            loading_dxf = LoadingsDxf(app_data)
            point = (0,3,4)
            load = -1.0565
            loading_dxf.addLoading(load, point, 804)
            mock_msp.assert_called()
            assert mock_add_text.call_count == 1

    def test_get_correct_and_load_for_dead_service_and_live_loads(self, app_data, wind_design):
        loadings_dxf = LoadingsDxf(app_data, wind_design)
        gravity_loads = [
            [801, 0., '0.10'],
            [802, 0., '1.30'],
            [803, 0., '0.45']
        ]
        assert loadings_dxf.getGravityLoads() == gravity_loads

    def test_gets_right_number_region_nodes_for_gravity_loads(self, app_data, wind_design):
        loadings_dxf = LoadingsDxf(app_data, wind_design)
        start_node, lines = loadings_dxf.getLoadingRegionLines(0)
        assert len(lines) == 487
        assert start_node == None
        



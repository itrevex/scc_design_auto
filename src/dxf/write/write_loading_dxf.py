import ezdxf
from dxf.read.dxf_input import DxfInput
from dxf.read.node_locations import NodeLocations

class LoadingsDxf():
    def __init__(self, app_data):
        self.dwg = ezdxf.new('R2010')
        self.app_data = app_data
        self.msp = self.dwg.modelspace()
        self.dxfInput = DxfInput(self.app_data)
        print("Creating loadings dxf . . .")
        self.locations = NodeLocations(self.dxfInput.conns, 
            nodes_array=self.dxfInput.nodes)
        self.saveDxf()

    def createLines(self, region_lines):
        for line in region_lines:
            line_nodes = self.dxfInput.conns[line].tolist()
            start_node = self.dxfInput.nodes[line_nodes[0]].tolist()
            end_node =self.dxfInput. nodes[line_nodes[1]].tolist()
            self.msp.add_line(start_node, end_node)

        #todo - get extreme corner node for region lines

    def getLoadingRegionLines(self, total_length, start_node=None):
        if start_node == None:
            start_node = self.locations.getStartNode()
        region_lines = self.locations.getLinesWithinPortition(start_node, total_length)

        return region_lines
        

    def saveDxf(self):
        path = self.app_data.getRootOutPutPath('LOADINGS.DXF')
        self.dwg.saveas(path)

    
import ezdxf
from dxf.read.dxf_input import DxfInput
from dxf.read.node_locations import NodeLocations

class LoadingsDxf():
    def __init__(self, app_data, *arg):
        self.dwg = ezdxf.new('R2010')
        self.app_data = app_data
        self.msp = self.dwg.modelspace()
        self.dxfInput = DxfInput(self.app_data)
        try:
            self.gen_desc = arg[0]
        except(IndexError):
            self.gen_desc = None
        
        print("Creating loadings dxf . . .")
        self.locations = NodeLocations(self.dxfInput.conns, 
            nodes_array=self.dxfInput.nodes)
        self.createLayers()

    def writeLoadingLines(self):
        regions = self.getLoadingRegions()
        start_node = None
        for zone, length in regions.items():
            start_node, region_lines = self.getLoadingRegionLines(length, start_node=start_node)
            self.createLines(region_lines, zone)
            

    def createLines(self, region_lines, layer):
        for line in region_lines:
            line_nodes = self.dxfInput.conns[line].tolist()
            start_node = self.dxfInput.nodes[line_nodes[0]].tolist()
            end_node =self.dxfInput. nodes[line_nodes[1]].tolist()
            self.msp.add_line(start_node, end_node, dxfattribs={'layer': str(layer)})

        #todo - get extreme corner node for region lines

    def getLoadingRegionLines(self, total_length, start_node=None):
        # print(total_length, start_node)
        if start_node == None:
            start_node = self.locations.getStartNode()
            if total_length < 0: #total length is in the negative direction
                start_node = self.locations.getEndNode()
        next_start_node, region_lines = self.locations.getLinesWithinPortition(start_node, total_length)
        
        return next_start_node, region_lines
        
    
    def getLoadingRegions(self):
        regions = {}
        windmap_values_x = self.gen_desc.wind_design.wind_calc_x.windmap_values
        for value in windmap_values_x:
            regions[value.zone_case_a] = value.length
            if value.closed == False:
                #if structure is not closed
                regions[value.zone_case_b] = value.length
                
        return regions

    def saveDxf(self):
        self.writeLoadingLines()
        path = self.app_data.getRootOutPutPath('LOADINGS.DXF')
        self.dwg.saveas(path)

    def createLayers(self):
        layers = self.app_data.getLoadingDxfLayers()
        for layer, color in layers.items():
            self.dwg.layers.new(name=layer, dxfattribs={'color': color })

    
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

    def getLoadingRegionContent(self):
        regions = self.getLoadingRegions()
        start_node = None
        counter = 1
        loading_regions = []
        for region in regions:
            zone = region[0]
            length = region[1]
            next_start_node, region_lines = self.getLoadingRegionLines(length, start_node=start_node)
            loading_region = [zone, start_node, region_lines]
            loading_regions.append(loading_region)
            if counter < len(regions):
                next_length = regions[counter][1]
            else:
                #there is no next length
                next_length = None
            start_node = self.getNextNode(next_length, length, start_node, next_start_node)
            counter += 1
        return loading_regions

    def createLoadingRegionLines(self):
        regions_contents = self.getLoadingRegionContent()
        for region_content in regions_contents:
            zone = region_content[0]
            regions_lines = region_content[2]
            self.createLines(regions_lines, zone)

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
        regions = []
        windmap_values_x = self.gen_desc.wind_design.wind_calc_x.windmap_values
        for value in windmap_values_x:
            load_case = [value.zone_case_a,value.length]
            regions.append(load_case)
            if value.closed == False:
                #if structure is not closed
                load_case = [value.zone_case_b,value.length]
                regions.append(load_case)
                
        return regions

    def saveDxf(self):
        self.createLoadingRegionLines()
        path = self.app_data.getRootOutPutPath('LOADINGS.DXF')
        self.dwg.saveas(path)

    def createLayers(self):
        layers = self.app_data.getLoadingDxfLayers()
        for layer, color in layers.items():
            self.dwg.layers.new(name=layer, dxfattribs={'color': color })

    def getPortionStartNode(self, next_start_node):
        return next_start_node

    def getNextNode(self, next_length, length, node, next_node):
        if next_length == None:
            return next_node
        if next_length < 0 and length > 0:
            return None
        if abs(next_length) <= abs(length):
            return node
        return next_node
    
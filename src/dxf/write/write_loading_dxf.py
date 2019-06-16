import ezdxf
from dxf.read.dxf_input import DxfInput
from dxf.read.node_locations import NodeLocations
from libs.constants import Constants

class LoadingsDxf():
    def __init__(self, app_data, *arg):
        self.dwg = ezdxf.new('R2010')
        self.app_data = app_data
        self.msp = self.dwg.modelspace()
        self.dxfInput = DxfInput(self.app_data)
        try:
            self.wind_design = arg[0]
        except(IndexError):
            self.wind_design = None
        
        print("Creating loadings dxf . . .")
        self.locations = NodeLocations(self.dxfInput.conns, 
            nodes_array=self.dxfInput.nodes)
        self.createLayers()

    def getLoadingRegionContent(self, y_direction=False, 
        gravity_loads=False, internal_pressure=False):
        regions = self.getLoadingRegions(y_direction, gravity_loads, internal_pressure)
        start_node = None
        counter = 1
        loading_regions = []
        for region in regions:
            zone = region[0]
            length = region[1]
            load = region[2]
            next_start_node, region_lines = self.getLoadingRegionLines(length, 
                start_node=start_node, y_direction=y_direction)
            loading_region = [zone, start_node, region_lines, load]
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
        region_contents = self.getLoadingRegionContent()
        y_regions_contents = self.getLoadingRegionContent(y_direction=True)
        gravity_loads_content = self.getLoadingRegionContent(gravity_loads=True)
        internal_pressure_content = self.getLoadingRegionContent(internal_pressure=True)

        region_contents.extend(y_regions_contents)
        region_contents.extend(gravity_loads_content)
        region_contents.extend(internal_pressure_content)

        for region_content in region_contents:
            zone = region_content[0]
            regions_lines = region_content[2]
            load = region_content[3]
            height_factor = self.getHeightFactor(load)
            gravity_load = self.isGravityLoad(zone)
            load_line = self.locations.getLoadLine(regions_lines, 
                height_factor=height_factor, gravity_load=gravity_load)
            self.addLoading(load, load_line[1], zone)
            self.createLine(load_line, zone)
            self.createLines(regions_lines, zone)

    def getHeightFactor(self, load):
        if float(load) < 0:
            return 1
        return -1

    def addLoading(self, load, point, layer, height=1000):
        load_value = abs(float(load))
        self.msp.add_text(load_value,  dxfattribs={
            'layer': str(layer), 
            'height': height }).set_pos(point, align='TOP_LEFT')

    def createLines(self, region_lines, layer):
        for line in region_lines:
            line_nodes = self.dxfInput.conns[line].tolist()
            start_node = self.dxfInput.nodes[line_nodes[0]].tolist()
            end_node =self.dxfInput. nodes[line_nodes[1]].tolist()
            self.createLine([start_node, end_node], layer)

    def createLine(self, nodes, layer=0):
        self.msp.add_line(nodes[0], nodes[1], dxfattribs={'layer': str(layer)})
        #todo - get extreme corner node for region lines

    def getLoadingRegionLines(self, total_length, start_node=None, y_direction=False):
        # print(total_length, start_node)
        if total_length == 0:
            lines =  list(self.locations.conns_array.shape)[0]
            return None, [x for x in range(lines)]

        if start_node == None:
            start_node = self.locations.getStartNode()
            if total_length < 0: #total length is in the negative direction
                if y_direction:
                    start_node = self.locations.getLeftTopNode()
                else:
                    start_node = self.locations.getEndNode()

        next_start_node, region_lines = \
            self.locations.getLinesWithinPortition(start_node, 
            total_length, y_direction=y_direction)
        
        return next_start_node, region_lines

    def getLoadingRegions(self, y_direction=False, gravity_load=False,
        internal_pressure=False):
        regions = []
        if internal_pressure:
            return self.getInternalPressureRegions()
        if gravity_load:
            return self.getGravityLoads()
        if y_direction:
            windmap_values = self.wind_design.wind_calc_y.windmap_values
        else:
            windmap_values = self.wind_design.wind_calc_x.windmap_values

        for value in windmap_values:
            # print(value.toString())
            load_case = [value.zone_case_a,value.length, value.p_case_a]
            regions.append(load_case)
            if value.closed == False:
                #if structure is not closed
                load_case = [value.zone_case_b,value.length, value.p_case_b]
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

    def getNextNode(self, next_length, length, node, next_node):
        if next_length == None:
            return next_node
        if next_length < 0 and length > 0:
            return None
        if abs(next_length) <= abs(length):
            return node
        return next_node
    
    def getGravityLoads(self):
        dead_load_factor = self.wind_design.props[Constants.ROOF_DEAD_LOAD]
        services_load_factor = self.wind_design.props[Constants.SERVICES_LOAD]
        live_load_factor = self.wind_design.props[Constants.ROOF_LIVE_LOAD]

        return [[801, 0., dead_load_factor],[802, 0., services_load_factor],
            [803, 0., live_load_factor]]

    def isGravityLoad(self, zone):
        if zone == 801 or zone == 802 or zone == 803:
            return True
        return False

    def getInternalPressureRegions(self):
        regions = []
        windmap_values = self.wind_design.internal_pressure_zone_ps
        for key, value in windmap_values.items():
                #if structure is not closed
                load_case = [key, 0., value]
                regions.append(load_case)
        return regions
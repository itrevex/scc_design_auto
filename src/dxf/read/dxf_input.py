import ezdxf, sys
import numpy as np

class DxfInput():
    TOR = 0.001
    def __init__(self, app_data):
        self.app_data = app_data
        self.getGeomFile()
        pass
    
    def getGeomFile(self):
        geom_file = self.app_data.getGeomFile()
        print(geom_file)
        try:
            dwg = ezdxf.readfile(geom_file)
            modelspace = dwg.modelspace()
            layer_61_lines = modelspace.query('LINE[layer=="61"]')
            layer_71_lines = modelspace.query('LINE[layer=="71"]')
            nodes_array = self.getTopChordNodesArray(modelspace, layer_61_lines,layer_71_lines)

            #get top chord connectivities
            layer_61_conns = self.getNodalConnectivites(layer_61_lines, nodes_array)
            layer_71_conns = self.getNodalConnectivites(layer_71_lines, nodes_array)

            print(layer_61_conns)

        except FileNotFoundError:
            print("Please add GEOM1.DXF file to working folder")
            sys.exit()

    def inList(self, list1, list2):
        return list1 == list2

    def getNodeIndex(self, end_node, nodes):
        index = 0
        for node in nodes:
            if self.equalLine(node, end_node):
                return index
            index +=1
        return None

    def equalLine(self, line1, line2):
        return self.pointEqual(line1[0], line2[0]) \
            and self.pointEqual(line1[1], line2[1]) \
            and self.pointEqual(line1[2], line2[2])

    def pointEqual(self, pt1, pt2):
        return abs(pt1-pt2) <= DxfInput.TOR

    def getTopChordNodesArray(self, modelspace, layer_61_lines, layer_71_lines):
        
        nodes = []
        nodes.extend(self.getLayerNodes(layer_61_lines))
        nodes.extend(self.getLayerNodes(layer_71_lines))

        return np.unique(nodes, axis=0)

    def getLayerNodes(self, lines):
        nodes = []
        for e in lines:
            start_node = e.dxf.start
            end_node = e.dxf.end
            nodes.append(start_node)
            nodes.append(end_node)
        return nodes

    def getNodalConnectivites(self, lines, nodes):
        connectivities = []
        for e in lines:
            start_node = e.dxf.start
            end_node = e.dxf.end
            start_node_index = self.getNodeIndex(start_node, nodes)
            end_node_index = self.getNodeIndex(end_node, nodes)
            connected = [start_node_index, end_node_index]
            connectivities.append(connected)
        
        return connectivities

    
    #open dxf file
    #read in all entities
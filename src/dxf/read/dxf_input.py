import ezdxf, sys, copy
import numpy as np

class DxfInput():
    TOR = 0.001
    def __init__(self, app_data):
        self.app_data = app_data
        self.getGeomFile()
        pass
    
    def getGeomFile(self):
        geom_file = self.app_data.getGeomFile()
        try:
            dwg = ezdxf.readfile(geom_file)
            modelspace = dwg.modelspace()
            layer_61_lines = modelspace.query('LINE[layer=="61"]')
            layer_71_lines = modelspace.query('LINE[layer=="71"]')
            nodes_array = self.getTopChordNodesArray(modelspace, layer_61_lines,layer_71_lines)

            #get top chord connectivities
            conns = self.getNodalConnectivites(layer_61_lines, nodes_array)
            layer_71_conns = self.getNodalConnectivites(layer_71_lines, nodes_array)
            conns.extend(layer_71_conns)
            conns = np.array(self.removeDuplicates(conns))
            print(conns.shape)

            #remove repeats and put in a single array

        except FileNotFoundError:
            print("Please add GEOM1.DXF file to working folder")
            sys.exit()

    def removeDuplicates(self, conns):
        new_conns = []
        for conn in conns:
            for new_con in new_conns:
                if self.equalLine(conn, new_con):
                    break
            else:
                new_conns.append(conn)
        return new_conns


    def equalLine(self, conn1, conn2):
        conn = copy.deepcopy(conn2)
        for e in conn1:
            if e not in conn:
                return False
            else:
                conn.remove(e)
        return True

    def getNodeIndex(self, end_node, nodes):
        index = 0
        for node in nodes:
            if self.equalNode(node, end_node):
                return index
            index +=1
        return None

    def equalNode(self, node1, node2):
        return self.pointEqual(node1[0], node2[0]) \
            and self.pointEqual(node1[1], node2[1]) \
            and self.pointEqual(node1[2], node2[2])

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
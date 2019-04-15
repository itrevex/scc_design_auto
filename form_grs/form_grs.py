import re
from libs.constants import Constants
class FormGrs:
    
    def __init__(self, app_data, gen_desc):
        self.gen_desc = gen_desc
        self.app_data = app_data

        self.lines = self.readInFile()
        self.changeTitle()
        self.changeLoads()
        pass

    def readInFile(self):
        #step 1: read file into lines
        form_grs_file = self.app_data.getFormGrsFile(
            self.gen_desc.design_code, self.gen_desc.enclosure)
        
        with open(form_grs_file) as f:
            lines = [line.strip() for line in f.readlines()]

        return lines 

    def changeTitle(self):
        #step 2: change title
        self.lines[0] = self.gen_desc.project_name
       
        pass

    def getStringIndex(self, text):
        i = 0
        while i < len(self.lines):
            if re.search(text, self.lines[i], re.IGNORECASE):
                return i
            i += 1

        return None
    
    def changeLoads(self):
        #step 3: change loads

        #update dead, service and live loads
        self.updateDeadLoad()
        self.updateServicesLoad()
        self.updateLiveLoad()
        self.updateWindLoads()

        # for line in self.lines:
        #     print(line)

        pass

    def updateDeadLoad(self):
        dead_load_factor = self.gen_desc.new_input_values[Constants.ROOF_DEAD_LOAD]
        dead_load_line = self.getStringIndex("Roof Dead Loads")
        dead_load_new_line = \
            "LC02  : Roof Dead Loads = %s kN/m2                801"%dead_load_factor

        self.lines[dead_load_line] = dead_load_new_line

    def updateServicesLoad(self):
        services_load_factor = self.gen_desc.new_input_values[Constants.SERVICES_LOAD]
        services_load_line = self.getStringIndex("Services Loads")
        services_load_new_line = \
            "LC03  : Services Loads  = %s kN/m2                802"%services_load_factor

        self.lines[services_load_line] = services_load_new_line

    def updateLiveLoad(self):
        live_load_factor = self.gen_desc.new_input_values[Constants.ROOF_LIVE_LOAD]
        live_load_line = self.getStringIndex("Live Load")
        live_load_new_line = \
            "LC04  : Live Load = %s kN/m2                      803"%live_load_factor

        self.lines[live_load_line] = live_load_new_line

    def updateWindLoads(self):
        # get wind in +x direction A
        # get wind in +x direction B
        print()
        print(self.gen_desc.wind_design.combinations)
        pass

    def printOutPutFile(self):
        #step 4: write new form grs file
        pass
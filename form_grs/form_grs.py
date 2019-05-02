import re
from libs.constants import Constants
class FormGrs:
    
    def __init__(self, app_data, gen_desc):
        self.gen_desc = gen_desc
        self.app_data = app_data

        self.lines = self.readInFile()
        self.changeTitle()
        self.changeLoads()

        print(gen_desc.wind_design.combinations)
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

        if self.gen_desc.wind_design.enclosed:
            self.updateWindLoadsClosed()
            #update internal pressure combinations
            for key, value in self.gen_desc.wind_design.pressure_combinations.items():
                self.writePressureCombinations(key, value)
                pass
            pass
        else:
            self.updateWindLoads()

        #write lines to form-grs file and close it after
        form_grs_file = self.app_data.getFormGrmsFile()
        for line in self.lines:
            line.strip()
            if line != "":
                form_grs_file.write(line+"\n")

        form_grs_file.close()
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
        #update windloads for open structures
        # get wind in +x direction A
        # get wind in +x direction B
        cases = ["A", "B"]
        directions = ["+X", "+X","-X", "-X","+Y", "+Y","-Y", "-Y"]
        counter = 0

        for key, value in self.gen_desc.wind_design.combinations.items():
            self.writeLoadCombinationLine(key, value, directions[counter%8], cases[counter%2])
            counter += 1

    def updateWindLoadsClosed(self):
        #update windloads for open structures
        # get wind in +x direction A
        # get wind in +x direction B
        directions = ["+X", "-X", "+Y", "-Y"]
        counter = 0

        for key, value in self.gen_desc.wind_design.combinations.items():
            self.writeLoadCombinationLineClosed(key, value, directions[counter%4])
            counter += 1

    def writeLoadCombinationLine(self, key, value, direction, case):
        line = self.getStringIndex("^%s"%key)
        cases = "  ".join(str(i) for i in value)
        new_line = "%s  : Wind Along %s Direction(%s)                  %s "% \
            (key, direction, case, cases)
        self.lines[line] = new_line
        pass

    def writePressureCombinations(self, key, value):
        line = self.getStringIndex("^%s"%key)
        new_line = "%s  : Positive Internal Pressure                  %s"% \
            (key, value)
        self.lines[line] = new_line
        pass

    def writeLoadCombinationLineClosed(self, key, value, direction):
        line = self.getStringIndex("^%s"%key)
        cases = "  ".join(str(i) for i in value)
        new_line = "%s  : Wind Along %s Direction                     %s "% \
            (key, direction, cases)
        self.lines[line] = new_line
        pass

    def printOutPutFile(self):
        #step 4: write new form grs file
        pass
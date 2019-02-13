class WindMapValue:
    def __init__(self, title, c_case_a, c_case_b, p_case_a, 
            p_case_b, zone_case_a):
        
        self.title = title
        self.roof_angle = None

        self.c_case_a = c_case_a
        self.c_case_b = c_case_b
        self.p_case_a = p_case_a
        self.p_case_b = p_case_b
        self.zone_case_a = zone_case_a
        self.zone_case_b = self.zone_case_a + 1
        self.plot_lines = []

    def setTitle(self, title):
        self.title = title

    def setRoofAngle(self, angle):
        self.roof_angle = angle

    def setCCaseA(self, c):
        self.c_case_a = c

    def setCCaseB(self, c):
        self.c_case_b = c

    def setPCaseA(self, p):
        self.p_case_a = p
    
    def setPCaseB(self, p):
        self.p_case_b = p

    def setZoneCaseA(self, zone):
        self.zone_case_a = zone

    def setZoneCaseB(self, zone):
        self.zone_case_b = zone

    def setPlotLines(self, plot_lines):
        self.plot_lines = plot_lines

    def toString(self):
        text = " "
        text += "\n title: " + self.title 
        text += "\n roof angle: " + str(self.roof_angle) 
        text += "\n c case a: " + str(self.c_case_a) 
        text += "\n c case b: " + str(self.c_case_b)
        text += "\n p case b: " + str(self.p_case_a) 
        text += "\n p case b: " + str(self.p_case_b)
        text += "\n zone case a: " + str(self.zone_case_a)
        text += "\n zone case b: " + str(self.zone_case_b) 
        text +="\n Lines: "
        for x in self.plot_lines:
            text += "\n"+x  
        return text

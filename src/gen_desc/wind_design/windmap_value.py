class WindMapValue:
    def __init__(self, title, c_case_a, c_case_b, p_case_a, 
            p_case_b, zone_case_a, roof_angle, coeff_prefix="N", closed=False):
        
        self.closed = closed
        self.title = title
        self.roof_angle = roof_angle

        self.c_case_a = c_case_a
        self.c_case_b = c_case_b
        self.p_case_a = p_case_a
        self.p_case_b = p_case_b
        self.zone_case_a = zone_case_a
        self.zone_case_b = self.zone_case_a + 1
        self.coeff_prefix = coeff_prefix
        self.plot_lines = []
        self.zone_ps = {}
        self.setPlotLines() 
        self.setZonePValues()

    def setZonePValues(self):
        '''
        Store zone: p value dictionary.
        This will be used to create list of zones used when making 
        loadings dxf
        '''

        self.zone_ps[self.zone_case_a] = float(self.p_case_a)
        if self.closed == False:
            self.zone_ps[self.zone_case_b] = float(self.p_case_b)

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

    def setCoeffPrefix(self, prefix):
        self.coeff_prefix = prefix
        
    def setPlotLines(self):
        '''
        Sets plot lines for the windmap_value
        '''
        titles = self.title.split(" ")
        self.plot_lines.append("$%s$"%self.title)
        self.plot_lines.append("$θ = %s˚$"%self.roof_angle)
        if self.closed:
            self.plot_lines.append("$C_%s = %.1f$"%(self.coeff_prefix,self.c_case_a))
        else:
            self.plot_lines.append("$CASE A: C_%s = %.1f$"%(self.coeff_prefix,self.c_case_a))
        self.plot_lines.append("$P = %skN/sq.m$"%self.p_case_a)
        self.plot_lines.append("$Zone: %d$"%self.zone_case_a)
        self.plot_lines.append("")

        if (self.closed == False):
            self.plot_lines.append("$CASE B: C_%s = %.1f$"%(self.coeff_prefix,self.c_case_b))
            self.plot_lines.append("$P = %skN/sq.m$"%self.p_case_b)
            self.plot_lines.append("$Zone: %d$"%self.zone_case_b)
        pass
             

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

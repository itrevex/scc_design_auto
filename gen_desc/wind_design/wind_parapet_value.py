class WindParapetValue:
    def __init__(self,title, subtitle, coeff, p, zone):
        
        self.title = title
        self.subtitle = subtitle
        self.coeff = coeff
        self.p = p
        self.zone = zone
        self.plot_lines = []
        self.setPlotLines() 

    def setTitle(self, title):
        self.title = title

    def setPlotLines(self):
        '''
        Sets plot lines for the windmap_value
        '''
    
        self.plot_lines.append("$%s$"%self.title)
        self.plot_lines.append("$%s$"%self.subtitle)
        self.plot_lines.append("$GC_pn = +%.1f$"%self.coeff)
        self.plot_lines.append("$P = %skN/sq.m$"%self.p)
        self.plot_lines.append("$Zone: %d$"%self.zone)
        pass
             
    def toString(self):
        text = " "
        text += "\n title: " + self.title 
        text += "\n subtitle: " + str(self.subtitle) 
        text += "\n coeff: " + str(self.coeff) 
        text += "\n p: " + str(self.p)
        text += "\n zone: " + str(self.zone) 
        text +="\n Lines: "
        for x in self.plot_lines:
            text += "\n"+x  
        return text

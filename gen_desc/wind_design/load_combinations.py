class LoadCombinations:
    def __init__(self, wind_design):
        self.wind_design = wind_design
        pass

    def setUpCombinations(self):
        self.combination_a = "LC" + "{:02d}".format(self.wind_design.current_combination)
        self.wind_design.combinations[self.combination_a] = []
        self.wind_design.current_combination += 1

        if self.wind_design.enclosed == False:
            self.combination_b = "LC" + "{:02d}".format(self.wind_design.current_combination)
            self.wind_design.combinations[self.combination_b] = []
            self.wind_design.current_combination += 1

        self.combination_a_neg = "LC" + "{:02d}".format(self.wind_design.current_combination)
        self.wind_design.combinations[self.combination_a_neg] = []
        self.wind_design.current_combination += 1

        if self.wind_design.enclosed == False:
            self.combination_b_neg = "LC" + "{:02d}".format(self.wind_design.current_combination)
            self.wind_design.combinations[self.combination_b_neg] = []
            self.wind_design.current_combination += 1
    
    def storeCombinations(self):
        self.wind_design.combinations[self.combination_a] \
            .append(self.wind_design.zone)
        
        if self.wind_design.enclosed == False:
            self.wind_design.combinations[self.combination_b] \
                .append(self.wind_design.zone + 1)

    def storeCombinationsNeg(self): 
        self.wind_design.combinations[self.combination_a_neg] \
            .append(self.wind_design.zone)
            
        if self.wind_design.enclosed == False:
            self.wind_design.combinations[self.combination_b_neg] \
                .append(self.wind_design.zone + 1)

    def storeCombinationsParapetNeg(self, zone):
        self.wind_design.combinations[self.combination_a_neg] \
            .append(zone)
            
        if self.wind_design.enclosed == False:
            self.wind_design.combinations[self.combination_b_neg] \
                .append(zone)

    def storeCombinationsParapet(self, zone):
        self.wind_design.combinations[self.combination_a] \
            .append(zone)
        
        if self.wind_design.enclosed == False:
            self.wind_design.combinations[self.combination_b] \
                .append(zone)

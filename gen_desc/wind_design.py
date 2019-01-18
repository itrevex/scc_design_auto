from run_properties import RunProperties

class WindDesign:
    WIND_DESIGN_X = "wind_design_x"
    WIND_DESIGN_ALONG_X = "along_x"
    WIND_DESIGN_TITLE = "title"
    WIND_DESIGN_TITLE_MINUS = "title_minus"
    WIND_DESIGN_WINDWARD_O5 = "windward_0.5"
    WIND_DESIGN_WINDWARD_05_L = "windward_0.5_L"
    WIND_DESIGN_LEEWARD_05 = "leeward_0.5"
    WIND_DESIGN_LEEWARD_05_L = "leeward_0.5_L"
    WIND_DESIGN_CASE_A = "case_a"
    WIND_DESIGN_CASE_B = "case_b"
    WIND_DESIGN_ZONE = "zone"
    WIND_DESIGN_BRACKET = "bracket"
    WIND_DESIGN_NW = "nw"
    WIND_DESIGN_NL = "nl"
    WIND_DESIGN_EQUALS = "equals"
    # WIND_DESIGN_

    def __init__(self):
        pass

    class WindDesignPartsX:
        def __init__(self, app_data):
            self.runs = []
            self.app_data = app_data.getWindDesignDefaults()
            self.template_data = self.app_data[WindDesignPartsX.WIND_DESIGN_ALONG_X]
            self.wind_factors = self.app_data[WindDesignPartsX.WIND_DESIGN_ALONG_X]
            self.run_parts = self.getRunParts()
            self.runsWindWard()
            self.runsLeeWard()
        
            pass

        def getRunParts(self):
            run_parts = {}
            for part_name, parts in self.template_data.items():
                for text, props in parts.items():
                    run_parts[part_name] = RunProperties(text, props)
                    pass

            return run_parts

        def windCases(self):
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_CASE_A])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_NW])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_EQUALS])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_ZONE])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_BRACKET])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_CASE_B])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_NL])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_EQUALS])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_ZONE])
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_BRACKET])

        def runsWindWard(self):
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_TITLE])
            #wind load windward_05
            self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_WINDWARD_O5])
            self.windCases()


        #wind load windward_05L
        self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_WINDWARD_05_L])
        self.windCases()

    def runsLeeWard(self):
        self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_TITLE_MINUS])

        #wind load windward_05
        self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_WINDWARD_O5])
        self.windCases()


        #wind load windward_05L
        self.runs.append(self.run_parts[WindDesignPartsX.WIND_DESIGN_WINDWARD_O5])
        self.windCases()



    class WindCase:
        def __init__(self, coeff, zone):
            self.coeff = self.setCoeff(coeff)
            self.zone = self.setZone(coeff)
        
        def setCoeff(self, coeff):
            self.coeff = RunProperties(coeff, {})
        
        def setZone(self, zone):
            self.zone = RunProperties(zone, {})

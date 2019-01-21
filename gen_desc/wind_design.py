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

    def __init__(self,app_data):
        self.app_data = app_data.getWindDesignDefaults()
        data_x = self.app_data[WindDesign.WIND_DESIGN_ALONG_X]
        wind_factors_x = app_data.getWindCoeffiecients()[WindDesign.WIND_DESIGN_ALONG_X]
        self.zone = 804
        self.wind_x = self.WindDesignPartsX(self, data_x, wind_factors_x)
        pass

    class WindDesignPartsX:
        def __init__(self, wind_design, template_data, wind_factors):
            self.wind_design = wind_design
            self.template_data = template_data
            self.wind_factors = wind_factors
            self.runs = []
            self.run_parts = self.getRunParts()
            self.loadCoeffiecients()
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

        def windCases(self, cnw = 1, cnl = 1):
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_CASE_A])
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_NW])
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_EQUALS])
            self.runs.append(RunProperties(cnw, {}))
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_ZONE])
            self.runs.append(RunProperties(self.wind_design.zone, {}))
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_BRACKET])
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_CASE_B])
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_NL])
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_EQUALS])
            self.runs.append(RunProperties(cnl, {}))
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_ZONE])
            self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_BRACKET])
            self.wind_design.zone += 2

        def runsWindWard(self):
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_TITLE])
            #wind load windward_05
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_WINDWARD_O5])
            self.windCases(self.cnw_05, self.cnl_05)


            #wind load windward_05L
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_WINDWARD_05_L])
            self.windCases(self.cnw_05L, self.cnl_05L)

        def runsLeeWard(self):
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_TITLE_MINUS])

            #wind load windward_05
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_WINDWARD_O5])
            self.windCases(self.cnw_05, self.cnl_05)


            #wind load windward_05L
            self.runs.append(self.run_parts[WindDesign.WIND_DESIGN_WINDWARD_O5])
            self.windCases(self.cnw_05L, self.cnl_05L)

        def loadCoeffiecients(self):
            print()
            print('---------------------------')
            factors_05 = self.wind_factors[WindDesign.WIND_DESIGN_WINDWARD_O5]
            factors_05L = self.wind_factors[WindDesign.WIND_DESIGN_WINDWARD_05_L]

            self.cnw_05 = factors_05[WindDesign.WIND_DESIGN_CASE_A]
            self.cnl_05 = factors_05[WindDesign.WIND_DESIGN_CASE_B]

            self.cnw_05L = factors_05L[WindDesign.WIND_DESIGN_CASE_A]
            self.cnl_05L = factors_05L[WindDesign.WIND_DESIGN_CASE_B]

            print(self.cnw_05)
            # for value in self.wind_factors.values():
                

    class WindCase:
        def __init__(self, coeff, zone):
            self.coeff = self.setCoeff(coeff)
            self.zone = self.setZone(coeff)
        
        def setCoeff(self, coeff):
            self.coeff = RunProperties(coeff, {})
        
        def setZone(self, zone):
            self.zone = RunProperties(zone, {})

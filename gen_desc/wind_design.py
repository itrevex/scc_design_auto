from run_properties import RunProperties

class WindDesign:

    #wind design x constants
    ALONG_X = "along_x"
    TITLE = "title"
    TITLE_MINUS = "title_minus"
    WINDWARD_O5 = "windward_0.5"
    WINDWARD_05_L = "windward_0.5_L"
    LEEWARD_05 = "leeward_0.5"
    LEEWARD_05_L = "leeward_0.5_L"
    CASE_A = "case_a"
    CASE_B = "case_b"
    ZONE = "zone"
    BRACKET = "bracket"
    NW = "nw"
    NL = "nl"
    P = "p"
    ZONE_CALC = "zone_calc"
    CASE_A_CALC = "case_a_calc"
    CASE_B_CALC = "case_b_calc"
    EQUALS = "equals"
    # 

    #wind design y constants
    ALONG_Y = "along_y"
    WINDWARD_H = "windward_h"
    WINDWARD_H_2H = "windward_h_2h"
    WINDWARD_2H = "windward_2h"
    LEEWARD_H = "leeward_h"
    LEEWARD_H_2H = "leeward_h_2h"
    LEEWARD_2H = "leeward_2h"
    N = "n"
    WIND_FACTOR = 0.85

    def __init__(self,app_data, wind_load=1.0):
        self.app_data = app_data.getWindDesignDefaults()
        self.wind_load = wind_load
        data_x = self.app_data[WindDesign.ALONG_X]
        data_y = self.app_data[WindDesign.ALONG_Y]
        wind_factors_x = app_data.getWindCoeffiecients()[WindDesign.ALONG_X]
        wind_factors_y = app_data.getWindCoeffiecients()[WindDesign.ALONG_Y]
        self.zone = 804
        self.wind_x = self.WindDesignPartsX(self, data_x, wind_factors_x)

        self.wind_y =  self.WindDesignPartsY(self, data_y, wind_factors_y)

        self.wind_calc_x = self.WindCalculationsX(self, data_x, wind_factors_x)

        self.wind_calc_y = self.WindCalculationsY(self, data_y, wind_factors_y)
        
        
        pass

    def resetZone(self):
        self.zone = 804

    def windLoad(self, wind_factor):
        load = float(wind_factor) * self.wind_load \
        * WindDesign.WIND_FACTOR

        return "{:.4f}".format(load)

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
            self.runs.append(self.run_parts[WindDesign.CASE_A])
            self.runs.append(self.run_parts[WindDesign.NW])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(cnw, {}))
            self.runs.append(self.run_parts[WindDesign.ZONE])
            self.runs.append(RunProperties(self.wind_design.zone, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.runs.append(self.run_parts[WindDesign.CASE_B])
            self.runs.append(self.run_parts[WindDesign.NL])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(cnl, {}))
            self.runs.append(self.run_parts[WindDesign.ZONE])
            self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.wind_design.zone += 2

        def runsWindWard(self):
            self.runs.append(self.run_parts[WindDesign.TITLE])
            #wind load windward_05
            self.runs.append(self.run_parts[WindDesign.WINDWARD_O5])
            self.windCases(self.cnw_05, self.cnl_05)


            #wind load windward_05L
            self.runs.append(self.run_parts[WindDesign.WINDWARD_05_L])
            self.windCases(self.cnw_05L, self.cnl_05L)

        def runsLeeWard(self):
            self.runs.append(self.run_parts[WindDesign.TITLE_MINUS])

            #wind load windward_05
            self.runs.append(self.run_parts[WindDesign.WINDWARD_O5])
            self.windCases(self.cnw_05, self.cnl_05)


            #wind load windward_05L
            self.runs.append(self.run_parts[WindDesign.WINDWARD_O5])
            self.windCases(self.cnw_05L, self.cnl_05L)

        def loadCoeffiecients(self):
            
            factors_05 = self.wind_factors[WindDesign.WINDWARD_O5]
            factors_05L = self.wind_factors[WindDesign.WINDWARD_05_L]

            self.cnw_05 = factors_05[WindDesign.CASE_A]
            self.cnl_05 = factors_05[WindDesign.CASE_B]

            self.cnw_05L = factors_05L[WindDesign.CASE_A]
            self.cnl_05L = factors_05L[WindDesign.CASE_B]

            # for value in self.wind_factors.values():
                
    class WindDesignPartsY:
        def __init__(self, wind_design, template_data, wind_factors):
            self.wind_design = wind_design
            self.template_data = template_data
            self.wind_factors = wind_factors
            self.runs = []
            self.run_parts = self.getRunParts()
            self.loadCoeffiecients()
            self.runsWindWard()
            self.runsLeeWard()

        def getRunParts(self):
            run_parts = {}
            for part_name, parts in self.template_data.items():
                for text, props in parts.items():
                    run_parts[part_name] = RunProperties(text, props)
                    pass

            return run_parts

        def windCases(self, case_a = 1, case_b = 1):
            self.runs.append(self.run_parts[WindDesign.CASE_A])
            self.runs.append(self.run_parts[WindDesign.N])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(case_a, {}))
            self.runs.append(self.run_parts[WindDesign.ZONE])
            self.runs.append(RunProperties(self.wind_design.zone, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.runs.append(self.run_parts[WindDesign.CASE_B])
            self.runs.append(self.run_parts[WindDesign.N])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(case_b, {}))
            self.runs.append(self.run_parts[WindDesign.ZONE])
            self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.wind_design.zone += 2

        def runsWindWard(self):
            self.runs.append(self.run_parts[WindDesign.TITLE])

            #wind load windward_h
            self.runs.append(self.run_parts[WindDesign.WINDWARD_H])
            self.windCases(self.h_case_a, self.h_case_b)


            #wind load windward_h_2h
            self.runs.append(self.run_parts[WindDesign.WINDWARD_H_2H])
            self.windCases(self.h_2h_case_a, self.h_2h_case_b)

            #wind load windward_2h
            self.runs.append(self.run_parts[WindDesign.WINDWARD_2H])
            self.windCases(self._2h_case_a, self._2h_case_b)

        def runsLeeWard(self):
            self.runs.append(self.run_parts[WindDesign.TITLE_MINUS])

            #wind load leeward_h
            self.runs.append(self.run_parts[WindDesign.WINDWARD_H])
            self.windCases(self.h_case_a, self.h_case_b)


            #wind load leeward_h_2h
            self.runs.append(self.run_parts[WindDesign.WINDWARD_H_2H])
            self.windCases(self.h_2h_case_a, self.h_2h_case_b)

            #wind load leeward_2h
            self.runs.append(self.run_parts[WindDesign.WINDWARD_2H])
            self.windCases(self._2h_case_a, self._2h_case_b)

        def loadCoeffiecients(self):
            
            factors_h = self.wind_factors[WindDesign.WINDWARD_H]
            factors_h_2h = self.wind_factors[WindDesign.WINDWARD_H_2H]
            factors_2h = self.wind_factors[WindDesign.WINDWARD_2H]

            self.h_case_a = factors_h[WindDesign.CASE_A]
            self.h_case_b = factors_h[WindDesign.CASE_B]

            self.h_2h_case_a = factors_h_2h[WindDesign.CASE_A]
            self.h_2h_case_b = factors_h_2h[WindDesign.CASE_B]


            self._2h_case_a = factors_2h[WindDesign.CASE_A]
            self._2h_case_b = factors_2h[WindDesign.CASE_B]

    class WindCalculationsX(WindDesignPartsX): 
        def __init__(self,  wind_design, template_data, wind_factors):
            wind_design.resetZone()
            super().__init__(wind_design, template_data, wind_factors)
            pass

        def windCases(self, cnw = 1, cnl = 1):
            self.runs.append(self.run_parts[WindDesign.CASE_A_CALC])
            self.runs.append(self.run_parts[WindDesign.P])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(self.wind_design.windLoad(cnw), {}))
            self.runs.append(self.run_parts[WindDesign.ZONE_CALC])
            self.runs.append(RunProperties(self.wind_design.zone, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.runs.append(self.run_parts[WindDesign.CASE_B_CALC])
            self.runs.append(self.run_parts[WindDesign.P])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(self.wind_design.windLoad(cnl), {}))
            self.runs.append(self.run_parts[WindDesign.ZONE_CALC])
            self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.wind_design.zone += 2

    class WindCalculationsY(WindDesignPartsY): 
        def __init__(self,  wind_design, template_data, wind_factors):
            super().__init__(wind_design, template_data, wind_factors)
            pass
        
        def windCases(self, case_a = 1, case_b = 1):
            self.runs.append(self.run_parts[WindDesign.CASE_A])
            self.runs.append(self.run_parts[WindDesign.P])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(self.wind_design.windLoad(case_a), {}))
            self.runs.append(self.run_parts[WindDesign.ZONE_CALC])
            self.runs.append(RunProperties(self.wind_design.zone, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.runs.append(self.run_parts[WindDesign.CASE_B])
            self.runs.append(self.run_parts[WindDesign.P])
            self.runs.append(self.run_parts[WindDesign.EQUALS])
            self.runs.append(RunProperties(self.wind_design.windLoad(case_b), {}))
            self.runs.append(self.run_parts[WindDesign.ZONE_CALC])
            self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
            self.runs.append(self.run_parts[WindDesign.BRACKET])
            self.wind_design.zone += 2

            
    class WindCase:
        def __init__(self, coeff, zone):
            self.coeff = self.setCoeff(coeff)
            self.zone = self.setZone(coeff)
        
        def setCoeff(self, coeff):
            self.coeff = RunProperties(coeff, {})
        
        def setZone(self, zone):
            self.zone = RunProperties(zone, {})

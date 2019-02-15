from gen_desc.run_properties import RunProperties
from .constants import WindDesignConsts
from .wind_parapets import WindParapets
from .wind_x import WindDesignPartsX
from .windmap_value import WindMapValue

class WindCalculationsX(WindDesignPartsX): 
    def __init__(self, wind_design):
        wind_design.resetZone()
        super().__init__(wind_design)
        pass
    
    def addParapetRuns(self):
        if (self.wind_design.parapet_load == "true"):
            # self.runsParapet()
            runs_parapets = WindParapets(self.wind_design, self.run_parts, 
                self.pn_windward, self.pn_leeward, True, self.windmap_values)
            self.runs.extend(runs_parapets.runs)

    def windCases(self, c_case_a = 1, c_case_b = 1, title=None):
        p_case_a = self.wind_design.windLoad(c_case_a)
        p_case_b = self.wind_design.windLoad(c_case_b)
        zone_case_a = self.wind_design.zone

        windmap_value = WindMapValue(title, c_case_a, c_case_b, p_case_a, 
        p_case_b, zone_case_a, self.wind_design.roof_angle)

        self.windmap_values.append(windmap_value)

        self.runs.append(self.run_parts[WindDesignConsts.CASE_A_CALC])
        self.runs.append(self.run_parts[WindDesignConsts.P])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(p_case_a, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE_CALC])
        self.runs.append(RunProperties(zone_case_a, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.runs.append(self.run_parts[WindDesignConsts.CASE_B_CALC])
        self.runs.append(self.run_parts[WindDesignConsts.P])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(p_case_b, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE_CALC])
        self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.wind_design.zone += 2


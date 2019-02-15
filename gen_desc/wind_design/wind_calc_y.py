from gen_desc.run_properties import RunProperties
from .constants import WindDesignConsts
from .wind_parapets import WindParapets
from .wind_y import WindDesignPartsY
from gen_desc.wind_design.windmap_value import WindMapValue

class WindCalculationsY(WindDesignPartsY): 
    NL = "{NL}"
    NW = "{NW}"
    def __init__(self,  wind_design):
        super().__init__(wind_design)
        pass
    
    def addParapetRuns(self):
        if (self.wind_design.parapet_load == "true"):
            # self.runsParapet()
            runs_parapets = WindParapets(self.wind_design, self.run_parts, 
                self.pn_windward, self.pn_leeward, True)
            self.runs.extend(runs_parapets.runs)

    def windCases(self, cnw = 1, cnl = 1, title=None):

        p_case_a = self.wind_design.windLoad(cnw)
        p_case_b = self.wind_design.windLoad(cnl)
        zone_case_a = self.wind_design.zone

        prefix = WindCalculationsY.NL

        if self.direction == 'pos':
            prefix = WindCalculationsY.NW

        windmap_value = WindMapValue(title, cnw, cnl, p_case_a, 
        p_case_b, zone_case_a, self.wind_design.roof_angle, prefix)
        

        self.windmap_values.append(windmap_value)

        self.runs.append(self.run_parts[WindDesignConsts.CASE_A_CALC])
        self.runs.append(self.run_parts[WindDesignConsts.P])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(self.wind_design.windLoad(cnw), {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE_CALC])
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.runs.append(self.run_parts[WindDesignConsts.CASE_B_CALC])
        self.runs.append(self.run_parts[WindDesignConsts.P])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(self.wind_design.windLoad(cnl), {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE_CALC])
        self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.wind_design.zone += 2


from gen_desc.run_properties import RunProperties
from .constants import WindDesignConsts
from .wind_parapets import WindParapets
from .wind_x import WindDesignPartsX
from .windmap_value import WindMapValue
from .internal_pressure import InternalPressure

class WindCalculationsX(WindDesignPartsX): 
    def __init__(self, wind_design, y_values=False):

        if y_values == False:
            wind_design.resetZone()
            
        super().__init__(wind_design, y_values)
        pass

    def setUpCombinations(self):
        #overide function and do nothing in it
        pass
        
    def addParapetRuns(self):
        if (self.wind_design.parapet_load == "true"):
            # self.runsParapet()
            runs_parapets = WindParapets(self.wind_design, self.run_parts, 
                self.pn_windward, self.pn_leeward, True, self.windmap_values)
            self.runs.extend(runs_parapets.runs)

    def addInternalPressures(self):
        if (self.wind_design.enclosed == True):
            runs_parapets = InternalPressure(self.wind_design, 0.18, True)
            self.wind_design.internal_pressure_zone_ps.update(runs_parapets.zone_ps) 
            self.runs.extend(runs_parapets.runs)

    def windCases(self, c_case_a = 1, c_case_b = 1, title=None, length=0.):
        p_case_a = self.wind_design.windLoad(c_case_a)
        p_case_b = self.wind_design.windLoad(c_case_b)
        zone_case_a = self.wind_design.zone

        #for runs in opposite direction, show length as a negative
        factored_length = 1 * length
        if self.negative_direction:
            factored_length = -1 * length

        windmap_value = WindMapValue(title, c_case_a, c_case_b, p_case_a, 
        p_case_b, zone_case_a, self.wind_design.roof_angle, length=factored_length)

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

    def windCasesClosed(self, cp = 1, title=None, length=0.):

        p_case_a = self.wind_design.windLoad(cp)
        zone_case_a = self.wind_design.zone
        #for runs in opposite direction, show length as a negative
        factored_length = 1 * length
        if self.negative_direction:
            factored_length = -1 * length

        windmap_value = WindMapValue(title, cp, "0", p_case_a, 
        "0", zone_case_a, self.wind_design.roof_angle, coeff_prefix="p", closed=True,
         length=factored_length)

        self.windmap_values.append(windmap_value)

        self.runs.append(self.run_parts[WindDesignConsts.CASE_A_CALC])
        self.runs.append(self.run_parts[WindDesignConsts.P])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(p_case_a, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE_CALC])
        self.runs.append(RunProperties(zone_case_a, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])


        self.wind_design.zone += 1


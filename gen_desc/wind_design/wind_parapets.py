from gen_desc.run_properties import RunProperties
from .constants import WindDesignConsts

class WindParapets:
    def __init__(self, wind_design, run_parts, pn_windward, pn_leeward, calcs = False):
        self.wind_design = wind_design
        self.run_parts = run_parts
        self.pn_windward = pn_windward
        self.pn_leeward = pn_leeward
        self.calcs = calcs
        self.runs = [RunProperties("", { "end_of_line": "true"})]
        self.runsParapet()
        
    def parapetCases(self, pn_windward, pn_leeward, calcs = False):
        if calcs:
            self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_PARAPET_CALC])
            self.runs.append(self.run_parts[WindDesignConsts.P])
        else:
            self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_PARAPET])
            self.runs.append(self.run_parts[WindDesignConsts.PN])

        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(pn_windward, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])

        if calcs:
            self.runs.append(self.run_parts[WindDesignConsts.LEEWARD_PARAPET_CALC])
            self.runs.append(self.run_parts[WindDesignConsts.P])
        else:
            self.runs.append(self.run_parts[WindDesignConsts.LEEWARD_PARAPET])
            self.runs.append(self.run_parts[WindDesignConsts.PN])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(pn_leeward, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])

        self.wind_design.zone += 2

    def runsParapet(self):
        self.runs.append(self.run_parts[WindDesignConsts.PARAPET_TITLE])

        #wind load_parapet cases
        if self.calcs:
            self.parapetCases(self.wind_design.windLoad(self.pn_windward), 
                self.wind_design.windLoad(self.pn_leeward), True)
        else:
            self.parapetCases(self.pn_windward, self.pn_leeward)



from gen_desc.run_properties import RunProperties
from .wind_parapets import WindParapets
from .constants import WindDesignConsts

class WindDesignPartsY:
    def __init__(self, wind_design):
        self.wind_design = wind_design
        self.template_data = wind_design.data_y
        self.wind_factors = wind_design.wind_factors_y
        self.runs = []
        self.run_parts = self.getRunParts()
        self.loadCoeffiecients()
        self.windmap_values = []

        #Make the paragraph runs
        self.directionalRuns()
        self.addParapetRuns()
        
    def addParapetRuns(self):
        if (self.wind_design.parapet_load == "true"):
            # self.runsParapet()
            runs_parapets = WindParapets(self.wind_design, self.run_parts, 
                self.pn_windward, self.pn_leeward)
            self.runs.extend(runs_parapets.runs)
        
    def getRunParts(self):
        run_parts = {}
        for part_name, parts in self.template_data.items():
            for text, props in parts.items():
                run_parts[part_name] = RunProperties(text, props)
                pass
        
        #add parts from common
        for part_name, parts in self.wind_design.data_common.items():
            for text, props in parts.items():
                run_parts[part_name] = RunProperties(text, props)
                pass

        return run_parts

    def windCases(self, cnw = 1, cnl = 1, title=None):
        '''
        Method to calculate wind cases
        Title is used when the wind cases are calculated. See child class
        '''
        self.runs.append(self.run_parts[WindDesignConsts.CASE_A])
        self.runs.append(self.run_parts[WindDesignConsts.NW])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(cnw, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.runs.append(self.run_parts[WindDesignConsts.CASE_B])
        self.runs.append(self.run_parts[WindDesignConsts.NL])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(cnl, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.wind_design.zone += 2

    def directionalRuns(self):
        #Runs in positive direction
        self.runs.append(self.run_parts[WindDesignConsts.TITLE])
        self.runsInDirection()

        #Runs in negative direction
        self.runs.append(self.run_parts[WindDesignConsts.TITLE_MINUS])
        self.runsInDirection()

    def runsInDirection(self):
        '''
        Runs in particular direction are similar.
        Thse are similar for both negative and positive direction

        '''

        #wind load windward_05
        title = self.wind_design.windmap_defaults[WindDesignConsts.WIND_Y_05]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_O5])
        self.windCases(self.cnw_05, self.cnl_05, title)

        #wind load windward_05L
        title = self.wind_design.windmap_defaults[WindDesignConsts.WIND_Y_05L]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_O5])
        self.windCases(self.cnw_05L, self.cnl_05L, title)

    def loadCoeffiecients(self):
        
        factors_05 = self.wind_factors[WindDesignConsts.WINDWARD_O5]
        factors_05L = self.wind_factors[WindDesignConsts.WINDWARD_05_L]
        factors_parapets = self.wind_factors[WindDesignConsts.PARAPETS]
        
        self.cnw_05 = factors_05[WindDesignConsts.CASE_A]
        self.cnl_05 = factors_05[WindDesignConsts.CASE_B]

        self.cnw_05L = factors_05L[WindDesignConsts.CASE_A]
        self.cnl_05L = factors_05L[WindDesignConsts.CASE_B]

        self.pn_windward = factors_parapets[WindDesignConsts.WINDWARD]
        self.pn_leeward = factors_parapets[WindDesignConsts.LEEWARD]

        # for value in self.wind_factors.values():
    

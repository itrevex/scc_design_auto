from gen_desc.run_properties import RunProperties
from .wind_parapets import WindParapets
from .constants import WindDesignConsts
from .internal_pressure import InternalPressure

class WindDesignPartsX:
    def __init__(self, wind_design, y_values = False):
        self.wind_design = wind_design
        self.template_data = wind_design.data_x
        self.wind_factors = wind_design.wind_factors_x

        if self.wind_design.enclosed and y_values:
            self.template_data = wind_design.data_y
            # self.wind_factors = wind_design.wind_factors_y

        self.runs = []
        self.run_parts = self.getRunParts()
        self.windmap_values = []

        if self.wind_design.enclosed:
            self.loadCoeffiecientsClosed()
        else:
            self.loadCoeffiecients()

        self.height = float(wind_design.props[WindDesignConsts.HEIGHT]) \
            * WindDesignConsts.ONE_M_IN_MM
        self.length_x = float(wind_design.props[WindDesignConsts.LENGTH_X])

        #create doc runs
        self.directionalRuns()
        
        
    def addParapetRuns(self):
        if (self.wind_design.parapet_load == "true"):
            # self.runsParapet()
            runs_parapets = WindParapets(self.wind_design, self.run_parts, 
                self.pn_windward, self.pn_leeward)
            self.runs.extend(runs_parapets.runs)

    def addInternalPressures(self):
        if (self.wind_design.enclosed == True):
            runs_parapets = InternalPressure(self.wind_design, 0.18)
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

    def windCases(self, case_a = 1, case_b = 1, title=None):
        self.runs.append(self.run_parts[WindDesignConsts.CASE_A])
        self.runs.append(self.run_parts[WindDesignConsts.N])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(case_a, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.runs.append(self.run_parts[WindDesignConsts.CASE_B])
        self.runs.append(self.run_parts[WindDesignConsts.N])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(case_b, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        self.wind_design.zone += 2

    def windCasesClosed(self, cp = 1, title=None):
        self.runs.append(self.run_parts[WindDesignConsts.CASE_A])
        self.runs.append(self.run_parts[WindDesignConsts.P_SUB])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(cp, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        
        self.wind_design.zone += 1

    def directionalRuns(self):
        #Runs in positive direction
        self.runs.append(self.run_parts[WindDesignConsts.TITLE])
        if self.windCasesClosed:
            self.runInDirectionClosed()
        else:
            self.runsInDirection()
        
        #Runs in negative direction
        self.runs.append(self.run_parts[WindDesignConsts.TITLE_MINUS])
        if self.windCasesClosed:
            self.runInDirectionClosed()
        else:
            self.runsInDirection()
        self.addInternalPressures()
        
    def runInDirectionClosed(self):
        '''
        Runs in particular direction are similar.
        Thse are similar for both negative and positive direction

        '''
        #wind load leeward_<=h/2
        title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_1]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_H])
        self.windCasesClosed(self.cp_1, title)

        #wind load leeward_h/2_h
        title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_2]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_H_2H])
        self.windCasesClosed(self.cp_2, title)
            

        #wind load leeward_h_2h
        title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_3]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_2H])
        self.windCasesClosed(self.cp_3, title)

        #wind load leeward_>_2h
        title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_4]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_2H])
        self.windCasesClosed(self.cp_4, title)
            

        self.addParapetRuns()
        pass

    def runsInDirection(self):
        '''
        Runs in particular direction are similar.
        Thse are similar for both negative and positive direction

        '''
        #wind load leeward_h
        title = self.wind_design.windmap_defaults[WindDesignConsts.WIND_X_H]
        self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_H])
        self.windCases(self.h_case_a, self.h_case_b, title)

        #wind load leeward_h_2h
        #show if 2*h => x_length
        if self.length_x > self.height:
            title = self.wind_design.windmap_defaults[WindDesignConsts.WIND_X_H_2H]
            self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_H_2H])
            self.windCases(self.h_2h_case_a, self.h_2h_case_b, title)

        #wind load leeward_2h
        #show if 2*h > x_length
        if self.length_x > 2 * self.height:
            title = self.wind_design.windmap_defaults[WindDesignConsts.WIND_X_2H]
            self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_2H])
            self.windCases(self._2h_case_a, self._2h_case_b, title)

        self.addParapetRuns()
        
    def loadCoeffiecients(self):
        
        factors_h = self.wind_factors[WindDesignConsts.WINDWARD_H]
        factors_h_2h = self.wind_factors[WindDesignConsts.WINDWARD_H_2H]
        factors_2h = self.wind_factors[WindDesignConsts.WINDWARD_2H]
        factors_parapets = self.wind_factors[WindDesignConsts.PARAPETS]

        self.h_case_a = factors_h[WindDesignConsts.CASE_A]
        self.h_case_b = factors_h[WindDesignConsts.CASE_B]

        self.h_2h_case_a = factors_h_2h[WindDesignConsts.CASE_A]
        self.h_2h_case_b = factors_h_2h[WindDesignConsts.CASE_B]


        self._2h_case_a = factors_2h[WindDesignConsts.CASE_A]
        self._2h_case_b = factors_2h[WindDesignConsts.CASE_B]

        self.pn_windward = factors_parapets[WindDesignConsts.WINDWARD]
        self.pn_leeward = factors_parapets[WindDesignConsts.LEEWARD]

    def loadCoeffiecientsClosed(self):
        
        factors_parapets = self.wind_factors[WindDesignConsts.PARAPETS]

        self.cp_1 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_1]
        self.cp_2 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_2]
        self.cp_3 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_3]
        self.cp_4 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_4]

        self.pn_windward = factors_parapets[WindDesignConsts.WINDWARD]
        self.pn_leeward = factors_parapets[WindDesignConsts.LEEWARD]


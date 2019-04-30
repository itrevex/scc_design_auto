from gen_desc.run_properties import RunProperties
from .wind_parapets import WindParapets
from .constants import WindDesignConsts
from .internal_pressure import InternalPressure
from .load_combinations import LoadCombinations

class WindDesignPartsX(LoadCombinations):
    def __init__(self, wind_design, y_values = False):
        super().__init__(wind_design)
        self.wind_design = wind_design
        self.template_data = wind_design.data_x
        self.wind_factors = wind_design.wind_factors_x
        self.y_values = y_values

        self.setUpCombinations()
        self.negative_direction = False
        
        self.height = float(wind_design.props[WindDesignConsts.HEIGHT]) \
            * WindDesignConsts.ONE_M_IN_MM
        self.length_x = float(wind_design.props[WindDesignConsts.LENGTH_X])
        self.length_y = float(wind_design.props[WindDesignConsts.LENGTH_Y])
        self.length = self.length_x

        if self.wind_design.enclosed and y_values:
            self.template_data = wind_design.data_y
            self.length = self.length_y
            # self.wind_factors = wind_design.wind_factors_y

        self.runs = []
        self.run_parts = self.getRunParts()
        self.windmap_values = []

        if self.wind_design.enclosed:
            self.loadCoeffiecientsClosed()
        else:
            self.loadCoeffiecients()

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

        #case B data
        self.runs.append(self.run_parts[WindDesignConsts.CASE_B])
        self.runs.append(self.run_parts[WindDesignConsts.N])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(case_b, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone + 1, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])

        self.storeAllCombinatios()

        self.wind_design.zone += 2

    def storeAllCombinatios(self):
        if self.negative_direction:
            self.storeCombinationsNeg()
        else:
            self.storeCombinations()

    def windCasesClosed(self, cp = 1, title=None):
        self.runs.append(self.run_parts[WindDesignConsts.CASE_A])
        self.runs.append(self.run_parts[WindDesignConsts.P_SUB])
        self.runs.append(self.run_parts[WindDesignConsts.EQUALS])
        self.runs.append(RunProperties(cp, {}))
        self.runs.append(self.run_parts[WindDesignConsts.ZONE])
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        self.runs.append(self.run_parts[WindDesignConsts.BRACKET])
        
        self.storeAllCombinatios()
        
        self.wind_design.zone += 1

    def directionalRuns(self):
        #Runs in positive direction
        self.runs.append(self.run_parts[WindDesignConsts.TITLE])
        self.negative_direction = False
        if self.wind_design.enclosed:
            self.runInDirectionClosed()
        else:
            self.runsInDirection()
            

        #Runs in negative direction
        self.runs.append(self.run_parts[WindDesignConsts.TITLE_MINUS])
        self.negative_direction = True
        if self.wind_design.enclosed:
            self.runInDirectionClosed()
        else:
            self.runsInDirection()
            

        if self.y_values:
            self.addInternalPressures()
    
    def runInDirectionClosed(self):
        '''
        Runs in particular direction are similar.
        Thse are similar for both negative and positive direction

        '''
        #wind load leeward <h/2
        title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_1]
        self.runs.append(self.run_parts[WindDesignConsts.WINDMAP_CLOSED_1])
        self.windCasesClosed(self.cp_1, title)
        length = self.length
        
        #wind load leeward h/2 to h
        if length > self.height/2:
            title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_2]
            run_title = self.run_parts[WindDesignConsts.WINDMAP_CLOSED_2]
            if (self.h_l > 1.0):
                title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_5]
                run_title = self.run_parts[WindDesignConsts.WINDMAP_CLOSED_5]
                
            self.runs.append(run_title)
            self.windCasesClosed(self.cp_2, title)
            

        #wind load leeward h to 2h
        if length > self.height:
            title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_3]
            self.runs.append(self.run_parts[WindDesignConsts.WINDMAP_CLOSED_3])
            self.windCasesClosed(self.cp_3, title)

        #wind load leeward >2h
        if length > 2 * self.height:
            title = self.wind_design.windmap_defaults[WindDesignConsts.TITLE_CLOSED_4]
            self.runs.append(self.run_parts[WindDesignConsts.WINDMAP_CLOSED_4])
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
        if self.length > self.height:
            title = self.wind_design.windmap_defaults[WindDesignConsts.WIND_X_H_2H]
            self.runs.append(self.run_parts[WindDesignConsts.WINDWARD_H_2H])
            self.windCases(self.h_2h_case_a, self.h_2h_case_b, title)

        #wind load leeward_2h
        #show if 2*h > x_length
        if self.length > 2 * self.height:
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

        #check h/L and modify cp_1 and cp_2
        self.h_l = self.height / self.length
        area = (self.length_x * self.length_y) / 1e6
        
        if (self.h_l >= 1.0):
            self.cp_1 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_5]
            if (area <= 9.3):
                self.cp_1 = self.cp_1 * 1.0
            elif(area > 9.3 and area < 92.9):
                self.cp_1 = self.cp_1 * 0.9
            elif(area >= 92.9):
                self.cp_1 = self.cp_1 * .8

            self.cp_2 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_6]

        self.cp_3 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_3]
        self.cp_4 = self.wind_factors[WindDesignConsts.WINDWARD_CLOSED_4]

        self.pn_windward = factors_parapets[WindDesignConsts.WINDWARD]
        self.pn_leeward = factors_parapets[WindDesignConsts.LEEWARD]


from libs.constants import Constants
from .constants import WindDesignConsts
from .wind_x import WindDesignPartsX
from .wind_y import WindDesignPartsY
from .wind_calc_x import WindCalculationsX
from .wind_calc_y import WindCalculationsY
from .wind_loads import WindLoads

class WindDesign:
 
    def __init__(self, app_data):

        self.wind_defaults = app_data.getWindDesignDefaults()
        self.app_data = app_data
        self.props = app_data.getInputValues()
        self.wind_load = WindLoads(app_data, self).wind_unit_load_kn
        self.internal_pressure_zone_ps = {}
        self.roof_angle = self.props[WindDesignConsts.ROOF_ANGLE]
        self.parapet_load = self.props[WindDesignConsts.PARAPET_LOAD]
        self.enclosed = self.props[Constants.ROOF_ENCLOSURE] == 'closed'
        self.data_common = self.wind_defaults[WindDesignConsts.COMMON]
        self.data_x = self.wind_defaults[WindDesignConsts.ALONG_X]
        self.data_y = self.wind_defaults[WindDesignConsts.ALONG_Y]
        if self.enclosed:
            self.data_y = self.wind_defaults[WindDesignConsts.ALONG_Y_CLOSED]
            self.wind_factors_x = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_X_CLOSED]
        else:
            self.wind_factors_x = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_X]
        
        self.wind_factors_y = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_Y]
        self.windmap_defaults = app_data.getWindMapDefaults()[WindDesignConsts.ASCE_7_10]
        self.zone = 804
        self.current_combination = 5
        self.combinations = {}
        self.pressure_combinations = {}
        self.getWindDesignValues()
        pass
    
    def getWindDesignValues(self):
        #The order in which these methods are called is important
        self.wind_x =  WindDesignPartsX(self)
        if self.enclosed:
            self.wind_y =  WindDesignPartsX(self, True)
        else:
            self.wind_y = WindDesignPartsY(self)

        self.wind_calc_x = WindCalculationsX(self)

        if self.enclosed:
            self.wind_calc_y = WindCalculationsX(self, True)
        else:
            self.wind_calc_y = WindCalculationsY(self)

    def resetZone(self):
        self.zone = 804

    def windLoad(self, wind_factor):
        load = float(wind_factor) * self.wind_load \
        * WindDesignConsts.WIND_FACTOR

        return "{:.4f}".format(load)
     
    def trials(self):
        # self.plotWindMap(self.app_data)
        pass
        
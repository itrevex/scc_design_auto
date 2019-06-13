from libs.general_methods import GeneralMethods
from libs.constants import Constants

class WindLoads:
    def __init__(self, app_data, wind_design):
        self.app_data = app_data
        self.new_input_values = wind_design.props
        self.calculateParameters()
    
    def calcKzValue(self):
        height_above_ground = self.new_input_values[Constants.HEIGHT_ABOVE_GROUND]
        self.kz = GeneralMethods(self.app_data).kzValue(float(height_above_ground))
        self.kz_text = GeneralMethods.kzValueText(self.kz)

    def calcSpeedMs(self):
        #calcualted wind speed in m/s and return value
        #first get wind_speed value from input
        wind_speed = self.new_input_values[Constants.WIND_SPEED]
        self.speed_ms, self.speed_text = GeneralMethods.windSpeedMPerSecond(wind_speed)

    def calcWindUnitLoad(self):
        self.wind_unit_load = GeneralMethods.calcWindUnitLoad(self.speed_ms, self.kz)
        self.wind_unit_load_text = GeneralMethods.windUnitLoadText(self.wind_unit_load)

    def calcWindUnitLoadKn(self):
        self.wind_unit_load_kn =  self.wind_unit_load/1000.
        self.wind_unit_load_kn_text = GeneralMethods.textFourPlaces(self.wind_unit_load_kn)

    def calculateParameters(self):
        self.calcSpeedMs()
        self.calcKzValue()
        self.calcWindUnitLoad()
        self.calcWindUnitLoadKn()


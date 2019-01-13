class Constants:
    
    # document value template file object constants
    TEMPLATE_IDENTIFIER = "identifier"
    REPLACE_ENTIRE_PARAGRAPH = "replace_entire_paragraph"
    TRUE = "true"

    # document table template file object constants

    '''
    parameters json appearance
        " kN/m": {
            "input_from": "",
            "bold": "",
            "italic": "",
            "underline": "",
            "subscript": "",
            "superscript": "",
            "end_of_line": ""
        }
    '''
    
    VALUE_PARTS = "value_parts"
    INPUT_FROM = "input_from"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    SUBSCRIPT = "subscript"
    SUPERSCRIPT = "superscript"
    END_OF_LINE = "end_of_line"
    INPUT_FROM_INPUT = "input"
    INPUT_FROM_CALCULATION = "calculation"

    #Calculation value constants
    WIND_SPEED = "wind_speed"
    WIND_SPEED_MS = "wind_speed_ms"
    HEIGHT_ABOVE_GROUND = "height_above_ground_level_in_m"
    KZ_VALUE = "kz_value"
    WIND_UNIT_LOAD = "wind_unit_load"
    WIND_UNIT_LOAD_KN = "wind_unit_load_kn_m"

    def __init__(self, app_data):
        self.app_data = app_data

    def windSpeedMPerSecond(speed_km_per_s):
        '''
        1000 value of 1km in m
        3600 value of 1hr in seconds
        speed_km_per_s speed in km/s
        '''
        wind_speed = (float(speed_km_per_s) * 1000) / 3600

        return wind_speed, "{:.2f}".format(wind_speed)

    def windSpeedMPerSecondText(wind_speed):
        return "{:.2f}".format(wind_speed)

    def kzValueText(kz_value):
        return "{:.2f}".format(kz_value)

    def kzValue(self, height_above_ground):
        self.table_27_3_1 = self.app_data.getTable27_3_1()
        min_value, max_value = self.minMaxKzValue(height_above_ground)
        if (max_value == None):
            return float(self.table_27_3_1[min_value])

        return self.kzInterpolation(min_value, max_value, height_above_ground)

    def minMaxKzValue(self, height_above_ground):
        '''
        Get the sealing values for interpolation
        '''
        max_value = None
        min_value, isExact = self.getMinimumValue(height_above_ground)
        # if value is exact, then there is no need to find maximum value
        if (isExact == False):
            max_value = self.getMaximumValue(height_above_ground)

        return min_value, max_value

    def kzInterpolation(self, min_value, max_value, height_above_ground):
        x1 = float(min_value)
        x2 = height_above_ground
        x3 = float(max_value)
        y1 = self.table_27_3_1[min_value]
        y3 = self.table_27_3_1[max_value]

        return (((x2-x1)/(x3-x1))*(y3-y1))+y1
        
    def getMinimumValue(self, sealing):
        '''
        second variable returned identifies if value return
        exactly matches the value within the list
        '''
        min_value = "0."
        for key in self.table_27_3_1:
            value = float(key)
            if (value == sealing): 
                return key, True

            if (value < sealing):
                if(value > float(min_value)):
                    min_value = key
        
        return min_value, False

    def getMaximumValue(self, sealing):
        '''
        second variable returned identifies if value return
        exactly matches the value within the list
        '''
        max_value = "10000." #random big value to start with
        for key in self.table_27_3_1:
            value = float(key)

            if (value > sealing):
                if(value < float(max_value)):
                    max_value = key
        
        return max_value

    def calcWindUnitLoad(wind_speed, kz):
        return 0.613* kz* 1.00* 0.85* wind_speed* wind_speed

    def windUnitLoadText(wind_unit_load):
        return "{:.2f}".format(wind_unit_load)

    def textFourPlaces(float_value):
        return "{:.4f}".format(float_value)
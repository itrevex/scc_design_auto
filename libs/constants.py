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

    def kzValue(heightAboveGround):
        min_value, max_value = minMaxKzValue(heightAboveGround)
        if (max_value == None):
            return float(min_value)

        return kzInterpolation(min_value, max_value, heightAboveGround)

    def minMaxKzValue(heightAboveGround):
        '''
        Get the sealing values for interpolation
        '''
        max_value = None
        min_value, isExact = getMinimumValue(table_27_3_1, heightAboveGround)
        # if value is exact, then there is no need to find maximum value
        if (isExact == False):
            max_value = getMaximumValue(table_27_3_1, heightAboveGround)

        return min_value, max_value

    def kzInterpolation(min_value, max_value, heightAboveGround):
        x1 = float(min_value)
        x2 = heightAboveGround
        x3 = float(max_value)
        y1 = table_27_3_1[min_value]
        y3 = table_27_3_1[max_value]

        return (((x2-x1)/(x3-x1))*(y3-y1))+y1
        
    def getMinimumValue(list, sealing):
        '''
        second variable returned identifies if value return
        exactly matches the value within the list
        '''
        min_value = "0."
        for key in table_27_3_1:
            value = float(key)
            if (value == sealing): 
                return key, True

            if (value < sealing):
                if(value > float(min_value)):
                    min_value = key
        
        return min_value, False

    def getMaximumValue(list, sealing):
        '''
        second variable returned identifies if value return
        exactly matches the value within the list
        '''
        max_value = "10000." #random big value to start with
        for key in table_27_3_1:
            value = float(key)

            if (value > sealing):
                if(value < float(max_value)):
                    max_value = key
        
        return max_value

    def calcWindUnitLoad(wind_speed, kz):
        return 0.613* kz* 1.00* 0.85* wind_speed* wind_speed

    def windUnitLoatText(wind_unit_load):
        return "{:.4f}".format(wind_unit_load)
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
    ROOF_ENCLOSURE = "enclosure_specification"
    INTERNAL_PRESSURE_VALUE = "internal_pressure_value"

    #Wind design parameters and constants
    WIND_DESIGN_X = "wind_design_x"
    WIND_DESIGN_Y = "wind_design_y"
    WIND_DESIGN_CALC_X = "wind_design_calculation_x"
    WIND_DESIGN_CALC_Y = "wind_design_calculation_y"

    #ROOF TYPE
    OPEN_ROOF = "open"
    ENCLOSED_ROOF = "closed"

    #Design Codes
    ASCE_710_ASD = "710_asd"
    ASCE_710_LRFD = "710_lrfd"

    #INPUT PARAMETERS
    ROOF_DEAD_LOAD = "roof_dead_load"
    SERVICES_LOAD = "services_load"
    ROOF_LIVE_LOAD = "roof_live_load"
    

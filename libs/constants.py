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

    #Wind design parameters and constants
    WIND_DESIGN_X = "wind_design_x"
    WIND_DESIGN_ALONG_X = "along_x"
    WIND_DESIGN_TITLE = "title"
    WIND_DESIGN_TITLE_MINUS = "title_minus"
    WIND_DESIGN_WINDWARD_O5 = "windward_0.5"
    WIND_DESIGN_WINDWARD_05_L = "windward_0.5_L"
    WIND_DESIGN_LEEWARD_05 = "leeward_0.5"
    WIND_DESIGN_LEEWARD_05_L = "leeward_0.5_L"
    WIND_DESIGN_CASE_A = "case_a"
    WIND_DESIGN_CASE_B = "case_b"
    WIND_DESIGN_ZONE = "zone"
    WIND_DESIGN_BRACKET = "bracket"
    WIND_DESIGN_NW = "nw"
    WIND_DESIGN_NL = "nl"
    WIND_DESIGN_EQUALS = "equals"

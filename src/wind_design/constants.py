class WindDesignConsts:
    '''
    Runs are paragragh runs, see run properties for details about runs
    '''

    #General
    ASCE_7_10 = "asce_7_10"

    #Multiplication factors
    ONE_M_IN_MM = 1000.
    
    #Common data
    COMMON = "common"
    CASE_A = "case_a"   
    CASE_B = "case_b"
    ZONE = "zone"
    BRACKET = "bracket"
    P = "p"
    ZONE_CALC = "zone_calc"
    CASE_A_CALC = "case_a_calc"
    CASE_B_CALC = "case_b_calc"
    EQUALS = "equals"

    #wind design x constants
    ALONG_X = "along_x"
    ALONG_X_CLOSED = "along_x_closed"
    TITLE = "title"
    TITLE_MINUS = "title_minus"
    WINDWARD_O5 = "windward_0.5"
    WINDWARD_05_L = "windward_0.5_L"
    LEEWARD_05 = "leeward_0.5"
    LEEWARD_05_L = "leeward_0.5_L"
    NW = "nw"
    NL = "nl"

    #CLOSED VALUES
    WINDWARD_CLOSED_1 = "windward_1"
    WINDWARD_CLOSED_2 = "windward_2"
    WINDWARD_CLOSED_3 = "windward_3"
    WINDWARD_CLOSED_4 = "windward_4"
    WINDWARD_CLOSED_5 = "windward_5"
    WINDWARD_CLOSED_6 = "windward_6"
    
    #wind design y constants
    ALONG_Y = "along_y"
    ALONG_Y_CLOSED = "along_y_closed"
    WINDWARD_H = "windward_h"
    WINDWARD_H_2H = "windward_h_2h"
    WINDWARD_2H = "windward_2h"
    LEEWARD_H = "leeward_h"
    LEEWARD_H_2H = "leeward_h_2h"
    LEEWARD_2H = "leeward_2h"
    N = "n"
    P_SUB = "p_sub"
    WIND_FACTOR = 0.85

    #Parapets
    PARAPETS = "parapets"
    WINDWARD = "windward"
    LEEWARD = "leeward"
    PARAPET_TITLE = "parapet_title"
    WINDWARD_PARAPET = "windward_parapet"
    LEEWARD_PARAPET = "leeward_parapet"
    WINDWARD_PARAPET_CALC = "windward_parapet_calc"
    LEEWARD_PARAPET_CALC = "leeward_parapet_calc"
    PN = "pn"

    #Input values
    ROOF_ANGLE = "roof_angle"
    PARAPET_LOAD = "parapet_load"
    LENGTH_X = "roof_x_length"
    LENGTH_Y = "roof_y_length"
    HEIGHT = "height_above_ground_level_in_m"


    #WIND_MAP_DEFAULTS
    WIND_Y_05 = "wind_y_05"
    WIND_Y_05L = "wind_y_05L"
    WIND_X_H = "wind_x_h"
    WIND_X_H_2H = "wind_x_h_2h"
    WIND_X_2H = "wind_x_2h"
    PARAPET_SECTION = "parapet_section"
    THETA = "theta"

    # WINDMAP DEFAULTS CLOSED
    TITLE_CLOSED_1 = "wind_x_h2_closed"
    TITLE_CLOSED_2 = "wind_x_h2_h_closed"
    TITLE_CLOSED_3 = "wind_x_h_2h_closed"
    TITLE_CLOSED_4 = "wind_x_2h_closed"
    TITLE_CLOSED_5 = "wind_x_h2h2_closed"

    WINDMAP_CLOSED_1 = "wind_title_1"
    WINDMAP_CLOSED_2 = "wind_title_2"
    WINDMAP_CLOSED_3 = "wind_title_3"
    WINDMAP_CLOSED_4 = "wind_title_4"
    WINDMAP_CLOSED_5 = "wind_title_5"

    #WIMDMAP PARAPET CONSTANTS
    WINDWARD_PARAPET_TITLE = "Windward parapet"
    LEEWARD_PARAPET_TITLE = "Leeward parapet"
    PARAPET_SECTION_TITLE = "Sec. 27.4.5"
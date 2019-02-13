from gen_desc.run_properties import RunProperties
from .windmap_value import WindMapValue
from .wind_parapets import WindParapets
from .constants import WindDesignConsts
from .wind_x import WindDesignPartsX
from .wind_y import WindDesignPartsY
from .wind_calc_x import WindCalculationsX
from .wind_calc_y import WindCalculationsY

class WindDesign:
 
    def __init__(self,app_data, wind_load=1.0, parapet_load = "false", angle=0):
        self.app_data = app_data.getWindDesignDefaults()
        self.wind_load = wind_load
        self.roof_angle = angle
        self.parapet_load = parapet_load
        self.data_common = self.app_data[WindDesignConsts.COMMON]
        self.data_x = self.app_data[WindDesignConsts.ALONG_X]
        self.data_y = self.app_data[WindDesignConsts.ALONG_Y]
        self.wind_factors_x = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_X]
        self.wind_factors_y = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_Y]
        self.windmap_defaults = app_data.getWindMapDefaults()[WindDesignConsts.ASCE_7_10]
        
        self.zone = 804
        self.getWindDesignValues()
        
        pass
    
    def getWindDesignValues(self):
        self.wind_x =  WindDesignPartsX(self)
        self.wind_y = WindDesignPartsY(self)
        self.wind_calc_x = WindCalculationsX(self)
        self.wind_calc_y = WindCalculationsY(self)

    def resetZone(self):
        self.zone = 804

    def windLoad(self, wind_factor):
        load = float(wind_factor) * self.wind_load \
        * WindDesignConsts.WIND_FACTOR

        return "{:.4f}".format(load)
    
    def trials(self):
        print("Trials method called . . .")
        print(self.windmap_defaults)
        for value in self.wind_calc_y.windmap_values:
            print(value.toString())
    
    def setWindMapDefaults(self, windmap_value):
        windmap_value.setRoofAngle(self.roof_angle)

        plot_lines = []
        plot_lines.append(windmap_value.title)
        plot_lines.append("$θ = %s˚$"%windmap_value.roof_angle)
        plot_lines.append("$CASE A: C_N = %.1f$"%windmap_value.c_case_a)
        plot_lines.append("$P = %skN/sq.m$"%windmap_value.p_case_a)
        plot_lines.append("$Zone: %d$"%windmap_value.zone_case_a)
        plot_lines.append("")
        plot_lines.append("$CASE B: C_N = %.1f$"%windmap_value.c_case_b)
        plot_lines.append("$Zone: %d$"%windmap_value.zone_case_a)

        windmap_value.setPlotLines(plot_lines)
        pass
             
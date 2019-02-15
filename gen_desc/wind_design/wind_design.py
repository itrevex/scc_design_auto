from gen_desc.plot.plot_windmap import PlotWindMap
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
        # self.plotWindMap()
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
    
    def plotWindMap(self):
        wind_texts = []
        wind_texts.extend(self.getPlotLines(self.wind_calc_x.windmap_values))
        wind_texts.extend(self.getPlotLines(self.wind_calc_y.windmap_values))

        windmap_plot = PlotWindMap(wind_texts)
        windmap_plot.plotMap()
     
    def getPlotLines(self, windmap_values):
        wind_texts = []
        for windmap_value in windmap_values:
            wind_texts.append(windmap_value.plot_lines)
        return wind_texts

    def trials(self):
        # for value in self.wind_calc_x.windmap_values:
        #     print(value.toString())
        self.plotWindMap()
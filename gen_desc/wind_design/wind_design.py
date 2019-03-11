from gen_desc.plot.plot_windmap import PlotWindMap
from .constants import WindDesignConsts
from .wind_x import WindDesignPartsX
from .wind_y import WindDesignPartsY
from .wind_calc_x import WindCalculationsX
from .wind_calc_y import WindCalculationsY

class WindDesign:
 
    def __init__(self, app_data, props, wind_load):
        self.wind_defaults = app_data.getWindDesignDefaults()
        self.app_data = app_data
        self.wind_load = wind_load
        self.roof_angle = props[WindDesignConsts.ROOF_ANGLE]
        self.parapet_load = props[WindDesignConsts.PARAPET_LOAD]
        self.props = props
        self.data_common = self.wind_defaults[WindDesignConsts.COMMON]
        self.data_x = self.wind_defaults[WindDesignConsts.ALONG_X]
        self.data_y = self.wind_defaults[WindDesignConsts.ALONG_Y]
        self.wind_factors_x = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_X]
        self.wind_factors_y = app_data.getWindCoeffiecients()[WindDesignConsts.ALONG_Y]
        self.windmap_defaults = app_data.getWindMapDefaults()[WindDesignConsts.ASCE_7_10]
        self.zone = 804
        self.getWindDesignValues()
        self.printWindMaps()
        self.plotWindMap(app_data)
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
    
    def plotWindMap(self, app_data):
        wind_texts = []
        wind_texts.extend(self.getPlotLines(self.wind_calc_x.windmap_values))
        wind_texts.extend(self.getPlotLines(self.wind_calc_y.windmap_values))
        for value in self.wind_calc_x.windmap_values:
            print(value.toString())

        windmap_plot = PlotWindMap(wind_texts, app_data)
        windmap_plot.plotMap()
     
    def getPlotLines(self, windmap_values):
        wind_texts = []
        for windmap_value in windmap_values:
            wind_texts.append(windmap_value.plot_lines)
        return wind_texts

    def trials(self):
        self.plotWindMap(self.app_data)
        pass
        
    def printWindMaps(self):
        print("Writing loads to a file . . .")
        values_x = self.getZonePValues(self.wind_calc_x)
        values_y = self.getZonePValues(self.wind_calc_y)
        zone_p_values = { **values_x, **values_y }
        p_values = sorted(set(zone_p_values.values()), key=float)
        # print(zone_p_values)
        loads_file = self.app_data.getLoadsFile()

        for value in reversed(p_values):
            value_zones = [zone for zone in zone_p_values.keys() if value == zone_p_values[zone]]
            loads_file.write(str(value))
            loads_file.write("\n"+",".join(str(x) for x in value_zones))
            loads_file.write("\n\n")
        #close file after using it
        loads_file.close()
        pass

    def getZonePValues(self, wind_calc):
        zone_p_values = {} 
        for value in wind_calc.windmap_values:
            zone_p_values.update(value.zone_ps)

        return zone_p_values
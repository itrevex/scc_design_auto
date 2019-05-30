from .plot_windmap import PlotWindMap

class Windmap:
    def __init__(self, wind_design):
        self.windmap_values_x = wind_design.wind_calc_x.windmap_values
        self.windmap_values_y = wind_design.wind_calc_y.windmap_values
        self.wind_texts = []
        self.prepareValues()
    
        pass

    def prepareValues(self):
        self.wind_texts.extend(self.getPlotLines(self.windmap_values_x))
        self.wind_texts.extend(self.getPlotLines(self.windmap_values_y))

        
    def plotWindMap(self, app_data):
        windmap_plot = PlotWindMap(self.wind_texts, app_data)
        windmap_plot.plotMap()

    def getPlotLines(self, windmap_values):
        wind_texts = []
        for windmap_value in windmap_values:
            wind_texts.append(windmap_value.plot_lines)
        return wind_texts

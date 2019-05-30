class PlotLoads:
    def __init__(self, wind_design):
        self.wind_design = wind_design
        self.wind_calc_x = wind_design.wind_calc_x
        self.wind_calc_y = wind_design.wind_calc_y
        pass

    def plotLoads(self, app_data):
        print("Creating loads summary file . . .")
        values_x = self.getZonePValues(self.wind_calc_x)
        values_y = self.getZonePValues(self.wind_calc_y)
        internal_pressure = self.wind_design.internal_pressure_zone_ps
        
        zone_p_values = { **values_x, **values_y, **internal_pressure}
        p_values = sorted(set(zone_p_values.values()), key=float)
        
        # print(zone_p_values)
        loads_file = app_data.getLoadsFile()

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

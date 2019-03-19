from gen_desc.run_properties import RunProperties
from .constants import WindDesignConsts

class InternalPressure:
    def __init__(self, wind_design, value, calc=False):
        self.wind_design = wind_design
        self.runs = []
        self.calc = calc
        self.value = self.getValue(value)
        self.positivePressure()
        self.negativePressure()
        pass

    def getValue(self, value):
        if (self.calc):
            load = float(value) * self.wind_design.wind_load
            # return "{:.4f}".format(load)
            return "{:.4f}".format(load)
        return str(value)

    def positivePressure(self):
        props = {
            "underline": "true",
            "end_of_line": "true"
        }
        text = "Positive Internal Pressure"
        self.runs.append(RunProperties(text, props))
        text = "           p =  "
        self.runs.append(RunProperties(text, {}))
        self.runs.append(RunProperties(self.value, {}))
        if(self.calc):
            text = "kN/m"
            text2 = "2 "
        else:
            text= " "
            text2 = ""
        self.runs.append(RunProperties(text, {}))
        text = "2"
        self.runs.append(RunProperties(text2, {"superscript": "true"}))
        text = "[Zone:"
        self.runs.append(RunProperties(text, {}))
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        text = "]"
        self.runs.append(RunProperties(text, {"end_of_line": "true"}))
        self.runs.append(RunProperties("", {"end_of_line": "true"}))
        self.wind_design.zone += 1
        pass

    def negativePressure(self):
        props = {
            "underline": "true",
            "end_of_line": "true"
        }
        text = "Negative Internal Pressure"
        self.runs.append(RunProperties(text, props))
        text = "           p =  "
        self.runs.append(RunProperties(text, {}))
        self.runs.append(RunProperties("-"+self.value, {}))
        if(self.calc):
            text = "kN/m"
            text2 = "2 "
        else:
            text= " "
            text2 = ""
        self.runs.append(RunProperties(text, {}))
        self.runs.append(RunProperties(text2, {"superscript": "true"}))
        text = "[Zone:"
        self.runs.append(RunProperties(text, {}))
        self.runs.append(RunProperties(self.wind_design.zone, {}))
        text = "]"
        self.runs.append(RunProperties(text, {"end_of_line": "true"}))
        self.runs.append(RunProperties("", {"end_of_line": "true"}))
        self.wind_design.zone += 1
        pass
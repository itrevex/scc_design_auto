import sys
from docx.shared import Pt
from docx.enum.text import WD_BREAK
sys.path.append("./libs/")

from constants import Constants
from common import Common

class TableValue:
    def __init__(self, app_data, document, new_input_values):
        self.app_data = app_data
        self.document = document
        self.new_input_values = new_input_values
        self.template_table_values = app_data.getTemplateTableValues()
        self.calculateParameters()
        pass

    def getIdenfierParagraph(self, identifier_text):
        '''
        String identifier_text
        Find the paragraph that contains the idenfier text
        and return it
        '''
        for table in self.document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if identifier_text in paragraph.text:
                            return paragraph
        return None

    def updateTableValues(self):
        for key, value in self.template_table_values.items():
            #key descriptive key of what to change
            identifier_text = value[Constants.TEMPLATE_IDENTIFIER]
            paragraph = self.getIdenfierParagraph(identifier_text)

            if (paragraph != None):
                paragraph.text = ""
                value_parts = value[Constants.VALUE_PARTS]
                self.updateValueParts(paragraph, value_parts)

                Common.giveFeedBack(key)
    
    def updateValueParts(self, paragraph, parts):
        for part_name, part in parts.items():
            text = self.getInputText(part, part_name)
            TableValue.add_paragraph_run(paragraph, text, part)

    def getInputText(self, part, value):

        input_from = TableValue.getParameter(part, Constants.INPUT_FROM)

        if (input_from == Constants.INPUT_FROM_INPUT):
            return self.new_input_values[value]
        elif(input_from == Constants.INPUT_FROM_CALCULATION):
            return self.calculatedValue(value)

        return value

    def calculatedValue(self, value):

        if(value == Constants.WIND_SPEED_MS):
            return self.speed_text
        if (value == Constants.KZ_VALUE):
            return self.kz_text
        if (value == Constants.WIND_UNIT_LOAD):
            return self.wind_unit_load_text
        if (value == Constants.WIND_UNIT_LOAD_KN):
            return self.wind_unit_load_kn_text
        
        return ""

    def calcKzValue(self):
        height_above_ground = self.new_input_values[Constants.HEIGHT_ABOVE_GROUND]
        self.kz = Constants(self.app_data).kzValue(float(height_above_ground))
        self.kz_text = Constants.kzValueText(self.kz)

    def calcSpeedMs(self):
        #calcualted wind speed in m/s and return value
        #first get wind_speed value from input
        wind_speed = self.new_input_values[Constants.WIND_SPEED]
        self.speed_ms, self.speed_text = Constants.windSpeedMPerSecond(wind_speed)

    def calcWindUnitLoad(self):
        self.wind_unit_load = Constants.calcWindUnitLoad(self.speed_ms, self.kz)
        self.wind_unit_load_text = Constants.windUnitLoadText(self.wind_unit_load)

    def calcWindUnitLoadKn(self):
        self.wind_unit_load_kn =  self.wind_unit_load/1000.
        self.wind_unit_load_kn_text = Constants.textFourPlaces(self.wind_unit_load_kn)

    def calculateParameters(self):
        self.calcSpeedMs()
        self.calcKzValue()
        self.calcWindUnitLoad()
        self.calcWindUnitLoadKn()


    def getParameter(part, key):
        try:
            return part[key]
        except KeyError:
            return ""
        
    def add_paragraph_run(paragraph, text, part):
        
        run = paragraph.add_run(text)
        
        bold = TableValue.getParameter(part, Constants.BOLD)
        italic = TableValue.getParameter(part, Constants.ITALIC)
        underline = TableValue.getParameter(part, Constants.UNDERLINE)
        subscript = TableValue.getParameter(part, Constants.SUBSCRIPT)
        superscript = TableValue.getParameter(part, Constants.SUPERSCRIPT)
        end_of_line = TableValue.getParameter(part, Constants.END_OF_LINE)
        
        if (bold == Constants.TRUE):
            run.bold = True
        if (italic == Constants.TRUE):
            run.italic = True
        if (underline == Constants.TRUE):
            run.underline = True
        if (subscript == Constants.TRUE):
            run.font.subscript = True
        if (superscript == Constants.TRUE):
            run.font.superscript = True
        if (end_of_line == Constants.TRUE):
            run.add_break(WD_BREAK.LINE)
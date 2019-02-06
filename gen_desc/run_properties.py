from docx.enum.text import WD_BREAK
from libs.constants import Constants

class RunProperties:
    '''
    props = {
            "bold": "",
            "italic": "true",
            "underline": "",
            "subscript": "",
            "superscript": "",
            "end_of_line": ""
        }

    '''
    def __init__(self, text, props={}):

        self.text = str(text)
        self.bold = self.updateProp(props, Constants.BOLD)
        self.italic = self.updateProp(props, Constants.ITALIC)
        self.underline = self.updateProp(props, Constants.UNDERLINE)
        self.subscript = self.updateProp(props, Constants.SUBSCRIPT)
        self.superscript = self.updateProp(props, Constants.SUPERSCRIPT)
        self.end_of_line = self.updateProp(props, Constants.END_OF_LINE)

        pass
    
    def updateProp(self, props, key):
        try:
            return props[key] == Constants.TRUE
        except KeyError:
            return False

    def setText(self, text):
        self.text = str(text)

    def setBold(self, bold):
        self.bold = bold

    def setItalic(self, italic):
        self.italic = italic

    def setUnderline(self, underline):
        self.underline = underline

    def setSubscript(self, subscript):
        self.subscript = subscript

    def setSuperscript(self, superscript):
        self.superscript = superscript

    def setEndOfLine(self, end_of_line):
        self.end_of_line = end_of_line

    def applyRunProps(self, run):
        if (self.bold):
            run.bold = True
        if (self.italic):
            run.italic = True
        if (self.underline):
            run.underline = True
        if (self.subscript):
            run.font.subscript = True
        if (self.superscript):
            run.font.superscript = True
        if (self.end_of_line):
            run.add_break(WD_BREAK.LINE)
        return run;


    
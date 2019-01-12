import sys
from docx.shared import Pt

sys.path.append("./libs/")

from constants import Constants
from common import Common

class TableValue:
    def __init__(self, app_data, document, new_input_values):
        self.document = document
        self.new_input_values = new_input_values
        self.template_table_values = app_data.getTemplateDocumentValues()
        pass

    def trialMethod(self):
        for key, value in self.template_table_values:
            print(key)
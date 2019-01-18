from docx import Document
import json
import os
from collections import OrderedDict

class LoadData:
    '''
    class to load all data for program
    '''
    def __init__(self):
        ## Get directory for file path
        self.file_dir = os.path.dirname(__file__)
        self.head, self.tail = os.path.split(self.file_dir)
        if(self.tail != 'Gen-Desc.docx'): 
          self.file_dir = self.head
        pass

    def getFile(self, file_path):
        return os.path.join(self.file_dir, file_path)

    def getGenDescFile(self):
        return self.getFile("assests/Gen-Desc.docx")

    def getOutputFile(self):
        return self.getFile("generated/Gen-Desc.docx")
    
    def getTemplateDocumentValues(self):
        return json.load(open(self.getFile("assests/document_value_template.json"), encoding='utf8'), 
            object_pairs_hook=OrderedDict)

    def getTemplateTableValues(self):
        return json.load(open(self.getFile("assests/document_table_template.json"), encoding='utf8'), 
            object_pairs_hook=OrderedDict)
    
    def getInputValues(self):
        return json.load(open(self.getFile("assests/input_file.json"), encoding='utf8'), 
            object_pairs_hook=OrderedDict)

    def getDocxDocument(self):
        return Document(self.getFile("assests/Gen-Desc.docx"))

    def getTable27_3_1(self):
        return json.load(open(self.getFile("assests/asce/table_27_3_1.json"), encoding='utf8'), 
            object_pairs_hook=OrderedDict)

    def getWindDesignDefaults(self):
        return json.load(open(self.getFile("assests/wind_design_defaults.json"), encoding='utf8'), 
            object_pairs_hook=OrderedDict)

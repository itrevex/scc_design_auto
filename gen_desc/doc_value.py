import sys
from docx.shared import Pt

from libs.constants import Constants
from .common import Common

class DocValue:
    def __init__(self, app_data, document, new_input_values):
        self.document = document
        self.new_input_values = new_input_values
        self.template_doc_values = app_data.getTemplateDocumentValues()
        pass


    def getIdenfierParagraph(self, identifier_text):
        '''
        String identifier_text
        Find the paragraph that contains the idenfier text
        and return it
        '''
        for paragraph in self.document.paragraphs:
            if identifier_text in paragraph.text:
                return paragraph
        return None

    def getDocValueReplacementText(self, key):
        '''
        Get replacement value for key provided within the 
        input values provided by the user
        '''
        return self.new_input_values[key]

    def getNewParagraphText(self, paragraph, original_text, new_text):
        '''
        Replace original text with new text with the paragraph
        Change the paragh text the the changed value
        '''
        return paragraph.text.replace(original_text, new_text)

    def updateDocumentValues(self):
        
        for key, value in self.template_doc_values.items():
            self.updateDocValue(key, value)
            
    def updateDocValue(self, key, value):
        identifier_text = value[Constants.TEMPLATE_IDENTIFIER]
        replace_entire_paragraph = value[Constants.REPLACE_ENTIRE_PARAGRAPH]

        paragraph = self.getIdenfierParagraph(identifier_text)
        new_text = self.new_input_values[key]

        if (replace_entire_paragraph == Constants.TRUE):
            paragraph_text  = new_text
        else:
            paragraph_text  = paragraph.text.replace(identifier_text, new_text)

        paragraph.text = ""
        paragraph_text_run = paragraph.add_run(paragraph_text)
        paragraph_text_run.font.size = Pt(12)

        # self.giveFeedBack(key)
        Common.giveFeedBack(key)

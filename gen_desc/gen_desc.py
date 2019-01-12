from doc_value import DocValue

class GenDesc:
    def __init__(self, app_data):
        self.app_data = app_data
        self.document = self.app_data.getDocxDocument()
        self.new_input_values = self.app_data.getInputValues()

        pass


    def saveNewDocument(self):

        doc_value = DocValue(self.app_data, self.document, self.new_input_values)
        doc_value.updateDocumentValues()

        output_file = self.app_data.getOutputFile()
        self.document.save(output_file)

    def trialMethod(self):
        self.getDocValueReplacementText("project_name")

from doc_value import DocValue
from table_value import TableValue

class GenDesc:
    PROJECT_NAME = "project_name"
    def __init__(self, app_data):
        self.app_data = app_data
        self.document = self.app_data.getDocxDocument()
        self.new_input_values = self.app_data.getInputValues()
        self.project_name = self.new_input_values[GenDesc.PROJECT_NAME]
        pass


    def saveNewDocument(self, name =""):
        #update doc values, these are values not appearing within tables
        doc_value = DocValue(self.app_data, self.document, self.new_input_values)
        doc_value.updateDocumentValues()

        #update document values appearing within tables
        table_value = TableValue(self.app_data, self.document, self.new_input_values)
        table_value.updateTableValues()

        #save updated document in new output file
        print()
        output_file = self.app_data.getOutputFile(self.project_name)
        self.document.save(output_file)

    def trialMethod(self):
        table_value = TableValue(self.app_data, self.document, self.new_input_values)
        table_value.trials()
        pass

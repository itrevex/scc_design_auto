from .doc_value import DocValue
from .table_value import TableValue
from libs.constants import Constants

class GenDesc:
    PROJECT_NAME = "project_name"
    DESIGN_CODE = "design_code"
    ENCLOSURE_SPEC = "enclosure_specification"

    def __init__(self, app_data, wind_design):
        self.app_data = app_data
        self.new_input_values = self.app_data.getInputValues()
        self.design_code = self.new_input_values[GenDesc.DESIGN_CODE]
        self.enclosure = self.new_input_values[GenDesc.ENCLOSURE_SPEC]
        self.seismic_design = self.designSeismic()
        
        self.document = self.app_data.getDocxDocument(self.design_code, self.enclosure, 
            self.seismic_design)
        self.project_name = self.new_input_values[GenDesc.PROJECT_NAME]

        #update doc values, these are values not appearing within tables
        doc_value = DocValue(self.app_data, self.document, self.new_input_values)
        doc_value.updateDocumentValues()

        #update document values appearing within tables
        table_value = TableValue(self.app_data, self.document, wind_design)
        table_value.updateTableValues()

        pass

    def designSeismic(self):
        try:
            return self.new_input_values[Constants.SEISMIC] \
                [Constants.SEISMIC_DESIGN].lower() == "true"
        except KeyError:
            return False

    def saveNewDocument(self, name =""):
        
        #save updated document in new output file
        print()
        output_file = self.app_data.getOutputFile(self.project_name)
        self.document.save(output_file)

    def trialMethod(self):
        table_value = TableValue(self.app_data, self.document, self.new_input_values)
        table_value.trials()
        pass

from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from docx.shared import Pt

from gen_desc.gen_desc import GenDesc
from libs.load_data import LoadData
from libs.messages import Messages
from windmap.windmap import Windmap
from windmap.plot_loads import PlotLoads
from form_grs.form_grs import FormGrs
from dxf.read.dxf_input import DxfInput

app_data = LoadData()

if __name__ == "__main__":
    gen_desc = GenDesc(app_data)
    
    #write gen_desc document
#!    gen_desc.saveNewDocument()
    
    #draw windmap jpg
    Windmap(gen_desc.wind_design).plotWindMap(app_data)

    #write windmap txts into file
#!    PlotLoads(gen_desc.wind_design).plotLoads(app_data)

    #write form grs file
#!    form_grs = FormGrs(app_data, gen_desc)

    #get geom dxf file
    dxf_input = DxfInput(app_data)
    
    #print prompt message
    Messages.continuePrompt("Press any key to continue . . .")
    
    pass




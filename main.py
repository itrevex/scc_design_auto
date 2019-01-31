from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_BREAK
from docx.shared import Pt

from gen_desc.gen_desc import GenDesc
from libs.load_data import LoadData

app_data = LoadData()

if __name__ == "__main__":
    gen_desc = GenDesc(app_data)
    # gen_desc.saveNewDocument()
    gen_desc.trialMethod()
    pass




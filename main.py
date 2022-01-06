import os
import io


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from PyPDF2 import PdfFileWriter, PdfFileReader


import utils
import functions
from parameters import *

'''
[X] Read Template
[X] Read Input Json
[X] Read Input Csv
[X] Process Csv
[X] Process Json
[X] Merge Template + Input
[X] Save Report
[X] How to change Font Size
[X] How to change Font Style
[X] How to change Font Color

Extras:

[ ] Func to make human Readable 
'''


path_output = 'output'
filename_output = 'report.pdf'
path_template = 'templates'
filename_template = 'clear_template.pdf'
value = "Valor Teste"

path_input_json = 'input'
filename_input_json = 'value_01'


list_infos_json = functions.read_input_json(path=path_input_json, filename=filename_input_json)
# list_infos_csv = functions.read_input_csv(path=path_input_json, filename=filename_input_json)
# list_infos_xlsx = functions.read_input_excel(path=path_input_json, filename=filename_input_json)

output = PdfFileWriter()
for dict_infos in list_infos_json:
    
    dict_template_mail = functions.process_dict_template(dict_json_input=dict_infos)

    output = functions.generate_direct_mail(path_template=path_template, filename_template=filename_template, dict_values=dict_template_mail, path_input_json=path_input_json, filename_input_json=filename_input_json, output=output)
    
functions.save_fill_template(path=path_output, filename=filename_output, output=output)









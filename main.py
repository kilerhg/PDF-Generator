import os
import io


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from PyPDF2 import PdfFileWriter, PdfFileReader


import utils
import functions

'''
[ ] Read Template
[ ] Read Input Json
[ ] Read Input Csv
[ ] Process Csv
[ ] Process Json
[ ] Merge Template + Input
[ ] Save Report
'''


MIN_X = 20
MIN_Y = 10

MAX_X = 530
MAX_Y = 820

def read_input_json():
    pass


def read_input_csv():
    pass


def save_input_in_ram(list_values : list):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    # "Hello world"
    for item in list_values:
        can.drawString(int(item['CORD_X']), int(item['CORD_Y']), item['VALUE'])
    # for cord_x in range(20, 530, 55):
    #     for cord_y in range(10, 820, 20):
    #         can.drawString(cord_x, cord_y, f'[{str(cord_x).zfill(3)}X{str(cord_y).zfill(3)}]')
    # can.save()
    packet.seek(0)
    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    return new_pdf


def read_template(path : str, filename : str):
    # read your existing PDF
    # input/basic_pdf_01.pdf
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    existing_pdf = PdfFileReader(open(full_path, "rb"))
    page = existing_pdf.getPage(0)
    return page


def merge_pdfs(page, new_pdf):
    output = PdfFileWriter()
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return output


def save_fill_template(path : str, filename : str, output):
    # finally, write "output" to a real file
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    outputStream = open(full_path, "wb")
    output.write(outputStream)
    outputStream.close()


def generate_direct_mail(path_output, filename_output, path_template, filename_template, list_values):
    new_pdf = save_input_in_ram(list_values=list_values)
    page = read_template(path=utils.process_str_to_lower(path_template), filename=utils.process_str_to_lower(filename_template))
    output = merge_pdfs(page=page, new_pdf=new_pdf)
    save_fill_template(path=path_output, filename=filename_output, output=output)


# input/basic_pdf_01.pdf
# output/report.pdf
path_output = 'output'
filename_output = 'report.pdf'
path_template = 'input'
filename_template = 'basic_pdf_01.pdf'
value = "Valor Teste"


list_values_input = [
    {
    'CORD_X':'100',
    'CORD_Y':'100',
    'VALUE':'100x100',
    },
    {
    'CORD_X':'200',
    'CORD_Y':'200',
    'VALUE':'200x200',
    },
    {
    'CORD_X':'300',
    'CORD_Y':'300',
    'VALUE':'300x300',
    },
    {
    'CORD_X':'400',
    'CORD_Y':'400',
    'VALUE':'400x400',
    },
    {
    'CORD_X':'500',
    'CORD_Y':'500',
    'VALUE':'500x500',
    },
    {
    'CORD_X':'550',
    'CORD_Y':'550',
    'VALUE':'550x550',
    },
    {
    'CORD_X':'530',
    'CORD_Y':'820',
    'VALUE':'530x820',
    },
    {
    'CORD_X':MIN_X,
    'CORD_Y':MIN_Y,
    'VALUE':'20x10',
    }
                    ]

generate_direct_mail(path_output=path_output, filename_output=filename_output, path_template=path_template, filename_template=filename_template, list_values=list_values_input)











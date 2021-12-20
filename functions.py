import os
import io
import logging
import json
from datetime import datetime


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, LETTER, landscape
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfbase.pdfmetrics import getAscent, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pandas import read_csv, read_excel

import utils
import parameters

MIN_X = 0
MIN_Y = 0

MAX_X = 600
MAX_Y = 870

NUMBER_MONTH_TO_NAME_MONTH = {
    '01':'Janeiro',
    '02':'Fevereiro',
    '03':'Março',
    '04':'Abril',
    '05':'Maio',
    '06':'Junho',
    '07':'Julho',
    '08':'Agosto',
    '09':'Setembro',
    '10':'Outubro',
    '11':'Novembro',
    '12':'Dezembro',
}


def process_dict_template(dict_json_input, dict_template = parameters.dict_template_mail):
    dict_template['FIELD_1']['VALUE'] = process_name_city_actual_date(dict_json_input['FIELD_1'])
    dict_template['FIELD_2']['VALUE'] = dict_json_input['FIELD_2']
    dict_template['FIELD_3']['VALUE'] = dict_json_input['FIELD_3']
    dict_template['FIELD_4']['VALUE'] = dict_json_input['FIELD_4']
    return dict_template


def process_name_city_actual_date(name_city : str):
    from datetime import datetime
    today = datetime.today()
    value = f'{str(name_city).strip().title()}, {str(today.day).zfill(2)} De {NUMBER_MONTH_TO_NAME_MONTH[str(today.month).zfill(2)]} De {str(today.year).zfill(4)}'
    return value


def read_input_json(path : str, filename : str):
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    with open(full_path + '.json', 'r', encoding='utf-8') as file:
        try:
            dict_infos = json.load(file)
        except:
            dict_infos = None
            logging.warning('Json Invalido')
    return dict_infos


def read_input_csv(path : str, filename : str):
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    df_input = read_csv(full_path + '.csv', header=0, delimiter=";", encoding=parameters.ENCODING_ISO_8859_1,low_memory=False, dtype=str)
    records_input = df_input.to_dict("records")
    return records_input


def read_input_excel(path : str, filename : str):
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    df_input = read_excel(full_path + '.xlsx', "input", dtype=str)
    records_input = df_input.to_dict("records")
    return records_input

def save_input_in_ram(dict_values : dict):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=landscape(LETTER))

    pdfmetrics.registerFont(TTFont('Trebuchet MS', 'trebuc.ttf'))


    for item in dict_values.values():
        if 'STYLE' == '1':
            can.setFillColorRGB(r=0, g=0, b=0)
            can.setFont(psfontname='Trebuchet MS', size=16) 
        elif 'STYLE' == '2':
            can.setFillColorRGB(r=0, g=0, b=0)
            can.setFont(psfontname='Trebuchet MS', size=10) 
        
        can.drawString(float(item['CORD_X']), float(item['CORD_Y']), item['VALUE'])
    # for cord_x in range(MIN_X + 20, MAX_X - 20, 30):
    #     for cord_y in range(MIN_Y + 20, MAX_Y - 20, 10):
    #         can.drawString(cord_x, cord_y, f'[{str(cord_x).zfill(3)}X{str(cord_y).zfill(3)}]')
    
    can.save()
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


def merge_pdfs(page, new_pdf, output):
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    return output


def save_fill_template(path : str, filename : str, output):
    # finally, write "output" to a real file
    full_path = str(os.path.join(utils.process_str_to_lower(path), utils.process_str_to_lower(filename)).strip())
    outputStream = open(full_path, "wb")
    output.write(outputStream)
    outputStream.close()


def generate_direct_mail(path_template, filename_template, dict_values, path_input_json, filename_input_json, output):
    new_pdf = save_input_in_ram(dict_values=dict_values)
    page = read_template(path=utils.process_str_to_lower(path_template), filename=utils.process_str_to_lower(filename_template))
    output = merge_pdfs(page=page, new_pdf=new_pdf, output=output)
    # save_fill_template(path=path_output, filename=filename_output, output=output)
    return output
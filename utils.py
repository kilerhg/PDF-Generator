from datetime import datetime

def process_str_to_lower(value):
    value = str(value).strip().lower()
    return value

def receive_text_break_by_max_length(text, length):
    list_sentences = []

def convert_date_from_str(value):
    value = str(value).strip()[:10]
    if value != '' and value != '-':
        if value.count('-') > 0:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        elif value.count('/') > 0:
            value = datetime.strptime(value, "%d/%m/%Y").date()
    else:
        value = ''
    return value

def process_date_latin_america(value_date : datetime.date):
    value = f'{str(value_date.day).zfill(2)}/{str(value_date.month).zfill(2)}/{str(value_date.year).zfill(4)}'
    return value

def process_date(value : str):
    value_date = convert_date_from_str(value = value)
    clear_str_date = process_date_latin_america(value_date = value_date)
    return clear_str_date
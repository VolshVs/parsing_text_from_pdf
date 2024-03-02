import os

import re
from pathlib import Path

import fitz

from data_handling.processing_5_2 import get_info_5_2
from data_handling.processing_5_3 import get_info_5_3


def get_big_data():
    """Функция считывает заданный PDF файл и убирает из всего текста
    символ новой строки."""
    script_dir = Path(__file__).parents[0]
    file_path = 'raw_files/SAE J1939-71.pdf'
    doc = fitz.open(os.path.join(script_dir, file_path))
    text = ''
    for page in doc:
        text += page.get_text(sort=True)
    all_text = re.sub("\n", '', text)
    return clear_pages(all_text)


def clear_pages(dirty_text):
    """Функция удаляет из всего текста повторяющиеся
    неиспользуемые выражения."""
    pattern_page = r"(Page\s\d*\sof\s442)"
    dell_pages = re.sub(
        pattern_page,
        '',
        dirty_text
    )
    pattern_db_report = r"(J1939\s.71\sDatabase\sReport)"
    dell_db_report = re.sub(
        pattern_db_report,
        '',
        dell_pages
    )
    pattern_date = r"(April\s15.\s2001)"
    dell_date = re.sub(
        pattern_date,
        '',
        dell_db_report
    )
    pattern_pgn_sup_info = r"(PGN\sSupporting\sInformation:)"
    dell_pgn_sup_info = re.sub(
        pattern_pgn_sup_info,
        '',
        dell_date
    )
    pattern_pgn_param_gr_name = r"(PGN\sParameter\sGroup\sName\sand\sAcronym\sDoc\.\sand\sParagraph)"
    dell_pgn_param_gr_name = re.sub(
        pattern_pgn_param_gr_name,
        '',
        dell_pgn_sup_info
    )
    pattern_ret_config_rc = r"(Retarder\sConfiguration\s-\sRC)"
    dell_ret_config_rc = re.sub(
        pattern_ret_config_rc,
        '',
        dell_pgn_param_gr_name
    )
    pattern_operational = r'(Operational\sRange:\ssame\sas\sslot\srange)'
    dell_operational = re.sub(
        pattern_operational,
        '',
        dell_ret_config_rc
    )
    pattern_spn_sup = r"(SPN\sSupporting\sInformation:)"
    dell_spn_sup = re.sub(
        pattern_spn_sup,
        '',
        dell_operational
    )
    pattern_ref = r"(Reference:)"
    dell_ref = re.sub(
        pattern_ref,
        '',
        dell_spn_sup
    )
    result = dell_ref
    return get_info_5_2(result), get_info_5_3(result)

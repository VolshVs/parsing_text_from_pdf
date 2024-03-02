import re

from models.tables_entry import table_entry_5_3, table_entry_5_3_params


def get_info_5_3(cleared_text):
    """Функция принимает текст и разбивает его на группы разделов 5.3."""
    global_list = []
    pattern = r'(-71{1}\s[5][.][3][.].{3})'
    pattern_5_2 = r'(-71{1}\s[5][.][2][.][7][.][???])'
    pattern_5_3 = r'(-71{1}\s[5][.][3][.]001)'
    raw_text = (cleared_text + ' ')[:-1]
    span_one_step_5_3 = list(re.search(
        pattern_5_2,
        raw_text
    ).span())[0]
    raw_text = raw_text[span_one_step_5_3:]
    span_two_step_5_3 = list(re.search(
        pattern_5_3,
        raw_text
    ).span())[0]
    group_two_step_5_3 = re.search(
        pattern_5_3,
        raw_text
    ).group()
    group_sec_5_3 = (group_two_step_5_3 + ' ')[:-1]
    text_corrected_sec_5_3 = raw_text[span_two_step_5_3:]
    while group_sec_5_3 in text_corrected_sec_5_3:
        group_list = []
        text_corrected_sec_5_3 = text_corrected_sec_5_3[1:]
        if re.search(pattern, text_corrected_sec_5_3) is None:
            continue
        span_next = ((list(re.search(
            pattern,
            text_corrected_sec_5_3
        ).span())[0]) - 1)
        text_small = text_corrected_sec_5_3[:span_next]
        group_list.append(text_small[:10])
        group_list.append(text_small)
        text_corrected_sec_5_3 = text_corrected_sec_5_3[span_next + 1:]
        group_sec_5_3 = (re.search(
            pattern,
            text_corrected_sec_5_3
        ).group() + ' ')[:-1]
        global_list.append(group_list)
    return get_correct_info_5_3(global_list)


def get_correct_info_5_3(g_list):
    """Функция перерабатывает поступивший список с группами разделов 5.3.
    в список словарей с получившимися параметрами."""
    global_list_info = []
    pk = 0
    for one_list in g_list:
        small_dict = dict()
        pk += 1
        small_dict['id'] = pk
        small_dict['section_number_5_3'] = one_list[0][3:]
        pattern_length = r'(Data Length: )'
        span_length = list(re.search(
            pattern_length,
            one_list[1]
        ).span())[0]
        split_text = one_list[1][span_length:].split(' ')
        small_dict['data_length'] = split_text[2]
        pattern_pgn_id = r'(Group  )(\d*) (\( [A-W\d]{1,4}?\ \))'
        text_with_pgn_id = " ".join(split_text[20:])
        if re.search(pattern_pgn_id, text_with_pgn_id) is None:
            continue
        span_pgn_id = list(re.search(
            pattern_pgn_id,
            text_with_pgn_id
        ).span())[0]
        split_text = text_with_pgn_id[span_pgn_id:].split(' ')
        small_dict['pgn'] = split_text[2]
        small_dict['id_CAN_identifier'] = split_text[4]
        text_next = " ".join(split_text[22:])
        params_list = get_params_for_5_3(text_next)
        small_dict['params_list'] = params_list
        global_list_info.append(small_dict)
    return (table_entry_5_3(global_list_info),
            table_entry_5_3_params(global_list_info))


def get_params_for_5_3(text):
    """Функция получает на вход список текстов,
    перерабатывая получает из них данные,
    возвращает полученные данные в словарях обратно."""
    pattern1_approved = r'\d{1,2}.\d{1,2}.\d{4}'
    pattern2_paragraph = r'( -71) (\d\.\d\.\d\..{1,3})'
    pattern6_length = r'(\d [b]\w{3,5})'
    params_list = []
    id_params = 0
    text = re.split(pattern1_approved, text, maxsplit=0, flags=0)
    for element in text:
        params_dict = dict()
        if len(element) < 10:
            continue
        paragraph = re.findall(
            pattern2_paragraph,
            element
        )
        if re.search(pattern2_paragraph, element) is None:
            continue
        element = element[:list(re.search(
            pattern2_paragraph,
            element
        ).span())[0]]
        element = element.split(" ")
        id_params += 1
        spn = element[-1]
        element = element[:-1]
        element = " ".join(element)
        length = re.findall(
            pattern6_length,
            element
        )
        if len(length) == 0:
            length = element
            parameter_name = ''
            params_dict['id'] = id_params
            params_dict['paragraph'] = paragraph[0][1].replace(' ', '')
            params_dict['spn'] = spn
            params_dict['length'] = length[0]
            params_dict['parameter_name'] = parameter_name
            params_list.append(params_dict)
            break
        element = re.split(pattern6_length, element)
        parameter_name = element[-1]
        params_dict['id'] = id_params
        params_dict['paragraph'] = paragraph[0][1].replace(' ', '')
        params_dict['spn'] = spn
        params_dict['length'] = length[0]
        params_dict['parameter_name'] = parameter_name[1:]
        params_list.append(params_dict)
    return params_list

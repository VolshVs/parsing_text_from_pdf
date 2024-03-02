import re

from models.tables_entry import table_entry_5_2


def get_info_5_2(cleared_text):
    """Функция принимает текст и разбивает его на группы параграфов 5.2."""
    global_list = []
    pattern = r'(-71{1}\s[5][.][2][.]\w*[.]*\d*\S{3})'
    raw_text = (cleared_text + ' ')[:-1]
    span_first_sec_5_2 = list(re.search(pattern, raw_text).span())[0]
    group_first_sec_5_2 = re.search(pattern, raw_text).group()
    group_sec_5_2 = (group_first_sec_5_2 + ' ')[:-1]
    text_corrected_sec_5_2 = raw_text[span_first_sec_5_2:]
    while group_sec_5_2 in text_corrected_sec_5_2:
        group_list = []
        text_corrected_sec_5_2 = text_corrected_sec_5_2[1:]
        if len(text_corrected_sec_5_2) > 100:
            span_next = ((list(re.search(
                pattern,
                text_corrected_sec_5_2
            ).span())[0]) - 1)
            text_small = text_corrected_sec_5_2[:span_next]
            group_list.append(text_small[:12])
            group_list.append(text_small)
            text_corrected_sec_5_2 = text_corrected_sec_5_2[span_next + 1:]
            group_sec_5_2 = (re.search(
                pattern,
                text_corrected_sec_5_2
            ).group() + ' ')[:-1]
        global_list.append(group_list)
    return get_correct_info_5_2(global_list)


def get_correct_info_5_2(g_list):
    """Функция перерабатывает поступивший список с группами параграфов 5.2.
    в список словарей с получившимися параметрами."""
    global_list_info = []
    pk = 0
    for one_list in g_list:
        small_dict = dict()
        if len(one_list) > 0:
            small_dict['paragraph_number'] = one_list[0][3:]
        pattern = r'(\d{2}\s\d.\d*.\d*.{4}\s\d*/\d*/\d*)'
        if len(one_list) > 0 and re.search(pattern, one_list[1]) is None:
            pattern_scaling = r'(Slot Scaling: .*)( , )'
            if re.search(pattern_scaling, one_list[1]) is not None:
                span_text_no_scaling = re.search(
                    pattern_scaling,
                    one_list[1]
                ).span()[0]
            text_no_scaling = one_list[1][:span_text_no_scaling]
            pk += 1
            one_string = text_no_scaling[12:].split(' ')
            new_one_list = []
            for word in one_string:
                if len(word) > 0:
                    new_one_list.append(word)
            new_list_upper = []
            count_2 = 0
            for word_upper in new_one_list[:12]:
                if word_upper in new_list_upper:
                    continue
                else:
                    new_list_upper.append(word_upper)
                if word_upper[0].islower():
                    count_2 += 1
                if count_2 == 2:
                    break
            if len(new_list_upper) > 7:
                for word_lower in new_list_upper:
                    if word_lower[0].islower():
                        new_list_upper = new_list_upper[:-1]
            small_dict['paragraph_title'] = " ".join(new_list_upper[:-1])
            slot_scaling, slot_range, spn, pgn = get_slots_spn_for_5_2(
                one_list[1]
            )
            small_dict['slot_scaling'] = slot_scaling
            small_dict['slot_range'] = slot_range
            small_dict['spn'] = spn
            small_dict['pgn'] = pgn.replace(' ', '')
            small_dict['pk'] = pk
        global_list_info.append(small_dict)
        if len(small_dict) == 1:
            small_dict.clear()
    complete_clean_list = list(filter(None, global_list_info))[:-1]
    return table_entry_5_2(complete_clean_list)


def get_slots_spn_for_5_2(text):
    """Функция получает на вход список текстов,
    перерабатывая получает из них данные,
    возвращает полученные данные обратно."""
    text = text[12:]
    pattern_scaling = r'(Slot Scaling: .*)( ,)'
    pattern_range = r'Slot Range: .{30}.{20}'
    pattern_spn = r'(SPN: \d*)'
    pattern_pgn = r'( \d{3,5} ){1}'
    slot_scaling = ''
    if len(re.findall(pattern_scaling, text)) > 0:
        slot_scaling = re.findall(pattern_scaling, text)[0][0]
    if len(slot_scaling) > 50:
        slot_scaling = slot_scaling[:30]
    text_range = re.findall(pattern_range, text)
    correct_pattern_range_1 = r'(.*)(   SPN Type:){1}'
    correct_pattern_range_2 = r'(.*)(Operational Range:){1}'
    slot_range = text_range
    if len(text_range) > 0:
        if len(re.findall(correct_pattern_range_1, slot_range[0])) > 0:
            slot_range = re.findall(correct_pattern_range_1, slot_range[0])
        elif len(re.findall(correct_pattern_range_2, slot_range[0])) > 0:
            slot_range = re.findall(correct_pattern_range_2, slot_range[0])
        else:
            pass
        slot_range = slot_range[0][0]
    spn = ''
    if len(re.findall(pattern_spn, text)) > 0:
        spn = re.findall(pattern_spn, text)[0]
    pgn = ''
    if len(re.findall(pattern_pgn, text)) > 0:
        span_pgn = re.search(pattern_spn, text).span()[1]
        pgn_2 = re.findall(pattern_pgn, text[span_pgn:])
        pgn = ",".join(pgn_2[:1])
    return slot_scaling[14:], slot_range[12:], spn[5:], pgn

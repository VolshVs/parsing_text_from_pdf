from sqlalchemy.orm import sessionmaker

from models.models import Section53, Section53Params, Section52
from system import connecting


def get_info(user_input):
    """Функция получает запрос от пользователя и выводит
    информацию из базы данных"""
    engine = connecting()
    Session = sessionmaker(bind=engine)
    dbsession = Session()
    session_body = dbsession.query(
        Section53.section_number_5_3,
        Section53.data_length,
        Section53.id_CAN_identifier,
        Section53Params.parameter_name,
        Section53Params.paragraph,
        Section53Params.length,
        Section53Params.spn
    ).select_from(
        Section53
    ).join(
        Section53Params,
        Section53.id == Section53Params.id_section_5_3
    )
    if len(str(user_input)) < 3:
        return print("Запрос некорректен.")
    try:
        if user_input[0].isdigit() and user_input[2] == "3":
            result_1 = session_body.filter(
                Section53.section_number_5_3 == user_input
            ).all()
        elif user_input[0].isdigit() and user_input[2] == "2":
            result_1 = session_body.filter(
                Section53Params.paragraph == user_input
            ).all()
        else:
            result_1 = session_body.filter(
                Section53Params.parameter_name == user_input
            ).all()
        session_body_2 = dbsession.query(
            Section52.paragraph_number_5_2,
            Section52.paragraph_title,
            Section52.scaling,
            Section52.range,
            Section52.spn,
            Section52.pgn
        ).select_from(
            Section52
        )
        result_2 = session_body_2.filter(
            Section52.paragraph_number_5_2 == result_1[0][4]
        ).all()
        num = 62
        num_1 = num
        num_2 = num
        if len(result_1[0][3]) < 3 and not None:
            num_1 = 3
            num_2 = len(result_2[0][1]) + 1
    except IndexError:
        return print('Ошибка ввода.')
    print('\n')
    try:
        for (number, d_length, id_can, param_name,
             paragraph, length, spn) in result_1:
            print(f"Найден раздел: {number: <8} | "
                  f"Data length: {d_length: <8} | "
                  f"ID: {id_can: <4} | "
                  f"Parameter name: {param_name: <{num_1}} | "
                  f"Параграф: {paragraph: <8} | "
                  f"Length: {length: <7} | "
                  f"SPN: {spn: <5}")
        print('\n')
        for p_number, p_title, scaling, range_, spn, pgn in result_2:
            print(f"Информация по параграфу: {p_number: <8} | "
                  f"Parameter name: {p_title: <{num_2}} | "
                  f"Scaling: {scaling: <17} | "
                  f"Range: {range_: <23} | "
                  f"SPN: {spn: <5} | "
                  f"PGN: {pgn: <7}")
        print("\n* В случае отсутствия информации в каком-то "
              "параметре необходимо обратиться к первичному документу.")
    except UnboundLocalError:
        return print('Ошибка ввода.')
    dbsession.commit()
    dbsession.close()

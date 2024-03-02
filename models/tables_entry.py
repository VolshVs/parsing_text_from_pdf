from sqlalchemy.orm import sessionmaker

from models.models import (Section52, create_tables,
                           Section53, Section53Params)
from system import connecting


def table_entry_5_2(data_list):
    """Функция получает список словарей и загружает данные в базу данных"""
    engine = connecting()
    create_tables(engine)
    for one_dict in data_list:
        model = Section52(
            id=one_dict['pk'],
            paragraph_number_5_2=one_dict['paragraph_number'],
            paragraph_title=one_dict['paragraph_title'],
            scaling=one_dict['slot_scaling'],
            range=one_dict['slot_range'],
            spn=one_dict['spn'],
            pgn=one_dict['pgn']
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(model)
        session.commit()
    session.close()


def table_entry_5_3(data_list):
    """Функция получает список словарей и загружает данные в базу данных"""
    engine = connecting()
    for one_dict in data_list:
        model = Section53(
            id=one_dict['id'],
            section_number_5_3=one_dict['section_number_5_3'],
            data_length=one_dict['data_length'],
            pgn=one_dict['pgn'],
            id_CAN_identifier=one_dict['id_CAN_identifier']
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(model)
        session.commit()
    session.close()


def table_entry_5_3_params(data_list):
    """Функция получает список словарей и загружает данные в базу данных"""
    engine = connecting()
    id_params = 0
    for one_dict in data_list:
        list_params = one_dict['params_list']
        for params in list_params:
            id_params += 1
            model = Section53Params(
                id=id_params,
                length=str(params['length']),
                parameter_name=params['parameter_name'],
                spn=params['spn'],
                paragraph=params['paragraph'],
                id_section_5_3=one_dict['id']
            )
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(model)
            session.commit()
    session.close()

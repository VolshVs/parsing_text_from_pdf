import sqlalchemy as sq

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Section52(Base):
    """Класс создает модель таблицы в базе  данных"""
    __tablename__ = "section_5_2"

    id = sq.Column(sq.Integer, primary_key=True)
    paragraph_number_5_2 = sq.Column(sq.String(length=12), nullable=False)
    paragraph_title = sq.Column(sq.String(length=300), nullable=False)
    scaling = sq.Column(sq.String(length=30), nullable=False)
    range = sq.Column(sq.String(length=50), nullable=False)
    spn = sq.Column(sq.String(length=20), nullable=False)
    pgn = sq.Column(sq.String(length=20), nullable=False)

    def __str__(self):
        return f'{self.__tablename__}'


class Section53(Base):
    """Класс создает модель таблицы в базе  данных"""
    __tablename__ = "section_5_3"

    id = sq.Column(sq.Integer, primary_key=True)
    section_number_5_3 = sq.Column(sq.String(length=12), nullable=False)
    data_length = sq.Column(sq.String(length=30), nullable=False)
    pgn = sq.Column(sq.String(length=20), nullable=False)
    id_CAN_identifier = sq.Column(sq.String(length=20),
                                  nullable=False)

    def __str__(self):
        return f'{self.__tablename__}'


class Section53Params(Base):
    """Класс создает модель таблицы в базе  данных"""
    __tablename__ = "5_3_params"

    id = sq.Column(sq.Integer, primary_key=True)
    length = sq.Column(sq.String(length=30), nullable=False)
    parameter_name = sq.Column(sq.String(length=300), nullable=False)
    spn = sq.Column(sq.String(length=20), nullable=False)
    paragraph = sq.Column(sq.String(length=20), nullable=False)
    id_section_5_3 = sq.Column(sq.Integer, sq.ForeignKey("section_5_3.id"),
                               nullable=False)

    section_5_3 = relationship(Section53, backref="5_3_params")

    def __str__(self):
        return f'{self.__tablename__}'


def create_tables(engine):
    """Функция очищает и заново создает таблицы в базе данных."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Options(SqlAlchemyBase):
    __tablename__ = 'options'

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    text = sqlalchemy.Column(sqlalchemy.String)
    work_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'))

    # orm-отношения
    question = orm.relationship('Questions')
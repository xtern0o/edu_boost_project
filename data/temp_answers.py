import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class TempAnswers(SqlAlchemyBase):
    __tablename__ = "temp_answers"

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    temp_answer = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'))

    temp_question = orm.relationship('Questions')
    temp_user = orm.relationship('Users')
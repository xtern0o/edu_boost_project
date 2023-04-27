import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Questions(SqlAlchemyBase):
    __tablename__ = "questions"

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    work_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("works.id"))
    header = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    answer_type = sqlalchemy.Column(sqlalchemy.String)
    correct_answer = sqlalchemy.Column(sqlalchemy.String)
    points = sqlalchemy.Column(sqlalchemy.Integer)

    # orm-отношения
    work = orm.relationship("Works")
    options = orm.relationship('Options', back_populates='question')
    temp_answer = orm.relationship('TempAnswers', back_populates='temp_question')

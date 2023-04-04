import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Questions(SqlAlchemyBase):
    __tablename__ = "questions"

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    work_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("works.id"))
    text = sqlalchemy.Column(sqlalchemy.String)
    answer_type = sqlalchemy.Column(sqlalchemy.String)
    input_form = sqlalchemy.Column(sqlalchemy.String)
    correct_answer = sqlalchemy.Column(sqlalchemy.String)

    # orm-отношения
    work = orm.relationship("Works")

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class SolvedWorks(SqlAlchemyBase):
    __tablename__ = "solved_works"

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    work_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("works.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    # orm-отношения
    solved_work = orm.relationship("Works")
    solved_user = orm.relationship("Users")
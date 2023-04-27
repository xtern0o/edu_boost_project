import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class WorksInProcess(SqlAlchemyBase):
    __tablename__ = 'works_in_process'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    work_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("works.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    # orm-отношения
    process_work = orm.relationship("Works")
    process_user = orm.relationship("Users")
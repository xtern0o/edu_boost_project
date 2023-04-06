import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Groups(SqlAlchemyBase):
    __tablename__ = 'groups'

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    # orm-отношения
    students = orm.relationship('Users', secondary='users_to_groups', backref='students')
    message = orm.relationship('Messages', back_populates='group')
    teacher = orm.relationship('Users')
    works = orm.relationship("Works", secondary="works_to_groups", backref='works')

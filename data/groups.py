import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Groups(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'groups'

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    code = sqlalchemy.Column(sqlalchemy.String, unique=True)

    # orm-отношения
    students = orm.relationship('Users', secondary='users_to_groups', backref='students')
    message = orm.relationship('Messages', back_populates='group')
    teacher = orm.relationship('Users')
    works = orm.relationship("Works", secondary="works_to_groups", backref='works')
    invites_students = orm.relationship('Groups', secondary='users_to_invites_to_groups', backref='users_invites')

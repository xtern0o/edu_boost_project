import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Messages(SqlAlchemyBase):
    __tablename__ = 'messages'

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # orm-отношения
    group = orm.relationship('Groups')
    sender = orm.relationship('Users')
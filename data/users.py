import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


# Вспомогательная таблица для связи many-to-many таблицы users и groups
users_to_groups_table = sqlalchemy.Table(
    'users_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('group', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')),
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
)


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    # Поля таблица
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    first_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    second_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    profile_photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # orm-отношения
    groups = orm.relationship('Groups', secondary='users_to_groups', backref='users')
    admin = orm.relationship('Groups', back_populates='teacher')
    sender = orm.relationship('Messages', back_populates='sender')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
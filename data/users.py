import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


# Вспомогательная таблица для связи many-to-many таблицы users и groups
users_to_groups_table = sqlalchemy.Table(
    'users_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('group', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')),
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
)


users_to_invites_to_groups_table = sqlalchemy.Table(
    'users_to_invites_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('group', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id'))

)


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    # Поля таблица
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    password = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    remember = sqlalchemy.Column(sqlalchemy.Boolean)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    second_name = sqlalchemy.Column(sqlalchemy.String)
    profile_photo = sqlalchemy.Column(sqlalchemy.BLOB, default=None)
    user_type = sqlalchemy.Column(sqlalchemy.String, default="student")
    apikey = sqlalchemy.Column(sqlalchemy.String)

    # orm-отношения
    groups = orm.relationship('Groups', secondary='users_to_groups', backref='groups')
    admin = orm.relationship('Groups', back_populates='teacher')
    sender = orm.relationship('Messages', back_populates='sender')
    creator = orm.relationship('Works', back_populates='creator')
    solved_works = orm.relationship('SolvedWorks', back_populates='solved_user')
    process_works = orm.relationship('WorksInProcess', back_populates='process_user')
    invites_group = orm.relationship('Groups', secondary='users_to_invites_to_groups', backref='invites')
    temp_answers = orm.relationship('TempAnswers', back_populates='temp_user')

    # функции
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_apikey(self, apikey):
        self.apikey = generate_password_hash(apikey)

    def check_apikey(self, apikey):
        return check_password_hash(self.apikey, apikey)
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


# Вспомогательная таблица для связи many-to-many таблицы works и groups
works_to_groups_table = sqlalchemy.Table(
    'works_to_groups',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('group', sqlalchemy.Integer, sqlalchemy.ForeignKey('groups.id')),
    sqlalchemy.Column('work', sqlalchemy.Integer, sqlalchemy.ForeignKey('works.id'))
)


class Works(SqlAlchemyBase):
    __tablename__ = 'works'

    # Поля таблицы
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=True)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    # orm-отношения
    groups = orm.relationship('Groups', secondary='works_to_groups', backref="in_groups")
    creator = orm.relationship('Users')
    questions = orm.relationship("Questions", back_populates="work")
    solved = orm.relationship('SolvedWorks', back_populates="solved_work")
    process = orm.relationship('WorksInProcess', back_populates='process_work')

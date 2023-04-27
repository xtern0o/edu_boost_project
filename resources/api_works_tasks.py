from flask_restful import reqparse, abort, Api, Resource

from data import db_session

from data.works import Works
from data.users import Users
from data.questions import Questions
from data.groups import Groups


def abort_if_work_not_found(work_id):
    db_sess = db_session.create_session()
    if not db_sess.query(Works).get(work_id):
        abort(404, message=f"work with id={work_id} not found")


def abort_of_group_not_found(group_id):
    db_sess = db_session.create_session()
    if not db_sess.query(Groups).get(group_id):
        abort(404, message=f"group with id={group_id} not found")


def format_group_to_dict(group: Groups) -> dict:
    out = {}



class GroupsResource(Resource):
    def get(self, group_id):
        abort_of_group_not_found(group_id)
        db_sess = db_session.create_session()
        groups = db_sess.query(Groups).get(group_id)


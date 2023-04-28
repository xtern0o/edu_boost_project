from typing import Optional

from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify

from data import db_session

from data.works import Works
from data.users import Users
from data.questions import Questions
from data.groups import Groups
from data.users import Users


def get_user_by_apikey(apikey) -> Optional[Users]:
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.apikey == apikey).first()
    if not user:
        abort(404, message="incorrect api key")
    return user


def abort_if_student(user: Users) -> None:
    if user.user_type == "student":
        abort(403, message="not allowed for students")


def abort_if_group_not_found(group_id) -> None:
    db_sess = db_session.create_session()
    if not db_sess.query(Groups).get(group_id):
        abort(404, message=f"group with id={group_id} not found")


def abort_if_not_required(user: Users, group: Groups) -> None:
    db_sess = db_session.create_session()
    if group in db_sess.query(Groups).filter(Groups.teacher == user).all():
        abort(403, message="you are not able to change this group")


def format_group_to_dict(group: Groups) -> dict:
    out = group.to_dict(only=('id', 'name', 'teacher_id', 'code'))
    out["students"] = [user.to_dict(only=('id',
                                          'first_name',
                                          'second_name',
                                          'email',
                                          'user_type')) for user in group.students]
    return out


parser_2 = reqparse.RequestParser()
parser_2.add_argument('name', required=True)
parser_2.add_argument('invites', required=True, type=str, action='append')

parser_3 = reqparse.RequestParser()
parser_3.add_argument('name', required=False)
parser_3.add_argument('invites', required=False, type=str, action='append')


class GroupsResource(Resource):
    def get(self, apikey, group_id):
        abort_if_student(get_user_by_apikey(apikey))
        abort_if_group_not_found(group_id)

        db_sess = db_session.create_session()
        group = db_sess.query(Groups).get(group_id)
        return jsonify(
            {
                "group": format_group_to_dict(group)
            }
        )

    def delete(self, apikey, group_id):
        abort_if_group_not_found(group_id)
        abort_if_student(get_user_by_apikey(apikey))

        db_sess = db_session.create_session()
        group = db_sess.query(Groups).get(group_id)

        abort_if_not_required(get_user_by_apikey(apikey), group)

        db_sess.delete(group)
        db_sess.commit()
        return jsonify(
            {
                "success": "OK"
            }
        )


class GroupsListResource(Resource):
    def get(self, apikey):
        user = get_user_by_apikey(apikey)
        abort_if_student(user)
        db_sess = db_session.create_session()
        teacher_id = user.id
        groups = db_sess.query(Groups).filter(Groups.teacher_id == teacher_id).all()
        return jsonify(
            {
                "groups": [format_group_to_dict(group) for group in groups]
            }
        )

    def post(self, apikey):
        args = parser_2.parse_args()
        user = get_user_by_apikey(apikey)
        abort_if_student(user)
        db_sess = db_session.create_session()
        if len(args['name']) >= 5:
            new_group = Groups(
                name=args['name'],
                teacher_id=user.id
            )
            db_sess.add(new_group)
            db_sess.commit()
            for i, item in enumerate(args["invites"]):
                if isinstance(item, int):
                    id = item
                    user = db_sess.query(Users).get(id)
                    if not user:
                        abort(404, message=f"user at position {i} not found")
                    user.invites_group.append(new_group)
                    db_sess.commit()
                elif isinstance(item, str):
                    email = item
                    print(email)
                    user = db_sess.query(Users).filter(Users.email == email).first()
                    print(user)
                    if not user:
                        abort(404, message=f"user at position {i} not found")
                    user.invites_group.append(new_group)
                    db_sess.commit()
            return jsonify(
                {
                    'success': 'OK'
                }
            )
        return jsonify(
            {
                'error': 'name of group should include at lest 5 symbols'
            }
        )


class GroupsPutResource(Resource):
    def put(self, group_id):
        args = parser_3.parse_args()
        abort_if_group_not_found(group_id)
        abort_if_student(get_user_by_apikey(args['apikey']))

        db_sess = db_session.create_session()
        group = db_sess.query(Groups).get(group_id)

        abort_if_not_required(get_user_by_apikey(args['apikey']), group)

        if args["name"]:
            if len(args["name"]) < 5:
                return jsonify(
                    {
                        'error': 'name of group should include at lest 5 symbols'
                    }
                )
            group.name = args["name"]
        if args["invites"]:
            for i, item in enumerate(args["invites"]):
                if isinstance(item, int):
                    id = item
                    user = db_sess.query(Users).get(id)
                    if not user:
                        abort(404, message=f"user at position {i} not found")
                    user.invites_group.append(group)
                    db_sess.commit()
                elif isinstance(item, str):
                    email = item
                    user = db_sess.query(Users).filter(Users.email == email).first()
                    if not user:
                        abort(404, message=f"user at position {i} not found")
                    user.invites_group.append(group)
                    db_sess.commit()
            return jsonify(
                {
                    "success": "OK"
                }
            )


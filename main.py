from flask import Flask, render_template, redirect, flash, get_flashed_messages, \
    url_for, abort, jsonify, request, session, make_response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, user_unauthorized
from flask_socketio import SocketIO, emit, join_room, leave_room

import datetime as dt
from statistics import mean
from random import choices
from string import ascii_letters, digits

from data import db_session
from data.users import Users
from data.groups import Groups
from data.messages import Messages
from data.questions import Questions
from data.works import Works
from data.options import Options
from data.solved_works import SolvedWorks

from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.invite_student import InviteForm, JoinGroupForm
from forms.group_creating_form import GroupCreatingForm
from forms.create_work_form import CreateWorkForm
from forms.works_beginning_form import WorksBeginningForm
from forms.edit_work_form import EditNameWorkForm
from forms.create_question_form import CreateQuestionForm
from forms.edit_question_form import EditTextQuestionForm, EditCorrectAnswerQuestionForm, EditTitleQuestionForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "maxkarnandjenyalol"
socketio = SocketIO(app, cors_allowed_origins='*')
login_manager = LoginManager()
login_manager.init_app(app)


def chose_socket_host():
    tunnel = input('input L/N (Local/Ngrok):')
    with open('./static/', 'w') as js_file:
        pass


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@socketio.on('send_message_json')
def handle_connect(data):
    db_sess = db_session.create_session()
    message = data.get('message_text')
    msg_object = Messages()
    msg_object.text = message
    msg_object.sender_id = current_user.id
    msg_object.group_id = data.get('group_id')
    db_sess.add(msg_object)
    db_sess.commit()
    json = {'message': message,
            'sender_name': f'{current_user.first_name} {current_user.second_name}',
            'pic_url': url_for('static', filename='img/erdogan.jpg'),}
    emit('updateMessage', json, to=data.get('group_id'))


@socketio.on('accept_invite')
def accept_handle(data):
    group_id = data.get('group_id')
    db_sess = db_session.create_session()
    group = db_sess.query(Groups).filter(Groups.id == group_id).first()
    user = db_sess.query(Users).filter(Users.id == current_user.id).first()
    user.invites_group.remove(group)
    user.groups.append(group)
    db_sess.commit()
    print('accepted successfully')


@socketio.on('cancel_invite')
def cancel_handle(data):
    group_id = data.get('group_id')
    db_sess = db_session.create_session()
    group = db_sess.query(Groups).filter(Groups.id == group_id).first()
    user = db_sess.query(Users).filter(Users.id == current_user.id).first()
    user.invites_group.remove(group)
    db_sess.commit()
    print('cancel_done')


@socketio.on('join_group')
def on_join(data):
    group = data.get('group')
    if group:
        join_room(group)
        print(request.sid)
    print('user connected')


@socketio.on('leave_group')
def on_leave(data):
    group = data.get('group')
    leave_room(group)
    print('user disconnect')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Главная страница")


@app.route("/login", methods=["POST", "GET"])
def login():
    if user_unauthorized:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(Users).filter(Users.email == form.email.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user, remember=form.remember_me.data)
                    return redirect(f"/profile/{user.id}")
                return render_template("login.html", title="Авторизация", message="Неверный логин или пароль", form=form)
            return render_template("login.html", title="Авторизация", message="Неверный логин или пароль", form=form)
        return render_template("login.html", title="Авторизация", form=form)
    return redirect("/profile")


@app.route("/register", methods=["POST", "GET"])
def registration():
    if user_unauthorized:
        form = RegisterForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = Users(
                email=form.email.data,
                remember=form.remember.data,
                first_name=form.first_name.data,
                second_name=form.second_name.data,
            )
            student_type = request.form.get("student-button")
            if student_type:
                user.user_type = "student"
            else:
                user.user_type = "teacher"
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            login_user(user, remember=form.remember.data)
            return redirect("/profile")
        return render_template("register.html", title="Регистрация", form=form)
    return redirect("/profile")


@app.route("/profile")
@login_required
def profile():
    return redirect(f"/profile/{current_user.id}")


@app.route("/profile/<int:user_id>")
@login_required
def profile_userid(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(Users).get(user_id)
    if user:
        works = []
        for group in user.groups:
            works.extend(group.works)
        if user.user_type == "student":
            marks = list(map(lambda n: n.mark, user.solved_works))
            params = {
                "title": f"{user.first_name} {user.second_name}",
                "n_of_works": len(user.solved_works),
                "avg_mark": "-" if not marks else mean(marks),
                "groups": user.groups,
                "works": works,
                "len_works": len(works),
                "user": user
            }
        else:
            created_works = db_sess.query(Works).filter(Works.creator == user).all()
            groups = db_sess.query(Groups).filter(Groups.teacher == user).all()
            params = {
                "title": f"{user.first_name} {user.second_name}",
                "created_works": created_works,
                "len_created_works": len(created_works),
                "groups": groups,
                "len_groups": len(groups),
                "user": user,
                "works": works,
                "len_works": len(works)
            }
        if current_user.id == user_id:
            params["my_profile"] = True
            return render_template("profile.html", **params)
        params["my_profile"] = False
        return render_template("profile.html", **params)
    abort(404)


@app.route('/chat', methods=['POST', 'GET'])
@login_required
def chat():
    form = InviteForm()
    form_accept = JoinGroupForm()
    db_sess = db_session.create_session()
    page = request.args.get('chat_id', default=None, type=int)
    if form_accept.validate_on_submit():
        code = request.form.get('code', None)
        group = db_sess.query(Groups).filter(Groups.code == code).first()
        if group:
            user = db_sess.query(Users).filter(Users.id == current_user.id).first()
            group.students.append(user)
            db_sess.commit()
    if form.validate_on_submit():
        student_email = request.form.get('email', None)
        user = db_sess.query(Users).filter(Users.email == student_email).first()
        if user:
            group = db_sess.query(Groups).filter(Groups.id == page).first()
            user.invites_group.append(group)
            db_sess.commit()
    user = db_sess.query(Users).filter(Users.id == current_user.id).first()
    if user.user_type == 'student':
        groups = user.groups
        invites = user.invites_group
    else:
        groups = db_sess.query(Groups).filter(Groups.teacher == user).all()
        invites = []
    if page:
        curr_page = db_sess.query(Groups).filter(Groups.id == page).first()
        messages = db_sess.query(Messages).filter(Messages.group_id == page)
        curr_group = db_sess.query(Groups).filter(Groups.id == page).first()
        if curr_group not in groups:
            abort(405)
    else:
        curr_page = page
        messages = None
    data = {
        'title': 'Чат',
        'groups': groups,
        'chosen_group': curr_page,
        'messages': messages,
        'invites': invites,
    }
    return render_template('chat.html', form_accept=form_accept, form=form, **data)


@app.route('/chat/creating', methods=["GET", "POST"])
@login_required
def groups_creating():
    db_sess = db_session.create_session()
    form = GroupCreatingForm()
    params = {
        "title": "Создание группы",
        "form": form
    }
    if current_user.user_type == "student":
        # TODO: Make 403 error response
        abort(405)
    if form.validate_on_submit():
        name = form.name.data
        invite_code = ''.join(choices(ascii_letters + digits, k=16))
        while db_sess.query(Groups).filter(Groups.code == invite_code).first():
            invite_code = ''.join(choices(ascii_letters + digits, k=16))
        new_group = Groups(
            name=name,
            teacher_id=current_user.id,
            code=invite_code
        )
        db_sess.add(new_group)
        db_sess.commit()
        params["success"] = True
        params["new_group_name"] = name
        params["new_group_code"] = invite_code
        return render_template("groups_creating.html", **params)

    params["title"] = "Создание группы"
    params["success"] = False
    return render_template("groups_creating.html", **params)


@app.route('/works/editing/<int:work_id>', methods=['GET', 'POST'])
@login_required
def edit_works(work_id):
    change_work_name_form = EditNameWorkForm()
    create_question_form = CreateQuestionForm()
    change_question_title = EditTitleQuestionForm()
    change_question_text = EditTextQuestionForm()
    change_question_correct_answer = EditCorrectAnswerQuestionForm()
    db_sess = db_session.create_session()
    work = db_sess.query(Works).filter(Works.id == work_id).first()
    if change_work_name_form.validate_on_submit():
        name = request.form.get('name')
        work.name = name
        db_sess.commit()
        print('name')
    elif create_question_form.validate_on_submit():
        title = request.form.get('title')
        text = request.form.get('text')
        correct_answer = request.form.get('correct_answer')
        question = Questions()
        question.header = title
        question.text = text
        question.correct_answer = correct_answer
        question.answer_type = 'text'
        question.work = work
        db_sess.add(question)
        db_sess.commit()
        print('create')
    elif change_question_text.validate_on_submit():
        quest_id = request.form.get('question_id')
        text = request.form.get('text')
        question = db_sess.query(Questions).filter(Questions.id == quest_id).first()
        question.text = text
        db_sess.commit()
        print('tex')
    elif change_question_title.validate_on_submit():
        quest_id = request.form.get('question_id')
        header = request.form.get('title')
        question = db_sess.query(Questions).filter(Questions.id == quest_id).first()
        question.header = header
        db_sess.commit()
        print('tit')
    elif change_question_correct_answer.validate_on_submit():
        quest_id = request.form.get('question_id')
        answer = request.form.get('correct_answer')
        question = db_sess.query(Questions).filter(Questions.id == quest_id).first()
        question.correct_answer = answer
        db_sess.commit()
        print('corr')
    data = {
        'work_name': work.name,
        'questions': work.questions
    }
    return render_template('work_editing.html', change_work_name_form=change_work_name_form,
                           create_question_form=create_question_form, change_question_title=change_question_title,
                           change_question_text=change_question_text,
                           change_question_correct_answer=change_question_correct_answer, **data)


@app.route('/works/creating', methods=['GET', 'POST'])
@login_required
def create_works():
    form = CreateWorkForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = db_sess.query(Users).filter(Users.id == current_user.id).first()
        name = request.form.get('name')
        work = Works()
        work.name = name
        work.creator = user
        db_sess.add(work)
        db_sess.commit()
        id = work.id
        return redirect(f'/works/editing/{id}')
    return render_template('work_creating.html', form=form)


@app.route("/works/<int:work_id>")
@login_required
def works_beginning(work_id):
    form = WorksBeginningForm()
    db_sess = db_session.create_session()
    work = db_sess.query(Works).get(work_id)
    if form.validate_on_submit():
        if current_user.user_type == "student":
            if work not in current_user.solved_works:
                # TODO: start test
                return redirect("/works/<int:work_id>/1")
            # TODO: show mark
            return render_template("works_beginning.html", title=work.name, form=form, work=work)
        # TODO: show results by students
        return render_template("works_beginning.html", title=work.name, form=form, work=work)
    return render_template("works_beginning.html", title=work.name, form=form, work=work)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.errorhandler(405)
def not_allowed(error):
    return render_template('405error.html'), 405


@app.errorhandler(404)
def not_found(error):
    return render_template('404error.html'), 404


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401error.html'), 401


if __name__ == '__main__':
    db_session.global_init("db/spermum.db")
    socketio.run(app, debug=True)

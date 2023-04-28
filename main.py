from flask import Flask, render_template, redirect, flash, get_flashed_messages, \
    url_for, abort, jsonify, request, session, make_response
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, user_unauthorized
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_restful import Api

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
from data.work_in_process import WorksInProcess
from data.temp_answers import TempAnswers

from resources import groups_resources

from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.invite_student import InviteForm, JoinGroupForm
from forms.group_creating_form import GroupCreatingForm
from forms.create_work_form import CreateWorkForm
from forms.works_beginning_form import WorksBeginningForm
from forms.edit_work_form import EditWorkForm
from forms.create_question_form import CreateQuestionForm
from forms.edit_question_form import EditQuestionForm
from forms.publish_work_form import PublishWorkForm
from forms.start_work_form import StartWorkForm
from forms.input_answer_form import InputAnswerForm
from forms.send_work_form import SendWorkForm
from forms.change_apikey_form import ChangeApikey

import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "maxkarnandjenyalol"

api = Api(app)

# апи-сервис для списка объектов
api.add_resource(groups_resources.GroupsListResource, '/api/groups/<string:apikey>')
# апи-сервис для одного объекта
api.add_resource(groups_resources.GroupsResource, '/api/groups/<string:apikey>/<int:group_id>')
# апи-сервис для put-запроса
api.add_resource(groups_resources.GroupsPutResource, '/api/groups/<string:apikey>/<int:group_id>')

print(api.resources)

login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app, cors_allowed_origins='*')


def generate_new_apikey() -> str:
    db_sess = db_session.create_session()
    apikey = ''.join(choices(ascii_letters + digits, k=16))
    while db_sess.query(Users).filter(Users.apikey == apikey).first():
        apikey = ''.join(choices(ascii_letters + digits, k=16))
    return apikey


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
                    return redirect(url_for('profile', user_id=user.id))
                return render_template("login.html", title="Авторизация", message="Неверный логин или пароль", form=form)
            return render_template("login.html", title="Авторизация", message="Неверный логин или пароль", form=form)
        return render_template("login.html", title="Авторизация", form=form)
    return redirect(url_for('profile'))


@app.route("/register", methods=["POST", "GET"])
def registration():
    if user_unauthorized:
        form = RegisterForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if not db_sess.query(Users).filter(Users.email == form.email.data).first():
                code = request.form.get('invite_code')
                user = Users(
                    email=form.email.data,
                    remember=form.remember.data,
                    first_name=form.first_name.data,
                    second_name=form.second_name.data,
                    apikey=generate_new_apikey()
                )
                student_type = request.form.get("student-button")
                if student_type:
                    user.user_type = "student"
                else:
                    user.user_type = "teacher"
                user.set_password(form.password.data)
                if code:
                    group = db_sess.query(Groups).filter(Groups.code == code).first()
                    if group:
                        user.groups.append(group)
                db_sess.add(user)
                db_sess.commit()
                login_user(user, remember=form.remember.data)
                return redirect(url_for('profile'))
            form.email.errors.append("Пользователь с данным e-mail же зарегистрирован")
        return render_template("register.html", title="Регистрация", form=form)
    return redirect(url_for('profile'))


@app.route("/profile")
@login_required
def profile():
    return redirect(url_for('profile_userid', user_id=current_user.id))


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
    change_work_form = EditWorkForm()
    create_question_form = CreateQuestionForm()
    edit_question = EditQuestionForm()
    publish_work = PublishWorkForm()
    db_sess = db_session.create_session()
    work = db_sess.query(Works).filter(Works.id == work_id).first()
    if change_work_form.validate_on_submit():
        name = request.form.get('name')
        work.name = name
        deadline = request.form.get('deadline')
        deadline = datetime.datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        work.deadline = deadline
        db_sess.commit()
    elif edit_question.validate_on_submit() and request.form.get('question_id'):
        quest_id = request.form.get('question_id')
        question = db_sess.query(Questions).filter(Questions.id == quest_id).first()
        if request.form.get('delete'):
            db_sess.delete(question)
        else:
            text = request.form.get('text')
            title = request.form.get('title')
            correct_answer = request.form.get('correct_answer')
            points = request.form.get('points')
            question.text = text
            question.header = title
            question.correct_answer = correct_answer
            question.points = points
        db_sess.commit()
    elif publish_work.validate_on_submit() and request.form.get('work_id'):
        work_id = request.form.get('work_id')
        work = db_sess.query(Works).filter(Works.id == work_id).first()
        work.is_published = 1 if work.is_published == 0 else 0
        db_sess.commit()
    elif create_question_form.validate_on_submit():
        question = Questions()
        title = request.form.get('title')
        text = request.form.get('text')
        correct_answer = request.form.get('correct_answer')
        points = request.form.get('points')
        question.header = title
        question.text = text
        question.correct_answer = correct_answer
        question.answer_type = 'text'
        question.work = work
        question.points = points
        db_sess.add(question)
        db_sess.commit()
    max_points = 0
    for question in work.questions:
        max_points += question.points
    data = {
        'work_name': work.name,
        'questions': work.questions,
        'deadline': work.deadline,
        'max_points': max_points,
        'work_is_published': work.is_published,
        'work_id': work.id,
    }
    return render_template('work_editing.html', change_work_form=change_work_form,
                           create_question_form=create_question_form, edit_question=edit_question,
                           publish_work_form=publish_work, title='Изменение работы', **data)


@app.route('/works/creating', methods=['GET', 'POST'])
@login_required
def create_works():
    form = CreateWorkForm()
    db_sess = db_session.create_session()
    groups = db_sess.query(Groups).filter(Groups.teacher_id == current_user.id).all()
    form.group.choices = [(group.id, group.name) for group in groups]
    if form.validate_on_submit():
        user = db_sess.query(Users).filter(Users.id == current_user.id).first()
        name = request.form.get('name')
        info = request.form.get('info')
        deadline = request.form.get('deadline')
        group_id = request.form.get('group')
        deadline = datetime.datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        time = request.form.get('time')
        time = datetime.datetime.strptime(time, '%H:%M').time()
        group = db_sess.query(Groups).filter(Groups.id == group_id).first()
        work = Works()
        work.name = name
        work.info = info
        work.creator = user
        work.deadline = deadline
        work.time = time
        work.is_published = 0
        db_sess.add(work)
        group.works.append(work)
        db_sess.commit()
        id = work.id
        return redirect(url_for('edit_works', work_id=id))
    return render_template('work_creating.html', form=form, groups=groups, title='Создать работу')


@app.route('/works', methods=['GET', 'POSt'])
@login_required
def works_review():
    if current_user.user_type == 'student':
        form = StartWorkForm()
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.id == current_user.id).first()
        if form.validate_on_submit():
            work_id = request.form.get('work_id')
            work = db_sess.query(Works).filter(Works.id == work_id).first()
            process_work = WorksInProcess()
            process_work.process_user = user
            process_work.process_work = work
            db_sess.add(process_work)
            db_sess.commit()
            return redirect(url_for('works_beginning', work_id=int(work_id)))
        start_works = list()
        process_works = list()
        groups = user.groups

        for group in groups:
            works_group = group.works
            proc_works = user.process_works
            solved_works = user.solved_works
            start_works.extend(db_sess.query(Works).filter(Works.id.in_([work.id for work in works_group])).\
                filter(Works.is_published == 1).
                               filter(~Works.id.in_([process_work.process_work.id for process_work in proc_works])).
                               filter(~Works.id.in_([work.work_id for work in solved_works])).all())
            process_works.extend(db_sess.query(Works).filter(Works.id.in_([work.id for work in works_group])).\
                filter(Works.is_published == 1).
                                 filter(Works.id.in_([process_work.process_work.id for process_work in proc_works])).
                                 filter(~Works.id.in_([work.work_id for work in solved_works])).all())

        data = {
            'start_works': start_works,
            'process_works': process_works
        }
        return render_template('works_review.html', form=form, title='Просмотр работ', **data)
    else:
        works = current_user.creator
        return render_template('works_review.html', works=works, title='Просмотр работ')


@app.route("/works/<int:work_id>", methods=["GET", "POST"])
@login_required
def works_beginning(work_id):
    db_sess = db_session.create_session()
    work = db_sess.query(Works).filter(Works.id == work_id).first()
    solved_work = db_sess.query(SolvedWorks).filter(SolvedWorks.work_id == work_id).\
        filter(SolvedWorks.user_id == current_user.id).first()
    if solved_work:
        return redirect(url_for('work_result', work_id=work_id))
    return render_template("works_base.html", work=work, title='Начало работа')


@app.route('/works/<int:work_id>/question/<int:question_id>', methods=["GET", "POST"])
@login_required
def works_doing(work_id, question_id):
    form = InputAnswerForm()
    send_work_form = SendWorkForm()
    db_sess = db_session.create_session()
    question = db_sess.query(Questions).filter(Questions.id == question_id).first()
    user = db_sess.query(Users).filter(Users.id == current_user.id).first()
    solved_work = db_sess.query(SolvedWorks).filter(SolvedWorks.work_id == work_id).\
        filter(SolvedWorks.user_id == current_user.id).first()
    if solved_work:
        return redirect(url_for('work_result', work_id=work_id))

    if send_work_form.validate_on_submit() and request.form.get('work_id'):
        solved_works = SolvedWorks()
        work_id = request.form.get('work_id')
        work = db_sess.query(Works).filter(Works.id == work_id).first()
        solved_works.work_id = work_id
        solved_works.user_id = current_user.id
        questions = work.questions
        all_answers = user.temp_answers
        all_points = sum([question.points for question in questions])
        got_points = sum([answer.temp_question.points for answer in all_answers
                          if answer.temp_answer == answer.temp_question.correct_answer])
        percent = got_points / all_points
        if percent < 0.52:
            solved_works.mark = 2
        elif 0.52 <= percent < 0.75:
            solved_works.mark = 3
        elif 0.75 <= percent < 0.9:
            solved_works.mark = 4
        elif 0.9 < percent:
            solved_works.mark = 5
        db_sess.add(solved_works)
        db_sess.commit()
        return redirect(url_for('work_result', work_id=work_id))
    elif form.validate_on_submit():
        answer = request.form.get('answer')
        temp_ans = db_sess.query(TempAnswers).filter(TempAnswers.user_id == current_user.id).filter(TempAnswers.question_id == question_id).first()
        if not temp_ans:
            temp_ans = TempAnswers()
        temp_ans.temp_question = question
        temp_ans.user_id = user.id
        temp_ans.temp_answer = answer
        db_sess.add(temp_ans)
        db_sess.commit()
    work = db_sess.query(Works).filter(Works.id == work_id).first()
    temp_answer_data = user.temp_answers
    temp_answers = {answer.question_id: answer.temp_answer for answer in temp_answer_data}
    data = {
        'work': work,
        'question': question,
        'temp_answers': temp_answers
    }
    return render_template('works_question.html', form=form, send_work_form=send_work_form, title='Вопрос', **data)


@app.route('/works/result/<int:work_id>', methods=["GET", "POST"])
@login_required
def work_result(work_id):
    db_sess = db_session.create_session()
    solved_work = db_sess.query(SolvedWorks).filter(SolvedWorks.work_id == work_id).\
        filter(SolvedWorks.user_id == current_user.id).first()
    work = db_sess.query(Works).filter(Works.id == work_id).first()
    questions = work.questions
    temp_answer_data = current_user.temp_answers
    temp_answers = {answer.question_id: answer.temp_answer for answer in temp_answer_data}
    data = {
        'solved_work': solved_work,
        'work': work,
        'questions': questions,
        'temp_answers': temp_answers
    }
    return render_template('work_result.html', title='Результат работы', **data)


@app.route('/apikeyshow/<int:user_id>', methods=["GET", "POST"])
@login_required
def apikey_show(user_id):
    db_sess = db_session.create_session()
    if current_user.id != user_id:
        abort(403)
    form = ChangeApikey()
    if form.validate_on_submit():
        new_apikey = generate_new_apikey()
        user = db_sess.query(Users).get(current_user.id)
        user.apikey = new_apikey
        db_sess.commit()
        return render_template("apikeyshow.html", title="Apikey", apikey=new_apikey, form=form)
    return render_template("apikeyshow.html", title="Apikey", apikey=current_user.apikey, form=form)


@app.route('/box')
def box():
    return 'чо это?'


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/works")
@login_required
def works():
    return ''

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

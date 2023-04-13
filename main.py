from flask import Flask, render_template, redirect, flash, get_flashed_messages, url_for, abort, jsonify, request, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO

import datetime as dt
from statistics import mean

from data import db_session
from data.users import Users
from data.groups import Groups
from data.messages import Messages
from data.questions import Questions
from data.works import Works
from data.solved_works import SolvedWorks

from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.chat_form import ChatForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "maxkarnlol"
socketio = SocketIO(app, cors_allowed_origins='*')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@socketio.on('send_message_json')
def handle_connect(data):
    print(session)
    print(data)


@socketio.on('message')
def handle_message(message):
    print(message)


@app.route('/')
@app.route('/index')
def index():
    return "Index"


@app.route("/login", methods=["POST", "GET"])
def login():
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


@app.route("/register", methods=["POST", "GET"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = Users(
            email=form.email.data,
            remember=form.remember.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
        )
        teacher_type = request.form.get("teacher-button")
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
            marks = list(map(lambda n: n.mark, user.solved_work))
            params = {
                "title": f"{user.first_name} {user.second_name}",
                "n_of_works": len(user.solved_work),
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
    form = ChatForm()
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == 1).first()
    groups = user.groups
    page = request.args.get('chat_id', default=None, type=int)
    curr_page = db_sess.query(Groups).filter(Groups.id == page).first()
    if form.validate_on_submit():
        print(form.message.data)
    data = {
        'groups': groups,
        'chosen_group': curr_page
    }
    return render_template('chat.html', title='Чат', form=form, **data)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    db_session.global_init("db/spermum.db")
    socketio.run(app, debug=False)

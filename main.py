from flask import Flask, render_template, redirect, flash, get_flashed_messages, \
    url_for, abort, jsonify, request, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, emit, join_room, leave_room

from data import db_session
from data.users import Users
from data.groups import Groups
from data.messages import Messages
from data.questions import Questions

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
    db_sess = db_session.create_session()
    message = data.get('message_text')
    msg_object = Messages()
    msg_object.text = message
    msg_object.sender_id = current_user.id
    msg_object.group_id = data.get('group_id')
    db_sess.add(msg_object)
    db_sess.commit()
    emit('updateMessage', {'message': message, 'sender_name': f'{current_user.first_name} {current_user.second_name}'}, to=data.get('group_id'))


@socketio.on('join_group')
def on_join(data):
    group = data.get('group')
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


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    form = ChatForm()
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == 1).first()
    groups = user.groups
    page = request.args.get('chat_id', default=None, type=int)
    if page:
        curr_page = db_sess.query(Groups).filter(Groups.id == page).first()
    else:
        curr_page = user.groups[0]
    data = {
        'groups': groups,
        'chosen_group': curr_page
    }
    return render_template('chat.html', title='Чат', form=form, **data)


@app.route('/card')
def card():
    return render_template('chat_user_cart.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    db_session.global_init("db/spermum.db")
    socketio.run(app, debug=True)

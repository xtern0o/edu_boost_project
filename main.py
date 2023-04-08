from flask import Flask, render_template, redirect, flash, get_flashed_messages, url_for, abort, jsonify, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send

from data import db_session
from data.users import Users
from data.groups import Groups
from data.messages import Messages
from data.questions import Questions

from forms.login_form import LoginForm
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


@socketio.on('connect12')
def handle_connect(data):
    print(type(data))
    print('connect', data)


@app.route('/')
@app.route('/index')
def index():
    return "index"


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
            return render_template("login.html", message="Неверный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == 1).first()
    groups = user.groups
    form = ChatForm()
    if form.validate_on_submit():
        print(form.message.data)
    data = {
        'groups': groups,
        'first_group': groups[0]
    }
    return render_template('chat.html', title='Чат', form=form, **data)


if __name__ == '__main__':
    db_session.global_init('db/spermum.db')
    socketio.run(app, debug=False)
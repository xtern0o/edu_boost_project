from data import db_session
from flask import Flask


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return


if __name__ == '__main__':
    db_session.global_init('db/spermum.db')
    app.run()

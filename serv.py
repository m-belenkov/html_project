from flask import Flask, session
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from werkzeug.security import generate_password_hash
from login import DB, BaseUs, BaseLet

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
conn = db.get_connection()
base = BaseUs(conn)
letters = BaseLet(conn)
base.init_table()
letters.init_table()

good_mail = ['gmail.com', 'mail.ru', 'yandex.ru']
name_of_act_user = ''


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    global name_of_act_user
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        exists = base.exists(request.form['email'], generate_password_hash(request.form['password']))
        # print(exists)
        if exists[0]:
            name_of_act_user = request.form['email']
            # session['username'] = cur_name
            # session['user_id'] = exists[1]
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    global name_of_act_user
    global good_mail
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        email = request.form['emailreg']
        if '@' in email and email.split('@')[1] in good_mail:
            base.insert(request.form['emailreg'], generate_password_hash(request.form['passwordreg']))
            name_of_act_user = request.form['emailreg']
            return redirect(url_for('main'))
        else:
            return redirect(url_for('registration'))


@app.route('/main', methods=['GET', 'POST'])
def main():
    global name_of_act_user
    if request.method == 'GET':
        theme = []
        for i in letters.get_all():
            if i[3] == name_of_act_user:
                theme.append(i)
        return render_template('main.html', themes=theme, user=name_of_act_user)
    elif request.method == 'POST':
        name_of_act_user = ''
        return redirect(url_for('login'))


@app.route('/main/<id>', methods=['POST', 'GET'])
def incoming(id):  # входящие
    if request.method == 'GET':
        themes = letters.get(id)
        return render_template('theme.html', id=id, themes=themes)


@app.route('/sent_letter', methods=['GET', 'POST'])
def add_theme():
    if request.method == 'GET':
        return render_template('add_theme.html')
    elif request.method == 'POST':
        letters.insert(request.form['title'], request.form['text'],
                       request.form['name'])
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

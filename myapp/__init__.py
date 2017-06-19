from flask import Flask, render_template, request, url_for, redirect, flash
import flask_login

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

# 数据库用户
users = {
    'admin@admin.com': {'pw': 'admin'}
}


class User(flask_login.UserMixin):
    user = ''
    email = ''


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


@app.route('/')
def homepage():
    return 'hello'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    if request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('dashboard'))

    return 'Bad login'


@app.route('/protected/')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/logout/')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/dashboard/')
@flask_login.login_required
def dashboard():
    return render_template('dashboard/index.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'
if __name__ == "__main__":
    app.run()

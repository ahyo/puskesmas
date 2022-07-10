# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from flask_bootstrap import Bootstrap5, SwitchField
from flask_wtf import  CSRFProtect
from forms import *
from myApi import *
import requests, json
from typing import Dict, Optional
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
    
app = Flask(__name__)

login_manager = LoginManager(app)
users: Dict[str, "User"] = {}

app.secret_key = 'dev'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'  # uncomment this line to test bootswatch theme

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

class User(UserMixin):
    def __init__(self, id: str, username: str, token: str, password: str, access: str):
        self.id = id
        self.username = username
        self.token = token
        self.password = password
        self.access = access

    @staticmethod
    def get(user_id: str) -> Optional["User"]:
        return users.get(user_id)

    def __str__(self) -> str:
        return f"<Id: {self.id}, Username: {self.username}, Token: {self.token}, Access: {self.access}>"

    def __repr__(self) -> str:
        return self.__str__()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {'no_ktp':form.no_ktp.data,'nama':form.nama.data,'alamat':form.alamat.data,'password':form.password.data}
        resp = api_call('pasien/register',data)
        info = ''
        if 'message' in resp:
            info = resp['message']
        if info:
            flash(info)
        return redirect(url_for('index'))

    return render_template(
        'register_form.html',
        form=form
    )

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.validate_on_submit():
        data = {'no_ktp':form.username.data,'password':form.password.data}
        resp = api_call('pasien/login',data)
        if 'status' in resp and resp['status']==200:
            return redirect(url_for('index'))
        if 'message' in resp:
            flash(resp['message'],'error')    
    return render_template(
        'login_form.html',
        form=form,
    )

@app.route('/form', methods=['GET', 'POST'])
def test_form():
    form = HelloForm()
    if form.validate_on_submit():
        flash('Form validated!')
        return redirect(url_for('index'))
    return render_template(
        'form.html',
        form=form,
        telephone_form=TelephoneForm(),
        contact_form=ContactForm(),
        im_form=IMForm(),
        button_form=ButtonForm(),
        example_form=ExampleForm()
    )


@app.route('/nav', methods=['GET', 'POST'])
def test_nav():
    return render_template('nav.html')


@app.route('/pagination', methods=['GET', 'POST'])
def test_pagination():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    return render_template('pagination.html', pagination=pagination, messages=messages)


@app.route('/flash', methods=['GET', 'POST'])
def test_flash():
    flash('A simple default alert—check it out!')
    flash('A simple primary alert—check it out!', 'primary')
    flash('A simple secondary alert—check it out!', 'secondary')
    flash('A simple success alert—check it out!', 'success')
    flash('A simple danger alert—check it out!', 'danger')
    flash('A simple warning alert—check it out!', 'warning')
    flash('A simple info alert—check it out!', 'info')
    flash('A simple light alert—check it out!', 'light')
    flash('A simple dark alert—check it out!', 'dark')
    flash(Markup('A simple success alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.'), 'success')
    return render_template('flash.html')


@app.route('/table')
def test_table():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page, per_page=10)
    messages = pagination.items
    titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'), ('create_time', 'Create Time')]
    return render_template('table.html', messages=messages, titles=titles, Message=Message)


@app.route('/table/<int:message_id>/view')
def view_message(message_id):
    message = Message.query.get(message_id)
    if message:
        return f'Viewing {message_id} with text "{message.text}". Return to <a href="/table">table</a>.'
    return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'


@app.route('/table/<int:message_id>/like')
def like_message(message_id):
    return f'Liked the message {message_id}. Return to <a href="/table">table</a>.'


@app.route('/table/new-message')
def new_message():
    return 'Here is the new message page. Return to <a href="/table">table</a>.'


@app.route('/icon')
def test_icon():
    return render_template('icon.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8000)
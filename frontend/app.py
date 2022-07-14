# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, Markup, redirect, url_for,session
from flask_bootstrap import Bootstrap5, SwitchField
from flask_wtf import  CSRFProtect
from forms import *
from myApi import *
import requests, json
from typing import Dict, Optional
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
    
app = Flask(__name__)

login_manager = LoginManager(app)
#users: Dict[str, "User"] = {}

class Table():
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        for arg in args:
            setattr(self, arg, arg) if isinstance(arg, str) else setattr(self, str(arg), arg)
    def __str__(self):
        return 'This is the example class'
    def __getitem__(self, obj):
        return self.__dict__[obj]
    def __len__(self):
        return len(self.__dict__.items())
    def __iter__(self):
        return iter(self.__dict__)

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
    def __init__():
        return [{'id':1}]

@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/poli')
def polis():
    resp = api_get('poli/','',session['token'])
    data = {}
    titles = [('_id', '#'), ('name', 'Nama Poli')]
    if 'status_code' in resp and resp['status_code']==200:
        data = resp['data']
    return render_template('poli.html',data=data,titles=titles)    

@app.route('/poli-add',methods=['GET','POST'])
def poli_new():
    form = PoliForm()
    if form.validate_on_submit():
        data = {'name':form.nama.data}
        resp = api_post('poli/',data,session['token'])
        flash(resp)
    return render_template('poli_form.html',form=form)    

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        data = {'no_ktp':form.no_ktp.data,'nama':form.nama.data,'alamat':form.alamat.data,'password':form.password.data}
        resp = api_post('pasien/register',data)
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
        data = {'username':form.username.data,'password':form.password.data}
        resp = api_post('admin/login',data)
        #flash(resp)
        if 'access_token' in resp:
            session['token'] = resp['access_token']
            return redirect(url_for('index'))
        if 'detail' in resp:
            flash(resp['detail'],'error')    
    return render_template(
        'login_form.html',
        form=form,
    )

@app.route('/pendaftaran', methods=['GET','POST'])
def pendaftaran():
    form = PendaftaranForm()
    if form.validate_on_submit():
        data = {'username':form.username.data,'password':form.password.data}
        resp = api_post('admin/login',data)
        #flash(resp)
        if 'access_token' in resp:
            session['token'] = resp['access_token']
            return redirect(url_for('index'))
        if 'detail' in resp:
            flash(resp['detail'],'error')    
    return render_template(
        'pendaftaran_form.html',
        form=form,
    )    

@app.route("/logout")
def logout():
    session['token'] = False
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80)
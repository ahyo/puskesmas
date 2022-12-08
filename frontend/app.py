# -*- coding: utf-8 -*-
import asyncio
from crypt import methods
from datetime import datetime as waktu
from urllib.request import Request
from flask import Flask, render_template, request, flash, Markup, redirect, url_for, session
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import Model, SQLAlchemy
from flask_wtf import CSRFProtect
from gtts import gTTS
from io import BytesIO
import os

from sqlalchemy import true
from forms import *
from myApi import *
import requests
import json
from typing import Dict, Optional
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.init_app(app)
#users: Dict[str, "User"] = {}


class Table():
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        for arg in args:
            setattr(self, arg, arg) if isinstance(
                arg, str) else setattr(self, str(arg), arg)

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
app.config['BOOTSTRAP_BTN_SIZE'] = 'md'
# uncomment this line to test bootswatch theme
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cerulean'

# set default icon title of table actions
app.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
app.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
app.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
app.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


class User(UserMixin):
    def __init__():
        if 'token' in session:
            return session['token']
        else:
            return None


class Poli(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.Text, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


login_manager.login_view = "login_form"


@app.route('/')
def index():
    data = []
    resp = api_get('public/antrian', None)
    if 'data' in resp:
        data = resp['data']
    # flash(resp)
    return render_template(
        'index.html',
        data=data
    )


@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginForm()
    if form.validate_on_submit():
        data = {'username': form.username.data, 'password': form.password.data}
        resp = api_post('admin/login', data)
        # flash(resp)
        if 'access_token' in resp:
            session['token'] = resp['access_token']
            # login_user(session['token'])
            return redirect(url_for('index'))
        if 'detail' in resp:
            flash(resp['detail'], 'error')
    return render_template(
        'login_form.html',
        form=form,
    )


@app.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('index'))


### POLI #################
@app.route('/poli')
def polis():
    token = ''
    if 'token' in session:
        token = session['token']

    resp = api_get('poli/', '', token)
    data = {}
    titles = [('id', '#'), ('nama', 'Nama Poli'), ('alias', 'Alias Antrian')]
    if 'status_code' in resp and resp['status_code'] == 200:
        data = resp['data']
    db.drop_all()
    db.create_all()
    for row in data:
        t = Poli(
            _id=row["_id"],
            nama=row["nama"],
            alias=row["alias"]
        )
        db.session.add(t)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    pagination = Poli.query.paginate(page, per_page=10)
    messages = pagination.items
    return render_template('poli.html', messages=messages, Poli=Poli, titles=titles)


@app.route('/poli-add', methods=['GET', 'POST'])
def poli_new():
    token = ''
    if 'token' in session:
        token = session['token']
    form = PoliForm()
    if form.validate_on_submit():
        data = {'nama': form.nama.data, 'alias': form.alias.data}
        resp = api_post('poli/', data, token)
        if 'description' in resp:
            flash(resp['description'])
        if 'detail' in resp:
            flash(resp['detail'], 'error')
    return render_template('poli_form.html', form=form, caption='Tambah')


@app.route('/poli-edit/<id>', methods=['GET', 'POST'])
def poli_edit(id):
    token = ''
    if 'token' in session:
        token = session['token']
    data = []
    poli = api_get('poli/'+id, None, token)
    if 'data' in poli:
        data = poli['data']
    # flash(data['nama'])
    form = PoliForm()
    if (request.method == 'GET'):
        form.nama.data = data['nama']
        form.alias.data = data['alias']
    if form.validate_on_submit():
        data = {'nama': form.nama.data, 'alias': form.alias.data}
        resp = api_put('poli/'+id, data, token)
        # flash(resp)
        return redirect(url_for('polis'))
    return render_template('poli_form.html', form=form, caption='Edit')


@app.route('/poli-view/<id>', methods=['GET', 'POST'])
def poli_view(id):
    token = ''

    if 'token' in session:
        token = session['token']
    poli = None
    kunjungan = None
    resp = api_get('poli/'+id, None, token)
    if 'data' in resp:
        poli = resp['data']
    # flash(resp)

        data = {'poli': poli['_id'], 'tanggal': 'tidak-perlu'}
        resp = api_get('kunjungan/poli/', data, token)
        if 'data' in resp:
            kunjungan = resp['data']
    # flash(resp)
    return render_template('poli_view.html', poli=poli, kunjungan=kunjungan)


@app.route('/poli-diagnosa/<poli_id>/<kunjungan_id>', methods=['GET', 'POST'])
def poli_diagnosa(poli_id, kunjungan_id):
    # cek token
    bell = 'bell.mp3'

    token = ''
    if 'token' in session:
        token = session['token']
    nama = ""
    # poli detail
    detail = api_get('poli/'+poli_id, None, token)
    if 'data' in detail:
        nama = detail['data']['nama']

    # kunjungan detail
    pid = '0'
    kunjungan = []
    kunjung = api_get('kunjungan/'+kunjungan_id, None, token)
    if 'data' in kunjung:
        kunjungan = kunjung['data']

    basepath = os.getcwd()
    mp3 = poli_id+'.mp3'
    tts = gTTS('Mohon Perhatian, Nomor antrian '+kunjungan['nomor'].strip(
        "-")+', atas nama '+kunjungan['nama_kk']+' dari '+kunjungan['alamat']+', silahkan ke bagian '+nama, lang='id')
    tts.save(basepath+'/static/'+mp3)

    # set antrian di poli
    api_put('poli/'+poli_id, {'antrian': kunjungan['nomor']}, token)
    # flash(put)
    form = DiagnosaForm()
    form.poli_id.data = poli_id
    form.kunjungan_id.data = kunjungan_id
    kunjungan = api_get('kunjungan/'+kunjungan_id, None, token)
    if 'data' in kunjungan:
        form.no_mr.data = kunjungan['data']['no_mr']
    if form.validate_on_submit():
        data = {'poli_id': form.poli_id.data, 'no_mr': form.no_mr.data,
                'kunjungan_id': form.kunjungan_id.data, 'diagnosa': form.diagnosa.data}
        #files = {'nama':'test','suara_jantung':form.suara_jantung.data,'suara_paru':form.suara_paru.data}
        nama = {'nama': 'test'}
        files = {
            'nama': (None, json.dumps(nama), 'application/json'),
            'suara_jantung': form.suara_jantung.data,
            'suara_paru': form.suara_paru.data
        }
        # save diagnosa
        save = api_post('diagnosa', data, token)
        # upload files
        upload = api_file('diagnosa/upload', files, token)

        # update kunjungan untuk antrian
        put = api_put('kunjungan/'+kunjungan_id, {'status': 'Finished'}, token)
        # flash(put)
        return redirect(url_for('poli_view', id=poli_id))

    return render_template('poli_diagnosa.html', form=form, mp3=mp3, kunjungan=kunjungan['data'], bell=bell)


class MyObject:
    def __init__(self, d=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)

### ---- KUNJUNGAN ---- ####


@app.route('/kunjungan', methods=['GET', 'POST'])
def kunjungan():

    choice = []
    list_kunjungan = []
    token = ''
    if 'token' in session:
        token = session['token']
    # daftar kunjungan
    kunjungan = api_get('kunjungan', None)
    if 'data' in kunjungan:
        list_kunjungan = kunjungan['data']
    # flash(kunjungan)

    polis = api_get('kunjungan/list_poli/', '', token)
    if 'data' in polis:
        for list in polis['data']:
            item = (list['_id'], list['nama'])
            choice.append(item)
            # flash(list)
    form = KunjunganForm(poli_choices=choice)

    if form.validate_on_submit():

        # validat no.mr
        pas = api_get('public/pasien/'+form.no_mr.data)
        flash(pas)
        if 'data' in pas:
            nama_kk = pas['data']['nama']
            alamat = pas['data']['alamat']
        else:
            nama_kk = ''
            alamat = ''
            # flash("No.MR tidak valid", "error")

        # hit dulu untuk mendapatkan nomor antrian
        tgl = date.today().strftime('%Y-%m-%d')
        jam = waktu.now().strftime('%H:%M:%S')
        data = {'tanggal': tgl,
                'poli': form.poli.data}
        resp = api_get('kunjungan/nomor_antrian', data, token)
        # flash(resp)
        nomor = 1
        if 'data' in resp and len(nama_kk) > 0:
            nomor = resp['data']['nomor']
            alias = resp['data']['alias']
            if not form.poli.data:
                cname = ''
            else:
                cname = dict(choice)[form.poli.data]

            data = {'nomor': nomor, 'no_mr': form.no_mr.data, 'nama_kk': nama_kk,
                    'tanggal': tgl, 'jam': jam,
                    'poli_id': form.poli.data, 'poli': cname, 'alias': alias, 'alamat': alamat}
            resp = api_post('kunjungan', data, token)
            # flash(resp)
            if 'description' in resp:
                flash(resp['description'])
            if 'detail' in resp:
                flash(resp['detail'], 'error')
            return redirect(url_for('kunjungan'))
    return render_template(
        'kunjungan_form.html',
        form=form,
        list_kunjungan=list_kunjungan
    )


# ANTRIAN
@app.route("/antrian")
def antrian():
    data = []
    resp = api_get('public/antrian', None)
    if 'data' in resp:
        data = resp['data']
    # flash(resp)
    return render_template(
        'antrian.html',
        data=data
    )


# PASIEN
@app.route("/pasien")
def pasien():
    token = ''
    if 'token' in session:
        token = session['token']

    resp = api_get('pasien', None, token)
    data = {}
    titles = ['#', 'Nomor Pasien', 'Nama Pasien',
              'Alamat Pasien', 'Tempat Lahir']
    if 'status_code' in resp and resp['status_code'] == 200:
        data = resp['data']
    return render_template('pasien.html', data=data, titles=titles)


@app.route('/pasien-add', methods=['GET', 'POST'])
def pasien_add():
    token = ''
    if 'token' in session:
        token = session['token']
    form = PasienForm()
    if form.validate_on_submit():
        nomor = form.nomor.data
        res = api_get('pasien/nomor', None, token)
        # print(res)
        if 'data' in res:
            nomor = res['data']
        data = {'nomor': nomor, 'nama': form.nama.data, 'alamat': form.alamat.data, 'tempat_lahir': form.tempat_lahir.data,
                'tanggal_lahir': form.tanggal_lahir.data.strftime("%Y-%m-%d"), 'jenis_kelamin': form.jenis_kelamin.data}
        resp = api_post('pasien/', data, token)
        # flash(resp)
        if 'detail' in resp:
            flash(resp['detail'])
        if 'description' in resp:
            flash(resp['description'])
        # jika add ke pendaftaran = yes,langsung daftar
        #
        # #
        no_pasien = nomor
        if form.add_daftar.data == "Yes":
            tgl = date.today().strftime('%Y-%m-%d')
            jam = waktu.now().strftime('%H:%M:%S')
            # get first polly
            #poli_id = "6343820ccd188f72ab7cbe9c"
            p = api_get('poli/first')

            poli_id = p['data']['_id']

            data = {'tanggal': tgl,
                    'poli': poli_id}
            resp = api_get('kunjungan/nomor_antrian', data, token)
            # flash(resp)
            nomor = 1
            if 'data' in resp:
                nomor = resp['data']['nomor']
                alias = resp['data']['alias']
                cname = 'Poli Umum'

                data = {'nomor': nomor, 'no_mr': no_pasien, 'nama_kk': form.nama.data,
                        'tanggal': tgl, 'jam': jam,
                        'poli_id': poli_id, 'poli': cname, 'alias': alias, 'alamat': form.alamat.data}
                resp = api_post('kunjungan', data, token)
                # flash(resp)
    return render_template('pasien_form.html', form=form)


@app.route('/pasien-update/<id>', methods=['GET', 'POST'])
def pasien_update(id):
    form = PasienForm()
    token = ''
    if 'token' in session:
        token = session['token']
    if request.method == 'GET':
        res = api_get('pasien/'+id, None, token)
        # flash(res)
        form.nomor.data = res['data']['nomor']
        form.no_ktp.data = res['data']['no_ktp']
        form.nama.data = res['data']['nama']
        form.alamat.data = res['data']['alamat']
        form.tempat_lahir.data = res['data']['tempat_lahir']
        tgl = waktu.strptime(res['data']['tanggal_lahir'], "%Y-%m-%d")
        form.tanggal_lahir.data = tgl
        form.jenis_kelamin.data = res['data']['jenis_kelamin']

    if form.validate_on_submit():

        data = {'nomor': form.nomor.data, 'no_ktp': form.no_ktp.data, 'nama': form.nama.data, 'alamat': form.alamat.data, 'tempat_lahir': form.tempat_lahir.data,
                'tanggal_lahir': form.tanggal_lahir.data.strftime("%Y-%m-%d"), 'jenis_kelamin': form.jenis_kelamin.data}
        resp = api_put('pasien/'+id, data, token)
        if 'detail' in resp:
            flash(resp['detail'])
        if 'description' in resp:
            flash(resp['description'])
    return render_template('pasien_form.html', form=form, update=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)

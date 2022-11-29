from db import db
from flask import Blueprint, Flask, render_template, request, flash, Markup, redirect, url_for,session
from myApi import *
from forms import *

poli_page = Blueprint('poli_page', __name__, template_folder='templates')
@poli_page.route('/poli')
def polis():
    resp = api_get('poli/','',session['token'])
    data = {}
    titles = [('id', '#'), ('nama', 'Nama Poli'),('alias', 'Alias Antrian')]
    if 'status_code' in resp and resp['status_code']==200:
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
    return render_template('poli.html',messages=messages,Poli=Poli,titles=titles)    

@poli_page.route('/poli-add',methods=['GET','POST'])
def poli_new():
    form = PoliForm()
    if form.validate_on_submit():
        data = {'nama':form.nama.data,'alias':form.alias.data}
        resp = api_post('poli/',data,session['token'])
        flash(resp['description'])
    return render_template('poli_form.html',form=form)    

@poli_page.route('/poli-edit/{id}',methods=['GET','POST'])
def poli_edit():
    form = PoliForm()
    if form.validate_on_submit():
        data = {'nama':form.nama.data,'alias':form.alias.data}
        resp = api_post('poli/',data,session['token'])
        flash(resp['description'])
    return render_template('poli_form.html',form=form)    

@poli_page.route('/poli-view/<id>',methods=['GET','POST'])
def poli_view(id):
    poli = []
    resp = api_get('poli/'+id,None,session['token'])
    if 'data' in resp:
        poli = resp['data']
        #flash(poli)
    kunjungan = []    
    data = {'poli':poli['nama'],'tanggal':'tidak-perlu'}    
    resp = api_get('kunjungan/poli/',data,session['token'])
    if 'data' in resp:
        kunjungan = resp['data']

    form = PoliForm()
    # if form.validate_on_submit():
    #     data = {'nama':form.nama.data,'alias':form.alias.data}
    #     resp = api_post('poli/',data,session['token'])
    #     flash(resp['description'])
    return render_template('poli_view.html',poli=poli,kunjungan=kunjungan,form=form)    

@poli_page.route("/poli_detail")
def poli_detail():
    return render_template('index.html')
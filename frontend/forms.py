from datetime import date, datetime
from distutils.text_file import TextFile
from email.policy import default
from secrets import choice
from flask_wtf import FlaskForm
from flask_bootstrap import SwitchField
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import *


class RegisterForm(FlaskForm):
    no_ktp = StringField('No.KTP', validators=[DataRequired(), Length(16, 20)])
    nama = StringField('Nama Lengkap', validators=[
                       DataRequired(), Length(3, 50)])
    alamat = StringField('Alamat', validators=[DataRequired(), Length(3, 100)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(1, 150)])
    submit = SubmitField()


class PasienForm(FlaskForm):
    nomor = StringField('Nomor Pasien', default="Otomatis")
    no_ktp = StringField('No.KTP', validators=[DataRequired(), Length(3, 20)])
    nama = StringField('Nama Lengkap', validators=[
                       DataRequired(), Length(3, 50)])
    alamat = StringField('Alamat', validators=[DataRequired(), Length(3, 100)])
    tempat_lahir = StringField('Tempat Lahir', validators=[
                               DataRequired(), Length(3, 100)])
    tanggal_lahir = DateField('Tanggal Lahir', format='%Y-%m-%d')
    jenis_kelamin = RadioField('Jenis Kelamin', choices=[
                               'M', 'F'], default='M')
    add_daftar = RadioField('Tambah ke pendaftaran', choices=[
        'Yes', 'No'], default='Yes')

    submit = SubmitField(label="Submit Data Pasien")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 50)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(1, 150)])
    submit = SubmitField()


class PoliForm(FlaskForm):
    nama = StringField('Nama Poli', validators=[DataRequired(), Length(1, 50)])
    alias = StringField('Alias Antrian')
    submit = SubmitField()


class PendaftaranForm(FlaskForm):
    def __init__(self, poli_choices: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if poli_choices:
            self.poli.choices = poli_choices
    nomor = StringField('Nomor Pasien')
    nama = StringField('Nama Pasien', validators=[
                       DataRequired(), Length(1, 50)])
    alamat = StringField('Alamat', validators=[DataRequired(), Length(1, 50)])
    poli = SelectField('Poli Yang Dituju', choices=[
                       ('Poli Umum', 'Poli Umum')])
    tanggal = HiddenField('Tanggal', default=date.today().strftime("%Y-%m-%d"))
    submit = SubmitField()


class KunjunganForm(FlaskForm):
    def __init__(self, poli_choices: list = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if poli_choices:
            self.poli.choices = poli_choices
    no_mr = StringField('No.MR', validators=[DataRequired(), Length(5, 5)])
    nama_kk = StringField('Nama KK', validators=[
                          DataRequired(), Length(3, 100)])
    alamat = StringField('Alamat', validators=[DataRequired(), Length(3, 100)])
    poli = SelectField('Poli Yang Dituju', choices=[
                       ('', 'Belum Ada Poli')], validators=[DataRequired()])
    tanggal = HiddenField('Tanggal', default=date.today().strftime("%Y-%m-%d"))
    submit = SubmitField(label='Tambahkan Ke Antrian')


class HelloForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class ButtonForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(1, 20)])
    confirm = SwitchField('Confirmation')
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class DiagnosaForm(FlaskForm):
    no_mr = HiddenField()
    poli_id = HiddenField()
    kunjungan_id = HiddenField()
    diagnosa = SelectField('Hasil Diagnosa', choices=[
        ('Healthy', 'Healthy'), ('URTI', 'URTI'), ('COPD', 'COPD'), ('Pneumonia', 'Pneumonia'), ('Bronchiectasis', 'Bronchiectasis'), ('Bronchiolitis', 'Bronchiolitis')], validators=[DataRequired()])

    submit = SubmitField(label='Selesai Diagnosa')


class IMForm(FlaskForm):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()

#!/usr/bin/env python3

from datetime import date
from fileinput import filename
import json
import os
import sys
import time
from os import listdir
from os.path import isfile, join
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import askyesno
from turtle import title
from PIL import ImageTk, Image
from tkinter import ttk


#from tkinter import ttk
#import tkinter.font as tkFont
from widgets import *
from recording import start_recording
from imaging import generate_image
from myApi import get_list_kunjungan, api_post, api_file


class PrintLogger():  # create file like object
    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.insert(tk.END, text)  # write text to textbox
        # could also scroll to end of textbox here to make sure always visible

    def flush(self):  # needed for file like object
        pass


app = tk.Tk()
app.title("Digital Stetoskop")
app.configure(bg='white')
# setting window size
width = 1280
height = 720
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2, (screenheight - height) / 2)
app.geometry(alignstr)
app.resizable(width=False, height=False)

app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=1)
app.columnconfigure(2, weight=1)

col_width = 425
row_height = 210

files_to_upload = []

# statusbar = tk.Text(app)
# statusbar.grid(column=2, sticky=tk.SW)

# pl = PrintLogger(statusbar)

# # replace sys.stdout with our object
# sys.stdout = pl

# -- row 1
frame_al = tk.LabelFrame(app, text="Anterior Left", labelanchor='n',  background="white", width=col_width,
                         height=row_height)
frame_al.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

frame_ar = tk.LabelFrame(app, text="Anterior Right", labelanchor='n',  background="white",
                         width=col_width, height=row_height)
frame_ar.grid(column=1, row=0, sticky=tk.N, padx=5, pady=5)

frame_tr = tk.LabelFrame(app, text="Trachea", labelanchor='n',  background="white",
                         width=col_width, height=row_height)
frame_tr.grid(column=2, row=0, sticky=tk.E, padx=5, pady=5)

img_x = 0
img_y = 0
img_width = 100
img_height = 100

# --- row 2

frame_pl = tk.LabelFrame(app, text="Posterior Left", labelanchor='n',  background="white", width=col_width,
                         height=row_height)
frame_pl.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

frame_pr = tk.LabelFrame(app, text="Posterior Right", labelanchor='n',  background="white",
                         width=col_width, height=row_height)
frame_pr.grid(column=1, row=1, sticky=tk.N, padx=5, pady=5)

frame_data = tk.LabelFrame(app, text="Patient", labelanchor='n',  background="white",
                           width=col_width, height=row_height)
frame_data.grid(column=2, row=1, sticky=tk.E, padx=5, pady=5)

# --- row 3

frame_ll = tk.LabelFrame(app, text="Lateral Left", labelanchor='n',  background="white", width=col_width,
                         height=row_height)
frame_ll.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

frame_lr = tk.LabelFrame(app, text="Lateral Right", labelanchor='n',  background="white",
                         width=col_width, height=row_height)
frame_lr.grid(column=1, row=2, sticky=tk.N, padx=5, pady=5)

frame_result = tk.LabelFrame(app, text="", labelanchor='n',  background="white",
                             width=col_width, height=row_height, bd=0)
frame_result.grid(column=2, row=2, sticky=tk.E, padx=5, pady=5)

# #list_box = MyListbox(app,x=10,y=50,height=35,width=30)
# global bg_white
# new_size = (430, 235)
# bg_white = ImageTk.PhotoImage(Image.open(
#     'images/bg_white.jpg').resize(new_size))

# column 2
r1 = 0
r2 = 430
r3 = 860
c1 = 0
c2 = 235
c3 = 470

image_height = 5
image_width = 22

f1 = 980
l1 = 870

col_x = 10

# # column 3
MyLabel(frame_data, x=col_x, y=10, anchor='w', text="No.MR:", size=18)
MyLabel(frame_data, text="Name:", x=col_x, y=60, bd=1, anchor='w', size=18)
lbl_nama = MyLabel(frame_data, x=150, y=60, bd=1,
                   text="Nayla Aisy**", anchor='w',  size=18)
MyLabel(frame_data, text="Address:", x=col_x, y=110, anchor='w', size=18)
lbl_alamat = MyLabel(frame_data, text="Bogor",
                     anchor='w', x=150, y=110, size=18)


global kunjungan_list
# Create a Tkinter variable
tkvar = tk.StringVar(frame_data)
nomor = ''
nama = ''
alamat = ''
# Dictionary with options
choices = []
# set the default option
kunjungan_list = get_list_kunjungan()
for kunjungan in kunjungan_list:
    choices.append(kunjungan['no_mr'])
    # Dictionary with options
    #choices = {'000'}
    # tkvar.set('000')  # set the default option
if kunjungan_list:
    nomor = kunjungan_list[0]['no_mr']
    nama = text = kunjungan_list[0]['nama_kk']
    alamat = text = kunjungan_list[0]['alamat']

if not choices:
    choices = ['']
tkvar.set(nomor)
lbl_nama.config(text=nama)
lbl_alamat.config(text=alamat)

n = tk.StringVar()
nomor_mr = ttk.Combobox(frame_data, value=choices)
nomor_mr.place(x=150, y=10)
nomor_mr.current(0)

#popupMenu = tk.OptionMenu(frame_data, tkvar, *choices)
#popupMenu.place(x=150, y=10)

img_size = 30

img_al = MyLabel(frame_al, text="Anterior Left", size=img_size,
                 anchor='center',  width=image_width, height=image_height)
img_pl = MyLabel(frame_pl, text="Posterior Left", size=img_size,
                 anchor='center',  width=image_width, height=image_height)
img_ll = MyLabel(frame_ll, text="Lateral Left", size=img_size,
                 anchor='center',  width=image_width, height=image_height)

img_ar = MyLabel(frame_ar, text="Anterior Right", size=img_size,
                 anchor='center',  width=image_width, height=image_height)
img_pr = MyLabel(frame_pr, text="Posterior Right", size=img_size,
                 anchor='center',  width=image_width, height=image_height)
img_lr = MyLabel(frame_lr, text="Lateral Right", size=img_size,
                 anchor='center', width=image_width, height=image_height)

img_tr = MyLabel(frame_tr, text="Trachea", anchor='center', size=img_size,
                 width=image_width, height=image_height)

lbl_result = MyLabel(frame_result, text="Result", anchor='w', x=0, y=100)

# demo

img_width = 410
img_height = 194


def add_to_upload(file):
    global files_to_upload
    if file not in files_to_upload:
        files_to_upload.append(file)
    # print(files_to_upload)


def image_al(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Anterior Kiri',
                      message='Letakan diafragma pada Anterior Kiri, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_AL_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_al.configure(image=img)
        img_al.image = img
        img_al['height'] = img_height
        img_al['width'] = img_width
        add_to_upload(file)


def image_pl(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Posterior Kiri',
                      message='Letakan diafragma pada Posterior Kiri, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_PL_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_pl.configure(image=img)
        img_pl.image = img
        img_pl['height'] = img_height
        img_pl['width'] = img_width
        add_to_upload(file)


def image_ll(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Lateral Kiri',
                      message='Letakan diafragma pada Lateral Kiri, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_LL_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_ll.configure(image=img)
        img_ll.image = img
        img_ll['height'] = img_height
        img_ll['width'] = img_width
        add_to_upload(file)


def image_ar(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Anterior Kanan',
                      message='Letakan diafragma pada Anterior Kanan, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_AR_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_ar.configure(image=img)
        img_ar.image = img
        img_ar['height'] = img_height
        img_ar['width'] = img_width
        add_to_upload(file)


def image_pr(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Posterior Kanan',
                      message='Letakan diafragma pada Posterior Kanan, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_PR_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_pr.configure(image=img)
        img_pr.image = img
        img_pr['height'] = img_height
        img_pr['width'] = img_width
        add_to_upload(file)


def image_lr(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Lateral Kanan',
                      message='Letakan diafragma pada Lateral Kanan, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_LR_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_lr.configure(image=img)
        img_lr.image = img
        img_lr['height'] = img_height
        img_lr['width'] = img_width
        add_to_upload(file)


def image_tr(event):
    # Heart, On check
    global files_to_upload
    answer = askyesno(title='Rekam Trachea',
                      message='Letakan diafragma pada Trachea, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = nomor_mr.get()+'_TR_' + \
            date.today().strftime('%Y%m%d')
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (img_width, img_height)
        file = 'images/'+filename+'.png'
        img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
        img_tr.configure(image=img)
        img_tr.image = img
        img_tr['height'] = img_height
        img_tr['width'] = img_width
        add_to_upload(file)


def reset():
    global files_to_upload
    global kunjungan_list
    answer = askyesno(title='Reset Data',
                      message='Yakin hapus semua data?')
    if not answer:
        return False
    img_al.config(image="")
    img_ar.config(image="")
    img_pl.config(image="")
    img_pr.config(image="")
    img_ll.config(image="")
    img_lr.config(image="")
    img_tr.config(image="")

    lbl_result.config(text="Result")
    files_to_upload = []

    choices = []

    # set the default option
    kunjungan_list = get_list_kunjungan()
    for kunjungan in kunjungan_list:
        choices.append(kunjungan['no_mr'])
        # Dictionary with options
        #choices = {'000'}
        # tkvar.set('000')  # set the default option
    nomor_mr['values'] = choices
    nomor_mr.current(0)


def submit():
    global files_to_upload
    if not files_to_upload:
        messagebox.showwarning(
            title="No Files", message="No files founds to upload")
        return False

    answer = askyesno(title='Submit Data',
                      message='Yakin submit semua data?')
    if not answer:
        return False

    res = files_to_upload
    res = [sub.replace('images', os.getcwd()+'/sounds')
           for sub in res]
    rekaman = [sub.replace('png', 'wav') for sub in res]
    # print(rekaman)
    if not rekaman:
        messagebox.showwarning(
            title="No Files", message="No files founds to upload")

    # print(rekaman)
    token = ''
    login = api_post(
        'admin/login', {'username': 'ahyo@admin.com', 'password': 'admin'})
    # print(login)
    if 'access_token' in login:
        token = login['access_token']

    file_list = []

    for f in rekaman:
        file_list.append(('rekaman', open(f, 'rb')))

    result = api_file('diagnosa/klasifikasi',
                      files=file_list, token=token)
    result = result['data']
    #result = upload['data'].split("---")
    # messagebox.showinfo(message=result[-1])
    lbl_result.config(text="Result: "+result)


def demo(events):
    filename = "health"
    generate_image(filename=filename)
    new_size = (img_width, img_height)
    file = 'images/'+filename+'.png'
    img = ImageTk.PhotoImage(Image.open(file).resize(new_size))
    img_al.configure(image=img)
    img_al.image = img
    img_al['height'] = img_height
    img_al['width'] = img_width
    if file not in files_to_upload:
        files_to_upload.append(file)
    lbl_result.config(text="Result: Healthy")


def pilih_nomor(events):
    global kunjungan_list
    nomor = nomor_mr.get()
    for k in kunjungan_list:
        if k['no_mr'] == nomor:
            lbl_nama.config(text=k['nama_kk'])
            lbl_alamat.config(text=k['alamat'])


MyButton(frame_result, text="Reset", x=0, y=0, width=10, command=reset)
MyButton(frame_result, text="Submit", x=270, y=0, width=10, command=submit)


img_al.bind("<Button-1>", image_al)
img_pl.bind("<Button-1>", image_pl)
img_ll.bind("<Button-1>", image_ll)

img_ar.bind("<Button-1>", image_ar)
img_pr.bind("<Button-1>", image_pr)
img_lr.bind("<Button-1>", image_lr)

img_tr.bind("<Button-1>", image_tr)

nomor_mr.bind("<<ComboboxSelected>>", pilih_nomor)

#app.bind("<F4>", app.destroy)
app.bind("<d>", demo)
app.bind("<f>", submit)


if __name__ == "__main__":
    app.mainloop()

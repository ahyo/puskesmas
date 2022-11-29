#!/usr/bin/env python3

from datetime import date
import json
import os
import time
import tkinter as tk
from tkinter.messagebox import askyesno
from PIL import ImageTk, Image

#from tkinter import ttk
#import tkinter.font as tkFont
from widgets import *
from recording import start_recording
from imaging import generate_image
from myApi import get_list_kunjungan, api_post, api_file

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

# statusbar = MyLabel(app, text="Copyright 2022, ahyo.haryanto@gmail.com",
#                     height=2, relief=tk.SUNKEN, anchor=tk.CENTER, x=0, y=685, width=145, size=12)

# column 1
#MyLabel(app,text="Daftar Kunjungan:",x=10,y=10,width=30)
#list_box = MyListbox(app,x=10,y=50,height=35,width=30)
global bg_white
new_size = (430, 235)
bg_white = ImageTk.PhotoImage(Image.open(
    'images/bg_white.jpg').resize(new_size))

# column 2
r1 = 0
r2 = 430
r3 = 860
c1 = 0
c2 = 235
c3 = 470
h = 6
w = 23

f1 = 980
l1 = 870

# column 3
MyLabel(app, text="No.MR:", x=l1, y=250, size=18)
lbl_mr = MyLabel(app, text="-", x=f1, y=250, size=18)
MyLabel(app, text="Name:", x=l1, y=280, size=18)
lbl_nama = MyLabel(app, text="Ah**", x=f1, y=280, size=18)
MyLabel(app, text="Address:", x=l1, y=310, size=18)
lbl_alamat = MyLabel(app, text="Bogor", x=f1, y=310, size=18)

# Create a Tkinter variable
tkvar = tk.StringVar(app)

# Dictionary with options
choices = {'001', '002', '003', '004', '005'}
tkvar.set('001')  # set the default option

popupMenu = tk.OptionMenu(app, tkvar, *choices)
popupMenu.place(x=f1, y=250)

img_al = MyLabel(app, text="Anterior Left", bg='#adafb3',
                 anchor='center', relief='raised',  x=r1, y=c1, width=w, height=h)
img_pl = MyLabel(app, text="Posterior Left", bg='#adafb3',
                 anchor='center', relief='raised', x=r1, y=c2, width=w, height=h)
img_ll = MyLabel(app, text="Lateral Left", bg='#adafb3',
                 anchor='center', relief='raised', x=r1, y=c3, width=w, height=h)

img_ar = MyLabel(app, text="Anterior Right", bg='#adafb3',
                 anchor='center', relief='raised',  x=r2, y=c1, width=w, height=h)
img_pr = MyLabel(app, text="Posterior Right", bg='#adafb3',
                 anchor='center', relief='raised', x=r2, y=c2, width=w, height=h)
img_lr = MyLabel(app, text="Lateral Right", bg='#adafb3',
                 anchor='center', relief='raised', x=r2, y=c3, width=w, height=h)

img_tr = MyLabel(app, text="Trachea", bg='#adafb3', anchor='center',
                 relief='raised',  x=r3, y=c1, width=w, height=h)

lbl_result = MyLabel(app, text="Result", x=l1, y=c3)


def image_al(event):
    # Heart, On check
    answer = askyesno(title='Rekam Anterior Kiri',
                      message='Letakan diafragma pada Anterior Kiri, kemudian klik Yes, dan tunggu selama 5 detik')
    if answer:
        filename = popupMenu['text']+'_al_' + \
            date.today().strftime('%Y%m%d')+'_O'
        start_recording(filename=filename)
        generate_image(filename=filename)
        new_size = (430, 235)
        img = ImageTk.PhotoImage(Image.open(
            'images/'+filename+'.png').resize(new_size))
        img_al.configure(image=img)
        img_al.image = img
        img_al['height'] = 235
        img_al['width'] = 430


def image_pl(event):
    # Heart, On check
    filename = popupMenu['text']+'_pl_'+date.today().strftime('%Y%m%d')+'_O'
    start_recording(filename=filename)
    generate_image(filename=filename)
    new_size = (430, 235)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_pl.configure(image=img)
    img_pl.image = img
    img_pl['height'] = 235
    img_pl['width'] = 430


def image_ll(event):
    # Heart, On check
    filename = popupMenu['text']+'_ll_'+date.today().strftime('%Y%m%d')+'_O'
    start_recording(filename=filename)
    generate_image(filename=filename)
    new_size = (430, 235)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_ll.configure(image=img)
    img_ll.image = img
    img_ll['height'] = 235
    img_ll['width'] = 430


def image_ar(event):
    # Heart, On check
    filename = popupMenu['text']+'_ar_'+date.today().strftime('%Y%m%d')+'_O'
    start_recording(filename=filename)
    generate_image(filename=filename)
    new_size = (430, 235)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_ar.configure(image=img)
    img_ar.image = img
    img_ar['height'] = 235
    img_ar['width'] = 430


def image_pr(event):
    # Heart, On check
    filename = popupMenu['text']+'_pr_'+date.today().strftime('%Y%m%d')+'_O'
    start_recording(filename=filename)
    generate_image(filename=filename)
    new_size = (430, 235)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_pr.configure(image=img)
    img_pr.image = img
    img_pr['height'] = 235
    img_pr['width'] = 430


def image_lr(event):
    # Heart, On check
    filename = popupMenu['text']+'_lr_'+date.today().strftime('%Y%m%d')+'_O'
    start_recording(filename=filename)
    generate_image(filename=filename)
    new_size = (430, 235)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_lr.configure(image=img)
    img_lr.image = img
    img_lr['height'] = 235
    img_lr['width'] = 430


def image_tr(event):
    # Heart, On check
    filename = popupMenu['text']+'_tr_'+date.today().strftime('%Y%m%d')+'_O'
    start_recording(filename=filename)
    generate_image(filename=filename)
    new_size = (430, 235)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_tr.configure(image=img)
    img_tr.image = img
    img_tr['height'] = 235
    img_tr['width'] = 430


def reset():
    img_al.config(text="Posterior XXX")
    img_al.config(image="")


def submit():
    if lbl_mr['text'] == '-':
        messagebox.showerror(title='Terjadi Kesalahan',
                             message='Harap memilih data kunjungan terlebih dahulu')
        quit()

    jname = os.getcwd()+'/sounds/' + \
        lbl_mr['text']+'H'+date.today().strftime('%Y%m%d')+'O.mp3'
    lname = os.getcwd()+'/sounds/' + \
        lbl_mr['text']+'L'+date.today().strftime('%Y%m%d')+'O.mp3'
    rekaman = {
        'suara_jantung': open(jname, 'rb'),
        'suara_paru': open(lname, 'rb')
    }
    print(rekaman)
    return False
    token = ''
    login = api_post(
        'admin/login', {'username': 'admin@email.com', 'password': 'admin'})
    if 'access_token' in login:
        token = login['access_token']
    upload = api_file('diagnosa/upload', files=rekaman, token=token)

# MyButton(app,text="Anterior Left",x=0,y=0,command=upload_jantung)
# MyButton(app,text="Posterior Left",x=0,y=240,command=upload_paru)
# MyButton(app,text="Lateral Left",x=0,y=480,command=upload_paru)


MyButton(app, text="Reset", x=950, y=380, width=10, command=reset)
MyButton(app, text="Submit", x=1100, y=380, width=10, command=submit)


img_al.bind("<Button-1>", image_al)
img_pl.bind("<Button-1>", image_pl)
img_ll.bind("<Button-1>", image_ll)

img_ar.bind("<Button-1>", image_ar)
img_pr.bind("<Button-1>", image_pr)
img_lr.bind("<Button-1>", image_lr)

img_tr.bind("<Button-1>", image_tr)

app.bind("<F4>", app.destroy)

if __name__ == "__main__":
    app.mainloop()

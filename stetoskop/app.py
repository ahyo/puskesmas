#!/usr/bin/env python3

from datetime import date
import json
import os
import time
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

#from tkinter import ttk
#import tkinter.font as tkFont
from widgets import *
from recording import start_recording
from imaging import generate_image
from myApi import get_list_kunjungan, api_post, api_file

app = tk.Tk()
app.title("Digital Stetoskop")
# setting window size
width = 1280
height = 720
screenwidth = app.winfo_screenwidth()
screenheight = app.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width) / 2, (screenheight - height) / 2)
app.geometry(alignstr)
app.resizable(width=False, height=False)

# statusbar

statusbar = MyLabel(app, text="Copyright 2022, ahyo.haryanto@gmail.com",
                    height=2, relief=tk.SUNKEN, anchor=tk.CENTER, x=0, y=685, width=145)

# column 1
MyLabel(app, text="Daftar Kunjungan:", x=10, y=10, width=30)
#list_box = MyListbox(app,x=10,y=50,height=35,width=30)
listbox_border = tk.Frame(app, bd=1, relief="ridge",
                          background="white", width=40, height=35)
listbox_border.pack(padx=10, pady=50, fill=tk.BOTH, expand=False, side=tk.LEFT)

listbox = tk.Listbox(listbox_border, width=30, height=10,
                     borderwidth=0, highlightthickness=0,
                     background=listbox_border.cget("background"),
                     )
vsb = tk.Scrollbar(listbox_border, orient="vertical", command=listbox.yview)
listbox.configure(yscrollcommand=vsb)
vsb.pack(side="right", fill="y")
listbox.pack(padx=10, pady=10, fill="both", expand=True)

list = get_list_kunjungan()
if not list:
    listbox.insert(tk.END, "- - Ada - Kunjungan")

for data in list:
    listbox.insert(tk.END, data['no_mr']+' - ' +
                   data['nama_kk']+' - '+data['alamat'])

# column 3
MyLabel(app, text="No.MR", x=950, y=15)
lbl_mr = MyLabel(app, text="-", x=1050, y=15)
MyLabel(app, text="Nama KK", x=950, y=45)
lbl_nama = MyLabel(app, text="-", x=1050, y=45)
MyLabel(app, text="Alamat", x=950, y=75)
lbl_alamat = MyLabel(app, text="-", x=1050, y=75)


def select_kunjungan(event):
    i = listbox.curselection()
    mystr = listbox.get(i)
    # print(mystr)
    item = mystr.split(' - ')
    lbl_mr['text'] = item[0]
    lbl_nama['text'] = item[1]
    lbl_alamat['text'] = item[2]


# column 2

lbl_jantung = MyLabel(app, text="...", x=580, y=15)
img_jantung = MyLabel(app, text="image jantung", bg='#adafb3',
                      anchor='center', relief='flat',  x=350, y=60, width=61, height=15)

lbl_paru = MyLabel(app, text="...", x=580, y=345)
img_paru = MyLabel(app, text="image paru", bg='#adafb3',
                   anchor='center', relief='flat', x=350, y=390, width=61, height=15)


def upload_jantung():
    # Heart, On check
    filename = lbl_mr['text']+'H'+date.today().strftime('%Y%m%d')+'O'
    lbl_jantung.configure(text="Recording 10 seconds, please wait...")
    start_recording(filename=filename)
    lbl_jantung['text'] = "Generating image..."
    generate_image(filename=filename)
    lbl_jantung['text'] = "Displaying image..."
    new_size = (550, 250)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_jantung.configure(image=img)
    img_jantung.image = img
    img_jantung['height'] = 250
    img_jantung['width'] = 550
    lbl_jantung['text'] = "Done"


def upload_paru():
    # Lungs, On check
    filename = lbl_mr['text']+'L'+date.today().strftime('%Y%m%d')+'O'
    lbl_paru['text'] = "Recording 10 seconds, please wait..."
    start_recording(filename=filename)
    lbl_paru['text'] = "Generating image..."
    generate_image(filename=filename)
    lbl_paru['text'] = "Displaying image..."
    new_size = (550, 250)
    img = ImageTk.PhotoImage(Image.open(
        'images/'+filename+'.png').resize(new_size))
    img_paru.configure(image=img)
    img_paru.image = img
    img_paru['height'] = 250
    img_paru['width'] = 550
    img_paru['text'] = "Done"


def reset():
    pass


def submit():
    # if lbl_mr['text'] == '-':
    #     messagebox.showerror(title='Terjadi Kesalahan',
    #                          message='Harap memilih data kunjungan terlebih dahulu')
    #     quit()

    jname = os.getcwd()+'/sounds/' + \
        lbl_mr['text']+'H'+date.today().strftime('%Y%m%d')+'O.wav'
    lname = os.getcwd()+'/sounds/' + \
        lbl_mr['text']+'L'+date.today().strftime('%Y%m%d')+'O.wav'
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
    if 'detail' in upload:
        statusbar['text'] = upload['detail']

    if 'description' in upload:
        statusbar['text'] = upload['description']


MyButton(app, text="Upload Rekaman Jantung",
         x=347, y=10, command=upload_jantung)
MyButton(app, text="Upload Rekaman Paru", x=347, y=340, command=upload_paru)

MyButton(app, text="Reset", x=950, y=340, width=10, command=reset)
MyButton(app, text="Submit", x=1100, y=340, width=10, command=submit)


def keypress(event):
    messagebox.showinfo(title='F1', message=event.char)


#list_box.bind('<<ListboxSelect>>', select_kunjungan)
listbox.bind('<<ListboxSelect>>', select_kunjungan)
app.bind("<KeyPress>", keypress)
# app.bind("<F2>", f_2)
# app.bind("<F3>", f_3)
# app.bind("<Return>", f_r)
app.bind("<F4>", app.destroy)

if __name__ == "__main__":
    app.mainloop()

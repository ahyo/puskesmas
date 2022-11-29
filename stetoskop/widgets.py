import tkinter as tk
#from tkinter import ttk
import tkinter.font as tkFont


class MyButton(tk.Button):
    def __init__(self, parent, x=0, y=0, width=20, height=1, bd=2, **kwargs):
        super().__init__(parent, kwargs, bg="#4287f5", bd=bd, relief="raised",
                         height=height, width=width, activebackground="#22d463", font=("Arial", 18))
        self.place(x=x, y=y)


class MyLabel(tk.Label):
    def __init__(self, parent, x=0, y=0, width=15, height=1, bd=0,  anchor='n', bg='white', size=24,  relief='flat', **kwargs):
        super().__init__(parent, kwargs, bg=bg, bd=bd, anchor=anchor, relief=relief,
                         height=height, width=width, font=("Arial", size), activebackground="blue")
        self.place(x=x, y=y)


class MyListbox(tk.Listbox):
    def __init__(self, parent, x=0, y=0, width=20, height=10, bg='#eee', **kwargs):
        super().__init__(parent, kwargs, bg=bg, bd=1, height=height, width=width)
        self.place(x=x, y=y)

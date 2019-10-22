#coding=utf-8
from __future__ import unicode_literals, print_function, division

from math import *
from Tkinter import *
import os


main = Tk()

main.iconbitmap('gas.ico')

main.title('Модель динамики газа в поршне')
main.geometry('700x570+300+200')
main.resizable(False, False)

menu = Label(main, text="Меню", font=("Arial Bold", 50))
menu.place(x = 270, y = 20)

def start_sim(evt):
    os.startfile(u'gas.py')
    simulation.configure(state = DISABLED)
    simulation.unbind('<1>')

simulation = Button(main, text="Симуляция", font=("Arial Bold", 20), width=30,height=2)
simulation.place(x = 115, y = 120)
simulation.bind('<1>', start_sim)


def start_theo(evt):
    exit()

theory = Button(main, text="Теория", font=("Arial Bold", 20), width=30,height=2)
theory.place(x = 115, y = 230)
theory.bind('<1>', start_theo)

def start_auth(evt):
    os.startfile(u'authors.py')

authors = Button(main, text="Авторы", font=("Arial Bold", 20), width=30,height=2)
authors.place(x = 115, y = 340)
authors.bind('<1>', start_auth)

def leave(evt):
    exit()

close = Button(main, text="ВЫХОД", font=("Arial Bold", 20), width=30,height=2)
close.place(x = 115, y = 450)
close.bind('<1>', leave)


main.mainloop()

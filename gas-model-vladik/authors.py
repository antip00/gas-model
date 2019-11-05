#coding=utf-8
from __future__ import unicode_literals, print_function, division

from math import *
from Tkinter import *
from PIL import Image, ImageTk

main = Tk()

main.iconbitmap('gas.ico')

main.title('Модель динамики газа в поршне')

main.geometry('700x570+300+200')
main.resizable(False, False)

label = Label(main, text="Авторы", font=("Arial Bold", 50))
label.place(x = 240, y = 20)

image_vlad = Image.open("Vladosik.jpg")
vlad = ImageTk.PhotoImage(image_vlad)
vladvlad = Label(image = vlad)
vladvlad.image = vlad
vladvlad.place(x = 0, y = 0)
print(dir(vladvlad.config()))
main.mainloop()

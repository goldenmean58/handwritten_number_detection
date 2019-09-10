#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : paint.py
# @Time     : Tue 10 Sep 2019 03:49:50 PM CST
# @Author   : Lishuxiang
# @E-mail   : lishuxiang@cug.edu.cn
# @Function :

import tkinter as tk
from PIL import Image, ImageDraw
from keras.preprocessing.image import img_to_array
from main import detect_img


class ImageGenerator:
    def __init__(self, parent, posx, posy, *kwargs):
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 200
        self.sizey = 200
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.drawing_area = tk.Canvas(self.parent,
                                      width=self.sizex,
                                      height=self.sizey)
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button = tk.Button(self.parent,
                                text="Done!",
                                width=10,
                                bg='black',
                                command=self.save)
        self.button.place(x=self.sizex / 7, y=self.sizey + 20)
        self.button1 = tk.Button(self.parent,
                                 text="Clear!",
                                 width=10,
                                 bg='black',
                                 command=self.clear)
        self.button1.place(x=(self.sizex / 7) + 80, y=self.sizey + 20)

        self.image = Image.new("RGB", (200, 200), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.result_label = tk.Label(
            master=self.parent, text='Please write a number in the canvas!')
        self.result_label.place(x=(self.sizex / 10), y=self.sizey + 70)

    def save(self):
        self.image = self.image.resize((28, 28), Image.ANTIALIAS)
        self.image = self.image.convert('L')
        arr = img_to_array(self.image)
        self.showinfo("The number is " + str(detect_img(arr)))

    def showinfo(self, message):
        self.result_label.config(text=message)

    def clear(self):
        self.drawing_area.delete("all")
        self.image = Image.new("RGB", (200, 200), (0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.result_label.config(text="Please write a number in the canvas!")

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"
        self.xold = None
        self.yold = None

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold,
                                         self.yold,
                                         event.x,
                                         event.y,
                                         smooth='true',
                                         width=12,
                                         fill='white')
                self.draw.line(((self.xold, self.yold), (event.x, event.y)),
                               (255, 255, 255),
                               width=12)

        self.xold = event.x
        self.yold = event.y


def main():
    root = tk.Tk()
    root.title('Hand Written Number Detection')
    root.wm_geometry("%dx%d+%d+%d" % (220, 300, 10, 10))
    root.config(bg='white')
    ImageGenerator(root, 10, 10)
    root.mainloop()


if __name__ == "__main__":
    main()

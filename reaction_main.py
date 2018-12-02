'''

Gerardo Pineda Vizcaino
github: graupv


MIT License

Copyright (c) 2018 graupv

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
import datetime
import os
import random
import threading
import time
from tkinter import *
from tkinter.ttk import *

import pandas as pd

fonta = 'Noto Sans', 10,
font = 'Noto Sans', 15,


class StopWatch(Frame):

    def __init__(self, master, scx, scy):
        self.scx = scx
        self.scy = scy
        self.start = float
        self.stop = float
        self.res = float
        self.u = float

        self.mf = Frame(master)
        self.mf.pack()

        self.time_label = Label(self.mf, text='Tiempo: ')
        self.time_label.grid(row=2, column=0, sticky=E)
        self.time = StringVar()
        self.time_val = Label(self.mf, textvariable=self.time, font=fonta)
        self.time_val.grid(row=2, column=2, sticky=W, columnspan=10)

        self.cd = StringVar()
        self.pressed_label = Label(self.mf, textvariable=self.cd, font=font)
        self.pressed_label.grid(row=5, column=2)

        self.check_but = Button(self.mf, text='Listo', command=self.cd_thread)
        self.check_but.grid(row=3, column=0)

        self.reset = Button(self.mf, text='Reset', command=self.reset_time)
        self.reset.grid(row=3, column=3, sticky=W + E, padx=5, pady=5)

        self.run = False
        self.spring = True

        self.surpirse = Label(self.mf, text='YA', font=('Noto Sans', 16, "bold"))
        #   label that will show up on random time interval

        self.hit_but = Button(self.mf, text='YA', command=self.stopwatch)
        self.hit_but.grid(row=7, column=2, padx=5, pady=5)

        #   data entry
        self.df = pd.DataFrame()
        self.name_label = Label(self.mf, text='Datos personales')
        self.name_label.grid(row=10, column=0, sticky=W)
        self.name_var = StringVar()
        self.name_label = Label(self.mf, text='Nombre')
        self.name_label.grid(row=11, column=0, sticky=W)
        self.name_ent = Entry(self.mf, textvariable=self.name_var, width=14)
        self.name_ent.grid(row=11, column=2, columnspan=4, sticky=W)

        self.coffee = IntVar()
        self.coffee_label = Label(self.mf, text='Cafe')
        self.coffee_label.grid(row=12, column=0, sticky=W)
        self.coffee_ent = Checkbutton(self.mf, text='Si / No', variable=self.coffee, onvalue=1, offvalue=0)
        self.coffee_ent.grid(row=12, column=2, columnspan=4, sticky=W)

        self.sex_label = Label(self.mf, text='Sexo')
        self.sex_label.grid(row=13, column=0, sticky=W)
        self.m_var = IntVar()
        self.m_cb = Radiobutton(self.mf, text='M', variable=self.m_var, value=1, command=self.sex_m)
        self.m_cb.grid(row=13, column=1, columnspan=2)
        self.h_var = IntVar()
        self.h_var.set(0)
        self.h_cb = Radiobutton(self.mf, text='H', variable=self.h_var, value=1, command=self.sex_h)
        self.h_cb.grid(row=13, column=2, columnspan=2)

        self.edad_var = IntVar()
        self.edad_label = Label(self.mf, text='Edad')
        self.edad_label.grid(row=14, column=0, sticky=W)
        self.edad_ent = Entry(self.mf, textvariable=self.edad_var, width=5)
        self.edad_ent.grid(row=14, column=2, columnspan=4, sticky=W)

    def sex_m(self):
        self.h_var.set(0)
        self.m_var.set(1)

    def sex_h(self):
        self.h_var.set(1)
        self.m_var.set(0)

    def load_df(self):
        try:
            if os.path.exists('resultados.xlsx'):
                self.df = pd.read_excel('resultados.xlsx')
            else:
                pass
        except Exception as e:
            print(e)

    def cd_thread(self):
        self.run = True
        thread = threading.Thread(target=self.countdown)
        thread.start()

    def countdown(self):
        # self.reset_time()
        x = 3
        self.hit_but.config(state='normal')
        while x >= 0 and self.run:
            self.cd.set(x)
            time.sleep(1)
            x -= 1

        self.u = random.uniform(0.5, 2.75) + random.uniform(0.15, 0.35)
        print(self.u)
        time.sleep(self.u)
        self.pop_up()
        self.startwatch()

    def pop_up(self):
        self.surpirse.grid(row=5, column=2)
        self.startwatch()

    def reset_time(self):
        self.run = False
        self.surpirse.grid_forget()
        self.hit_but.config(state='normal')
        self.cd.set(3)
        self.time.set(datetime.timedelta(seconds=0))

    def startwatch(self):
        self.start = time.time()

    def save_data(self):
        #   save to df and to file
        lsd = []
        if self.m_var.get() == 1:
            s = 'Mujer'
        else:
            s = 'Hombre'

        if self.coffee.get() == 1:
            c = 'Si'

        else:
            c = 'No'

        data = {'nombre': self.name_var.get(), 'edad': self.edad_var.get(), 'sexo': s, "Cafe": c, 'Dif 1': self.res}
        lsd.append(data)
        df = pd.DataFrame(lsd)
        f = [self.df, df]
        res = pd.concat(f, ignore_index=True, sort=False)
        res.to_excel('resultados.xlsx')
        self.load_df()

    def stopwatch(self):
        self.stop = time.time()
        try:
            self.hit_but.config(state='disabled')
            self.res = self.stop - self.start
            self.time.set(self.res)
            self.save_data()
        except Exception as e:
            #   apacho antes
            print(e)
            t = time.time() + self.u
            self.res = t - self.stop
            self.time.set(self.res)
            self.save_data()


if __name__ == '__main__':
    root = Tk()
    root.title('Test de Reacción')
    root.minsize(275, 300)
    root.maxsize(275, 300)

    app = StopWatch(root, root.winfo_screenwidth(), root.winfo_screenheight())
    app.reset_time()
    app.load_df()

    mainloop()

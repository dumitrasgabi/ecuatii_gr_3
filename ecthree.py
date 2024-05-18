import numpy as np
from tkinter import *
import tkinter.messagebox
from cmath import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Class:
    def __init__(self, rot):
        # =============Functii==========================

        def focus_next_entry(event):
            event.widget.tk_focusNext().focus()
            return "break"

        def focus_previous_entry(event):
            event.widget.tk_focusPrev().focus()
            return "break"

        def on_enter_pressed(event):
            Calculeaza()

        def on_escape_pressed(event):
            Iesire()

        def on_r_pressed(event):
            Reset()

        def Reset():
            A.set("")
            B.set("")
            C.set("")
            D.set("")
            Sol1.set("")
            Sol2.set("")
            Sol3.set("")
            Delta.set("")
            ax.clear()
            ax.plot(0, 0)
            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.spines['top'].set_color('none')
            ax.spines['right'].set_color('none')
            canvas.draw()
            return

        def Iesire():
            q = tkinter.messagebox.askyesno("Validate Entry Widget", "Sunteti sigur ca doriti sa parasiti aplicatia?")
            if q > 0:
                rot.destroy()
                return

        def ComplexToString(z):
            x = round(z.real, 3)
            y = round(z.imag, 3)
            if y == 0:
                return f"{x:g}"
            if x == 0:
                return f"{y:g}j"
            return f"{x:g}{y:+g}j"

        def RezolvareEcuatie(a, b, c, d):
            def Radix3(omega):
                rho, theta = polar(omega)
                return [rect(pow(rho, 1 / 3), (theta + 2 * kk * pi) / 3) for kk in range(3)]

            assert a != 0
            p = c / a - b * b / (3.0 * a * a)
            q = 2.0 * b ** 3 / (27.0 * a ** 3) - b * c / (3.0 * a * a) + d / a
            delta = q * q + 4.0 * p ** 3 / 27.0
            w = (-q + sqrt(delta)) / 2
            roots = []
            for u in Radix3(w):
                z = u - p / (3 * u)
                z -= b / (3.0 * a)
                roots.append(z)
            roots = sorted(roots, key=lambda x: (x.real, x.imag))
            newRoots = [ComplexToString(Rut) for Rut in roots]
            newDelta = ComplexToString(delta)
            return newRoots, newDelta

        def Calculeaza():
            a = A.get()
            b = B.get()
            c = C.get()
            d = D.get()
            try:
                a = complex(a)
                if a == 0:
                    tkinter.messagebox.showwarning("Eroare", "Valoarea lui a trebuie sa fie nenula!")
                    A.set("")
                    return
                b = complex(b)
                c = complex(c)
                d = complex(d)
                roots, delta = RezolvareEcuatie(a, b, c, d)
                sol1, sol2, sol3 = roots
                Sol1.set(sol1)
                Sol2.set(sol2)
                Sol3.set(sol3)
                Delta.set(str(delta))
                Deseneaza_Grafic(a, b, c, d)
                return True

            except ValueError:
                tkinter.messagebox.showwarning("Eroare", "Valorile introduse nu sunt corecte!")
                A.set("")
                B.set("")
                C.set("")
                D.set("")
                Sol1.set("")
                Sol2.set("")
                Sol3.set("")
                return False

        def Deseneaza_Grafic(a, b, c, d):
            ax.clear()
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            x = np.linspace(-10, 10, 700)
            y = a * x ** 3 + b * x ** 2 + c * x + d
            y = np.real(y)
            ax.plot(x, y)
            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.spines['top'].set_color('none')
            ax.spines['right'].set_color('none')
            canvas.draw()

        # ================Frame-uri=======================
        self.root = rot
        self.root.title("Ecuatii de Gradul III")
        self.root.geometry("1175x735+0+0")
        self.root.configure(bg="#d9c0de")
        frmPrincipal = Frame(self.root, bd=10, width=800)
        frmPrincipal.grid()
        frmTitlu = Frame(frmPrincipal, bd=10, width=800, relief=RIDGE)
        frmTitlu.pack(side=TOP)
        frmGrafic = Frame(frmPrincipal, bd=10, width=800, relief=RIDGE)
        frmGrafic.pack(side=RIGHT)
        # ================Variabile=======================
        A = StringVar()
        B = StringVar()
        C = StringVar()
        D = StringVar()
        Sol1 = StringVar()
        Sol2 = StringVar()
        Sol3 = StringVar()
        Delta = StringVar()
        # ================Widgeturi=======================
        lblInfo = Label(frmTitlu, font=('Helvetica', 25, 'bold'), text="Ecuatii de Gradul III", justify=LEFT, bg="#d9c0de")
        lblInfo.grid(padx=0, sticky="w")
        lblDate = LabelFrame(frmPrincipal, bd=10, width=800, height=200, font=('Helvetica', 12, 'bold'), text='Date', relief=RIDGE)
        lblDate.pack(side=TOP)
        lblSolutii = LabelFrame(frmPrincipal, bd=10, width=800, height=200, font=('Helvetica', 12, 'bold'), text='Solutii', relief=RIDGE)
        lblSolutii.place(x=20, y=300)
        lblOptiuni = LabelFrame(frmPrincipal, bd=10, width=800, height=80, font=('Helvetica', 12, 'bold'), text='Optiuni', relief=RIDGE)
        lblOptiuni.pack(side=BOTTOM)
        lblGrafic = LabelFrame(frmGrafic, bd=10, width=900, height=600, font=('Helvetica', 12, 'bold'), text='Grafic', relief=RIDGE)
        lblGrafic.pack(side=RIGHT, anchor=NE)
        cnvPanza = Canvas(lblGrafic, width=660, height=560)
        cnvPanza.pack()
        fig = Figure(figsize=(6.6, 5.6), dpi=100)
        ax = fig.add_subplot(111)
        canvas = FigureCanvasTkAgg(fig, master=cnvPanza)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        ax.plot(0, 0)
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=BOTTOM, fill=X)

        lblA = Label(lblDate, font=('Helvetica', 16, 'bold'), text="a=", bd=7)
        lblA.grid(row=0, column=0, sticky=W)
        txtA = Entry(lblDate, font=('Helvetica', 13, 'bold'), bd=7, textvariable=A, width=34)
        txtA.grid(row=0, column=1)

        lblB = Label(lblDate, font=('Helvetica', 16, 'bold'), text="b=", bd=7)
        lblB.grid(row=1, column=0, sticky=W)
        txtB = Entry(lblDate, font=('Helvetica', 13, 'bold'), bd=7, textvariable=B, width=34)
        txtB.grid(row=1, column=1)

        lblC = Label(lblDate, font=('Helvetica', 16, 'bold'), text="c=", bd=7)
        lblC.grid(row=2, column=0, sticky=W)
        txtC = Entry(lblDate, font=('Helvetica', 13, 'bold'), bd=7, textvariable=C, width=34)
        txtC.grid(row=2, column=1)

        lblD = Label(lblDate, font=('Helvetica', 16, 'bold'), text="d=", bd=7)
        lblD.grid(row=3, column=0, sticky=W)
        txtD = Entry(lblDate, font=('Helvetica', 13, 'bold'), bd=7, textvariable=D, width=34)
        txtD.grid(row=3, column=1)

        txtA.bind("<Down>", focus_next_entry)
        txtB.bind("<Down>", focus_next_entry)
        txtC.bind("<Down>", focus_next_entry)
        txtB.bind("<Up>", focus_previous_entry)
        txtC.bind("<Up>", focus_previous_entry)
        txtD.bind("<Up>", focus_previous_entry)

        lblDelta = Label(lblSolutii, font=('Helvetica', 16, 'bold'), text="Δ=", bd=7)
        lblDelta.grid(row=4, column=0, sticky=W)
        txtDelta = Entry(lblSolutii, font=('Helvetica', 13, 'bold'), bd=7, textvariable=Delta, width=34, state=DISABLED)
        txtDelta.grid(row=4, column=1, padx=8, pady=8)

        lblX1 = Label(lblSolutii, font=('Helvetica', 16, 'bold'), text="x1=", bd=7)
        lblX1.grid(row=5, column=0, sticky=W)
        txtX1 = Entry(lblSolutii, font=('Helvetica', 13, 'bold'), bd=7, textvariable=Sol1, width=34, state=DISABLED)
        txtX1.grid(row=5, column=1, padx=8, pady=8)

        lblX2 = Label(lblSolutii, font=('Helvetica', 16, 'bold'), text="x2=", bd=7)
        lblX2.grid(row=6, column=0, sticky=W)
        txtX2 = Entry(lblSolutii, font=('Helvetica', 13, 'bold'), bd=7, textvariable=Sol2, width=34, state=DISABLED)
        txtX2.grid(row=6, column=1, padx=8, pady=8)

        lblX3 = Label(lblSolutii, font=('Helvetica', 16, 'bold'), text="x3=", bd=7)
        lblX3.grid(row=7, column=0, sticky=W)
        txtX3 = Entry(lblSolutii, font=('Helvetica', 13, 'bold'), bd=7, textvariable=Sol3, width=34, state=DISABLED)
        txtX3.grid(row=7, column=1, padx=8, pady=8)

        btnCalc = Button(lblOptiuni, padx=18, bd=7, font=('Helvetica', 16, 'bold'), width=7, command=Calculeaza, text="Rezolva", bg="#414ce8")
        btnCalc.grid(row=2, column=0, pady=12)
        root.bind('<Return>', on_enter_pressed)

        btnReset = Button(lblOptiuni, padx=18, bd=7, font=('Helvetica', 16, 'bold'), width=7, command=Reset, text="Reset (R)", bg="#e8d241")
        btnReset.grid(row=2, column=1, pady=12)
        root.bind('<KeyPress-r>', on_r_pressed)

        btnQuit = Button(lblOptiuni, padx=18, bd=7, font=('Helvetica', 16, 'bold'), width=7, command=Iesire, text="Iesire", bg="#ed5f61")
        btnQuit.grid(row=2, column=3, pady=12)
        root.bind('<Escape>', on_escape_pressed)


if __name__ == '__main__':
    root = Tk()
    root.iconbitmap("ec3.ico")
    application = Class(root)
    root.resizable(False, False)
    root.mainloop()

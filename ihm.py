# On importe Tkinter
from tkinter import *
import tkinter as tk

#def du bouton stats
def boutonFourreTout():
    newWindow = tk.Toplevel(fenetre)
    newWindow.title('Statistiques')
    newWindow.maxsize(400, 500)
    newWindow.minsize(400, 500)
    labelNew = tk.Label(newWindow, text="Statistiques")

    labelNew.pack()


# On crée une fenêtre, racine de notre interface
fenetre = tk.Tk()
fenetre.title('Simulation')
fenetre.maxsize(1300, 700)
fenetre.minsize(1300, 700)
fenetre['bg']='white'

Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, fill=Y, ipadx=30)

s_borne = Spinbox(Frame1, from_=0, to=10)
s_pers = Spinbox(Frame1, from_=0, to=500)


Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame2.pack(side=BOTTOM, fill=X, ipady=50)

Frame3 = Frame(fenetre, borderwidth=2,bg='white')
Frame3.pack(fill=X, ipady=250)

stats = Button(Frame1, text="Statistiques", fg="white", bg="green", command = boutonFourreTout)

Label(Frame1, text="Paramètres Modifiables", font=("Helvetica", 16)).pack()
Label(Frame1, text="").pack()
Label(Frame1, text="Nombre de bornes (de 1 à 10):").pack()
s_borne.pack()
Label(Frame1, text="").pack()
Label(Frame1, text="Nombre de personnes (de 1 à 500):").pack()
s_pers.pack()
Label(Frame1, text="").pack()
Label(Frame1, text="").pack()
stats.pack()
Label(Frame2, text="Logs en direct").pack(side=TOP, padx=80, pady=20)
Label(Frame3, text="Simulation").pack(side=TOP, padx=80, pady=20)

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
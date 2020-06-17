# On importe Tkinter
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

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
fenetre.maxsize(1700, 700)
fenetre.minsize(1700, 700)
fenetre['bg']='white'

Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, fill=Y, ipadx=30)

s_borne = Spinbox(Frame1, from_=0, to=10)
s_pers = Spinbox(Frame1, from_=0, to=500)


Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame2.pack(side=BOTTOM, fill=X, ipady=0)


Frame3 = Frame(fenetre, borderwidth=2,bg='white')
Frame3.pack(fill=X, ipady=250)

text = Text(Frame2)

stats = Button(Frame1, text="Statistiques", fg="white", bg="green", command = boutonFourreTout)

logs="blablablablablabla"+"\n"+"blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n""blablablablablabla"+"\n"
logs = logs + "test" + "\n"
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

canvasLog = Canvas(Frame2, bg="Black", width=800, height=150)
canvasLog.pack()
scrollbar = Scrollbar(canvasLog, orient=VERTICAL, command=canvasLog.yview)
scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
canvasLog.create_text(100,10,fill="white",font="Times 15",
                        text=logs)
scrollbar.config(command=canvasLog.yview)
canvasLog.config(yscrollcommand=scrollbar.set)

Label(Frame3, text="Simulation").pack(side=TOP, padx=80, pady=20)


canvasSim = Canvas(Frame3, bg="Black")

img1 = ImageTk.PhotoImage(file="Prediction_nbCLient_for_Monday.png")


#canvasUser = tk.Canvas(canvasSim, width=10, height=10)
#canvasUser.create_image(0, 0, anchor=tk.NW, image=img1)
#canvasUser.pack()

scrollbar2 = Scrollbar(Frame3, orient=VERTICAL, command=canvasSim.yview)
scrollbar2.pack(side=RIGHT,fill=Y)
scrollbar2.config(command=canvasSim.yview)

scrollbar3 = Scrollbar(Frame3, orient=HORIZONTAL, command=canvasSim.yview)
scrollbar3.pack(side=BOTTOM,fill=X)
scrollbar3.config(command=canvasSim.xview)

canvasSim.config(width=100,height=100)
canvasSim.config(yscrollcommand=scrollbar2.set)
canvasSim.config(xscrollcommand=scrollbar3.set)
canvasSim.pack(side=LEFT,expand=True,fill=BOTH)

canvasSim.create_image(100,100,image=img1)

#labelImg1 = tk.Label(canvasSim, image=img1)
#labelImg1.pack()
#labelImg2 = tk.Label(canvasSim, image=img2)
#labelImg2.pack()
#labelImg3 = tk.Label(canvasSim, image=img3)
#labelImg3.pack()

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()
# On import Tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from resizeimage import resizeimage
import csv

# def du bouton stats
def boutonFourreTout():
    newWindow = tk.Toplevel(fenetre)
    newWindow.title('Détails des jours')
    newWindow.maxsize(400, 610)
    newWindow.minsize(400, 610)

    n = ttk.Notebook(newWindow)  # Création du système d'onglets
    n.pack()
    o1 = ttk.Frame(n, width=400, height=500)  # Ajout de l'onglet 1
    o1.pack()
    o2 = ttk.Frame(n, width=400, height=500)  # Ajout de l'onglet 2
    o2.pack()
    o3 = ttk.Frame(n, width=400, height=500)  # Ajout de l'onglet 3
    o3.pack()
    n.add(o1, text='Jour 1')  # Nom de l'onglet 1
    n.add(o2, text='Jour 2')  # Nom de l'onglet 2
    n.add(o3, text='Jour 3')  # Nom de l'onglet 3

    liste = ["0      |", "1      |", "2      |", "3      |", "4      |", "5      |", "6      |", "7      |", "8      |",
             "9      |", "10    |", "11    |", "12    |", "13    |", "14    |", "15    |", "16    |", "17    |", "18    |",
             "19    |",
             "20    |", "21    |", "22    |", "23    |", "24    |"]

    lab1c1 = Label(o1, text="C1    |")
    lab1c2 = Label(o1, text="C2")

    lab2c1 = Label(o2, text="C1    |")
    lab2c2 = Label(o2, text="C2")

    lab3c1 = Label(o3, text="C1    |")
    lab3c2 = Label(o3, text="C2")


    x=2
    for h in liste:
        l1 = Label(o1,text=h)
        l2 = Label(o2,text=h)
        l3 = Label(o3,text=h)
        l1.grid(row=x,column=0, sticky=W, pady=0)
        l2.grid(row=x, column=0, sticky=W, pady=0)
        l3.grid(row=x, column=0, sticky=W, pady=0)
        x+=1

    lab1c1.grid(row=0, column=0, sticky=W, pady=0)
    lab1c2.grid(row=0, column=1, sticky=W, pady=0,padx=10)

    lab2c1.grid(row=0, column=0, sticky=W, pady=0)
    lab2c2.grid(row=0, column=1, sticky=W, pady=0, padx=10)

    lab3c1.grid(row=0, column=0, sticky=W, pady=0)
    lab3c2.grid(row=0, column=1, sticky=W, pady=0, padx=10)

    l = Label(o1, text="-------")
    l.grid(row=1, column=0, sticky=W, pady=0)
    l = Label(o1, text="-------")
    l.grid(row=1, column=1, sticky=W, pady=0)

    l = Label(o2, text="-------")
    l.grid(row=1, column=0, sticky=W, pady=0)
    l = Label(o2, text="-------")
    l.grid(row=1, column=1, sticky=W, pady=0)

    l = Label(o3, text="-------")
    l.grid(row=1, column=0, sticky=W, pady=0)
    l = Label(o3, text="-------")
    l.grid(row=1, column=1, sticky=W, pady=0)

    with open('log_lundi.csv') as f:
        f_csv = csv.reader(f)
        x=2
        for ligne in f_csv:
            if x==27:
                break
            l = Label(o1, text=ligne[1])
            l.grid(row=x, column=1, sticky=W, pady=0)
            x=x+1

    with open('log_mardi.csv') as f:
        f_csv = csv.reader(f)
        x=2
        for ligne in f_csv:
            if x==27:
                break
            l = Label(o2, text=ligne[1])
            l.grid(row=x, column=1, sticky=W, pady=0)
            x=x+1

    with open('log_mercredi.csv') as f:
        f_csv = csv.reader(f)
        x=2
        for ligne in f_csv:
            if x==27:
                break
            l = Label(o3, text=ligne[1])
            l.grid(row=x, column=1, sticky=W, pady=0)
            x=x+1


# On crée une fenêtre, racine de notre interface
fenetre = tk.Tk()
fenetre.title('Simulation')
fenetre.maxsize(1300, 700)
fenetre.minsize(1300, 700)
fenetre['bg'] = 'white'

Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, fill=Y, ipadx=10)

s_borne = Spinbox(Frame1, from_=0, to=10)
s_pers = Spinbox(Frame1, from_=0, to=500)

Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
Frame2.pack(side=BOTTOM, fill=X, ipady=0)

Frame3 = Frame(fenetre, borderwidth=2, bg='white')
Frame3.pack(fill=X, ipady=250)

text = Text(Frame2)

stats = Button(Frame1, text="Détails des jours", fg="white", bg="green", command=boutonFourreTout)

logs = "[5, 6, 5, 5, 4, 5, 5, 10, 23, 32, 34, 11, 15, 11, 34, 42, 38, 38, 26, 8, 5, 4, 3, 5, 4, 5, 6, 5, 5, 5, 5, " +"\n"+ "23, 28, 46, 41, 43, 17, 23, 33, 28, 31, 26, 21, 8, 5, 4, 5, 5, 4, 5, 5, 6, 5, 5, 5, 17, 34, 36, 38, 24, 39, 43, " +"\n"+ "34, 43, 45, 33, 21, 7, 5, 4, 5, 6, 2, 4, 5, 7, 5, 5, 5, 12, 41, 36, 42, 23, 12, 14, 26, 43, 35, 32, 27, 15, 5," +"\n"+ " 4, 5, 5]" +"\n"+ "[2.31, 0.84, 2.64, 2.12, 1.43, 1.35, 16.67, 98.37, 76.24, 103.69, 73.68, 85.34, 42.69, 64.21, 48.57, 56.34, "+"\n"+ "49.99, 21.54, 16.55, 4.69, 2.12, 1.45, 2.44, 2.31, 0.84, 2.12, 0.65, 0.57, 1.39, 1.64, 21.96, 96.31, 87.12, 98.55," +"\n"+ " 46.12, 136.49, 126.97, 124.65, 48.76, 56.93, 98.32, 45.21, 28.97, 2.16, 2.97, 0.54, 1.33, 4.95, 1.46, 0.19," +"\n"+ " 0.97, 0.64, 1.97, 2.64, 31.23, 76.48, 45.96, 67.45, 47.65, 101.02, 81.13, 46.73, 75.68, 102.21, 89.67, 65.48," +"\n"+ " 31.46, 3.46, 12.32, 16.46, 1.09, 1.01, 1.97, 0.68, 0.41, 0.69, 2.54, 9.42, 29.64, 84.63, 124.97, 94.65, 97.23, 75.65, " +"\n"+ "71.98, 46.68, 67.94, 35.48, 67.98, 59.46, 35.67, 10.95, 4.38, 0.68, 1.97, 2.64] " +"\n\n"+ "ARIMA(0, 0, 0)x(0, 0, 0, 24)24 - AIC:1032.8926431858006" +"\n"+ "Total time in seconds for first call: 0.019819021224975586" +"\n"+ "ARIMA(0, 0, 0)x(0, 0, 1, 24)24 - AIC:3009.8729702994" +"\n"+ "Total time in seconds for first call: 0.42527270317077637" +"\n"+ "ARIMA(0, 0, 0)x(0, 0, 2, 24)24 - AIC:484.1869674453041" +"\n"+ "Total time in seconds for first call: 0.8452131748199463" +"\n"+"ARIMA(0, 0, 0)x(0, 0, 3, 24)24 - AIC:257.78587991704126" +"\n"+"Total time in seconds for first call: 6.663841485977173"

Label(Frame1, text="Paramètres Modifiables", font=("Helvetica", 14)).pack()
Label(Frame1, text="").pack()
Label(Frame1, text="Nombre d'utilisateurs par borne :").pack()
s_borne.pack()
Label(Frame1, text="").pack()
Label(Frame1, text="Bande passante:").pack()
s_pers.pack()
Label(Frame1, text="").pack()
Label(Frame1, text="").pack()
stats.pack()
#Label(Frame2, text="Logs en direct").pack(side=TOP, padx=80, pady=20)

canvasLog = Canvas(Frame2, bg="Black", width=1000, height=200)
canvasLog.pack()
scrollbar = Scrollbar(canvasLog, orient=VERTICAL, command=canvasLog.yview)
scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
canvasLog.create_text(500, 0, fill="white", font="Times 12",
                      text=logs)
scrollbar.config(command=canvasLog.yview)
canvasLog.config(yscrollcommand=scrollbar.set)

#scrollbarH = Scrollbar(canvasLog, orient=HORIZONTAL, command=canvasLog.yview)
#scrollbarH.pack(side=BOTTOM, fill=X)
#scrollbarH.config(command=canvasLog.xview)
#canvasLog.config(xscrollcommand=scrollbarH.set)

Label(Frame3, text="Simulation").pack(side=TOP, padx=80, pady=20)

canvasSim = Canvas(Frame3, bg="White")

img1 = Image.open('borneNB_forecasting.PNG')
img1 = resizeimage.resize_thumbnail(img1, [800, 700])
img1.save('borneNB_forecasting.PNG', img1.format)

img2 = Image.open('forecasting_bandwidth.PNG')
img2 = resizeimage.resize_thumbnail(img2, [800, 700])
img2.save('forecasting_bandwidth.PNG', img2.format)

img3 = Image.open('forecasting_client.PNG')
img3 = resizeimage.resize_thumbnail(img3, [800, 700])
img3.save('forecasting_client.PNG', img3.format)

img4 = Image.open('fleche.jpeg')
img4 = resizeimage.resize_thumbnail(img4, [300, 200])
img4.save('fleche.jpeg', img4.format)

img5 = Image.open('Prediction_Bandwidth_Mo.s_for_Tuesday.png')
img5 = resizeimage.resize_thumbnail(img5, [800, 700])
img5.save('Prediction_Bandwidth_Mo.s_for_Tuesday.png', img5.format)

img6 = Image.open('Prediction_nbCLient_for_Tuesday.png')
img6 = resizeimage.resize_thumbnail(img6, [800, 700])
img6.save('Prediction_nbCLient_for_Tuesday.png', img6.format)

img7 = Image.open('Prediction_Result_for_Tuesday.png')
img7 = resizeimage.resize_thumbnail(img7, [800, 700])
img7.save('Prediction_Result_for_Tuesday.png', img3.format)

img8 = Image.open('Prediction_Bandwidth_Mo.s_for_Wednesday.png')
img8 = resizeimage.resize_thumbnail(img8, [800, 700])
img8.save('Prediction_nbCLient_for_Wednesday.png', img8.format)

img9 = Image.open('Prediction_nbCLient_for_Wednesday.png')
img9 = resizeimage.resize_thumbnail(img9, [800, 700])
img9.save('Prediction_nbCLient_for_Wednesday.png', img9.format)

img10 = Image.open('Prediction_Result_for_Wednesday.png')
img10 = resizeimage.resize_thumbnail(img10, [800, 700])
img10.save('Prediction_Result_for_Wednesday.png', img10.format)

#img11 = Image.open('stats7.png')
#img11 = resizeimage.resize_thumbnail(img11, [800, 700])
#img11.save('stats7.PNG', img11.format)

img1 = ImageTk.PhotoImage(file="borneNB_forecasting.PNG")
img2 = ImageTk.PhotoImage(file="forecasting_bandwidth.PNG")
img3 = ImageTk.PhotoImage(file="forecasting_client.PNG")
img4 = ImageTk.PhotoImage(file="fleche.jpeg")
img5 = ImageTk.PhotoImage(file="Prediction_Bandwidth_Mo.s_for_Tuesday.png")
img6 = ImageTk.PhotoImage(file="Prediction_nbCLient_for_Tuesday.png")
img7 = ImageTk.PhotoImage(file="Prediction_Result_for_Tuesday.png")
img8 = ImageTk.PhotoImage(file="Prediction_Bandwidth_Mo.s_for_Wednesday.png")
img9 = ImageTk.PhotoImage(file="Prediction_nbCLient_for_Wednesday.png")
img10 = ImageTk.PhotoImage(file="Prediction_Result_for_Wednesday.png")
#img11 = ImageTk.PhotoImage(file="stats7.png")

scrollbar2 = Scrollbar(Frame3, orient=VERTICAL, command=canvasSim.yview)
scrollbar2.pack(side=RIGHT, fill=Y)
scrollbar2.config(command=canvasSim.yview)

scrollbar3 = Scrollbar(Frame3, orient=HORIZONTAL, command=canvasSim.yview)
scrollbar3.pack(side=BOTTOM, fill=X)
scrollbar3.config(command=canvasSim.xview)

canvasSim.config(width=100, height=100)
canvasSim.config(yscrollcommand=scrollbar2.set)
canvasSim.config(xscrollcommand=scrollbar3.set)
canvasSim.pack(side=LEFT, expand=True, fill=BOTH)

x = 200
y = 200
#img11
liste = [img3,img2,img4,img1,img5,img6,img4,img7,img8,img9,img4,img10]

for img in liste:
    canvasSim.create_image(x, y, image=img)

    if img == img1 or img == img7 :
        x = -700
        y += 400

    if img == img10 :
        x=200
        y += 400

    if img == img2 or img == img4 or img == img6 or img == img9 or img == img10 :
        x += 500
    else: x += 900

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre
fenetre.mainloop()

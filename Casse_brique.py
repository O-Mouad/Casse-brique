""" 
Mouad Ouamane 
TP4 du 09/10/2025
Ce fichier contient les tests pour comprendre tkinter
"""


from tkinter import Tk, Label, Button, StringVar, Entry 
from tkinter import messagebox 

mw = Tk()

mw.title("Casse brique")

message = Label(mw, text = "Bienvenue dans une phase de test" , relief = 'groove')
message.pack()

bouttonQuitter = Button ( mw , text = "Fermer" , relief = 'raised' , fg = 'red' , command = mw.destroy)
bouttonQuitter.pack()

mw.mainloop()


def verif(): 
    if mdp.get() == 
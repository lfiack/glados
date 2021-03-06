#!/usr/bin/python
# coding: utf-8
"""Premier exemple avec Tkinter.


On crée une fenêtre simple qui souhaite la bienvenue à l'utilisateur.


"""


# On importe Tkinter

try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here


# On crée une fenêtre, racine de notre interface

fenetre = Tk()


# On crée un label (ligne de texte) souhaitant la bienvenue

# Note : le premier paramètre passé au constructeur de Label est notre

# interface racine

champ_label = Label(fenetre, text="Salut les Zér0s !")


# On affiche le label dans la fenêtre

champ_label.pack()

bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.pack()

var_texte = StringVar()
ligne_texte = Entry(fenetre, textvariable=var_texte, width=30)
ligne_texte.pack()

#var_texte2 = StringVar()
#ligne_texte2 = Text(fenetre, textvariable=var_texte2, width=30)
#ligne_texte2.pack()

var_case = IntVar()
case = Checkbutton(fenetre, text="Ne plus poser cette question", variable=var_case)
case.pack()

var_choix = StringVar()
choix_rouge = Radiobutton(fenetre, text="Rouge", variable=var_choix, value="rouge")
choix_vert = Radiobutton(fenetre, text="Vert", variable=var_choix, value="vert")
choix_bleu = Radiobutton(fenetre, text="Bleu", variable=var_choix, value="bleu")
choix_rouge.pack()
choix_vert.pack()
choix_bleu.pack()

liste = Listbox(fenetre)
liste.pack()
liste.insert(END, "Pierre")
liste.insert(END, "Feuille")
liste.insert(END, "Ciseau")

cadre = Frame(fenetre, width=768, height=576, borderwidth=1)
cadre.pack(fill=BOTH)

message = Label(cadre, text="Notre fenêtre")
message.pack(side="top", fill=X)

# On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre

fenetre.mainloop()

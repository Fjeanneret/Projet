import tkinter
from tkinter.filedialog import *

import webbrowser
from Main import *


def Parcourir():
	FileName = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt'),('all files','.*')])
	main(FileName)

def Afficher():
	webbrowser.open("result.html", new=0, autoraise=True)
	
fenetre = Tk()
fenetre.title("Extraction d'annotations") 

# bouton Parcourir
bouton=Button(fenetre, command=Parcourir, text="Parcourir",  width="25", height="3", background ="#3a6d4f", activebackground="#bfb3da", font=("bold",15), fg="#f1f1f1",  activeforeground="#f1f1f1", relief="flat", cursor="based_arrow_down")
bouton = bouton.pack()

#Afficher le premier diagramme
bouton=Button(fenetre, command=Afficher, text="Afficher", bg="#E8C868", activebackground="#eed68e", width="25", height="3", font=("bold",15),fg="#f1f1f1", activeforeground="#f1f1f1", relief="flat", cursor="top_right_corner")
bouton = bouton.pack() 


mainloop()

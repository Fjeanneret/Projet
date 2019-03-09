import tkinter
from tkinter.filedialog import *

import webbrowser
from Morgane.mainM import *
from Florian.mainF import *
from Damien.mainD import *

		
	
## button functions
player =""


def Parcourir():
	FileName = askopenfilename(title="Ouvrir votre document",filetypes=[('txt files','.txt'),('all files','.*')])
	openedFile = open(FileName)
	readFile = openedFile.read()
	txt.delete(1.0,END)
	txt.insert('1.0', readFile)
	
	
def radiobutton():
	global player
	player = str(choix.get())
	print(player)

def file_save():
    name=asksaveasfile(mode='w',defaultextension=".txt")
    text2save= open_new("{}/result.html".format(player))
    name.write(text2save.read())
    name.close


def Afficher():
	a="C:/Program Files/Mozilla Firefox"
	webbrowser.open('file://' + os.path.realpath('{}/result.html'.format(player)), new=0, autoraise=True)
	
	
def Envoyer():
	
	#Relevant files
	template = open("{}/template.html".format(player),"r")
	result = open("{}/result.html".format(player),"w")
	result.write(template.read())
	template.close()

	#Gene and Specie Data
	data = txt.get('1.0', END+'-1c')
	
	#Main calling
	if player == "Morgane":
		mainM(fenetre, data, result, txt)
	elif player == "Damien":
		mainD(fenetre, data, result, txt)
	else :
		mainF(fenetre, data, result, txt)
	

	
	
	#Printing and Save button 
	bouton=Button(bottomframe, command=Afficher, image = resultIcon, bg="#f1f1f1", activebackground="#eed68e", width="225",height="130", font=("bold",15),fg="#f1f1f1", activeforeground="#f1f1f1", relief="flat", cursor="top_right_corner")
	bouton = bouton.pack(side=LEFT)
	bouton=Button(bottomframe, command=file_save, image = saveIcon, bg="#ffffff", activebackground="#eed68e", width="225",height="130", font=("bold",15),fg="#f1f1f1", activeforeground="#f1f1f1", relief="flat", cursor="top_right_corner")
	bouton = bouton.pack(side=LEFT)
	
	
## Tkinter widgets 

fenetre = Tk()
fenetre.resizable(width=False, height=False)
fenetre.title("Extraction d'annotations") 

# Pictures
dinner = PhotoImage(file=os.path.join("",'t.png'))
trash = PhotoImage(file=os.path.join("",'trash.png'))
upload = PhotoImage(file=os.path.join("",'upload.png'))
resultIcon = PhotoImage(file=os.path.join("",'print.png'))
saveIcon = PhotoImage(file=os.path.join("",'save.png'))

# Boxes
bottomframe = Frame(fenetre)
bottomframe.pack(fill=X, side = BOTTOM )
fr = Frame(fenetre)
fr.pack(fill=X, side = BOTTOM )
w = Label(fenetre, text="Choose your player", height="2", background ="#525266", activebackground="#D4A45F",font=("bold",15), fg="#f1f1f1")
w.pack(fill=X)




choix = StringVar()
R1 = Radiobutton(fenetre, text="Morgane", variable=choix, value="Morgane", command=radiobutton)
R1.pack()

R2 = Radiobutton(fenetre, text="Damien", variable=choix, value="Damien", command=radiobutton)
R2.pack()

R3 = Radiobutton(fenetre, text="Florian", variable=choix, value="Florian", command=radiobutton)
R3.pack()


	


#Upload text file
UploadButton=Button(fenetre, command=Parcourir, image=upload,  width="450", height="130", bg ="#ffffff", activebackground="#bfb3da", font=("bold",15), relief="flat", cursor="based_arrow_down")
UploadButton = UploadButton.pack(fill=X)

#Text area
txt = Text(fenetre, height=10, width=57, wrap=WORD, fg="#a1a1a1")
txt.insert('1.0', 'Format : Specie <tab> Gene Symbol')
txt.pack(fill=X)

#CleanButton
Button(fr, image=trash, command=lambda: txt.delete(1.0,END),width="225",height="130", background ="#ffffff", activebackground="#E22136", font=("bold",15), fg="#f1f1f1",  activeforeground="#f1f1f1", relief="flat", cursor="based_arrow_down").pack(side=LEFT)

#SendButton
Button(fr, command=Envoyer, image=dinner,width="225",height="130", background ="#f1f1f1", activebackground="#47ADA0", font=("bold",15), fg="#f1f1f1",  activeforeground="#f1f1f1", relief="flat", cursor="based_arrow_down").pack(side=LEFT)


mainloop()

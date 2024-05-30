from tkinter import *
import os

os.system("cls")

def imprimir_esporte():

    ve = vesporte.get()
    if ve == "f":
        print ("Esporte Futebol")
    elif ve == "v":
        print ("Esporte Volei")
    elif ve == "b":
        print ("Esporte Basquete")
    else:
        print ("Selecione um esporte")
    
app=Tk()
app.title ("Radio Bottom")
app.geometry("800x400")
app.configure(bg = "#dde")

vesporte = StringVar()
vcor = StringVar()

bl_esportes = Label(app, text = "Esportes")
bl_esportes.pack()

rb_futebol = Radiobutton(app, text = "Futebol", value = "f", variable = vesporte)
rb_futebol.pack()

rb_volei = Radiobutton(app, text = "Volei", value = "v", variable = vesporte)
rb_volei.pack()

rb_basquete = Radiobutton(app, text = "Basquete", value = "b", variable = vesporte)
rb_basquete.pack()

rb_verde = Radiobutton(app, text = "Verde", value = "#0f0", variable = vcor)
rb_verde.pack()

rb_vermelho = Radiobutton(app, text = "Vermelho", value = "#f00", variable = vcor)
rb_vermelho.pack()

btn_esporte = Button(app, text = "Esporte selecionado", command = imprimir_esporte)
btn_esporte.place (x = 330, y = 155, width = 140, height = 40)

app.mainloop()

imprimir_esporte()
from tkinter import *
import os

os.system("cls")

def imprimir_esporte():

    ve = vesporte.get()
    if ve == "Futebol":
        print ("Esporte Futebol")
    elif ve == "Volei":
        print ("Esporte Volei")
    elif ve == "Basquete":
        print ("Esporte Basquete")
    else:
        print ("Selecione um esporte")
    
app=Tk()
app.title ("Radio Bottom")
app.geometry("800x400")
app.configure(bg = "#dde")

listaEsportes = ["-", "Futebol", "Volei", "Basquete"]

vesporte = StringVar()
vesporte.set(listaEsportes[0])

bl_esportes = Label(app, text = "Esportes")
bl_esportes.pack()

op_esportes = OptionMenu(app, vesporte, *listaEsportes)
op_esportes.pack()

btn_esporte = Button(app, text = "Esporte selecionado", command = imprimir_esporte)
btn_esporte.pack()

app.mainloop()

imprimir_esporte()
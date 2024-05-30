from tkinter import *
import os

pastaApp = os.path.dirname(__file__)

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("980x600")
app.configure(bg = "#dde")

imagem_logo = PhotoImage(file = pastaApp+"\\imagem_teste.png")
label_logo = Label(app, image = imagem_logo)
label_logo.place(x = 10, y = 10)

app.mainloop()
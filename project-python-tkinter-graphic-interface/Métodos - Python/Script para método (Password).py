from tkinter import *

def senha():
    print("Senha digitada", vsenha.get())

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("800x400")
app.configure(bg = "#dde")

vsenha = StringVar()

p_senha = Entry(app, textvariable = vsenha, show = "*")
p_senha.pack()

btn_senha = Button(app, text = "Senha", command = senha)
btn_senha.pack()


app.mainloop()
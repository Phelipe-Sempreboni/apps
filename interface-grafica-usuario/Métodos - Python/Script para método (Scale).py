from tkinter import *

def valor_escala():
    print("Valor da escala é ", sc_escala.get())

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("800x400")
app.configure(bg = "#dde")

lb_valor = Label(app, text = "Valor")
lb_valor.pack()

sc_escala = Scale(app, from_ = 0, to = 100, orient = HORIZONTAL)
sc_escala.set(50)
sc_escala.pack()

btn_valor_escala = Button(app, text = "Valor da escala", command = valor_escala)
btn_valor_escala.pack()


app.mainloop()
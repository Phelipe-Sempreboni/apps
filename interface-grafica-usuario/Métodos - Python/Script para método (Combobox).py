from tkinter import *
from tkinter import ttk

def imprimir_esporte():
    ve = cb_esportes.get()
    print("Esporte ", ve)

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("800x400")
app.configure(bg = "#dde")

lista_esportes = ["Selecione um esporte" ,"Futebol", "Volei", "Basquete"]
lista_valor_inicial = lista_esportes[0]

lb_esportes = Label(app, text = "Esportes")
lb_esportes.pack()

cb_esportes = ttk.Combobox(app, values = lista_esportes)
cb_esportes.set(lista_valor_inicial)
cb_esportes.pack()

btn_esporte = Button(app, text = "Esporte Selecionado", command = imprimir_esporte)
btn_esporte.pack()

app.mainloop()
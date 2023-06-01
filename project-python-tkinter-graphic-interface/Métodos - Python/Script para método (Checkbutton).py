from tkinter import *

def futebolclicado():
    print("Futebol: ", vfutebol.get())

def voleiclicado():
    print("Volei: ", vvolei.get())

def basqueteclicado():
    print("Basquete: ", vbasquete.get())

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("800x400")
app.configure(bg = "#dde")

vfutebol = StringVar()
vvolei = StringVar()
vbasquete = StringVar()

fr_quadro1 = Frame(app, borderwidth = 1, relief = "solid")
fr_quadro1.place(x = 10, y = 10, width = 300, height = 100)

cb_futebol = Checkbutton(fr_quadro1, text = "Futebol", variable = vfutebol, onvalue = "s", offvalue = "n", command = futebolclicado)
cb_futebol.pack(side = LEFT)

cb_volei = Checkbutton(fr_quadro1, text = "Volei", variable = vvolei, onvalue = "s", offvalue = "n", command = voleiclicado)
cb_volei.pack(side = LEFT)

cb_basquete = Checkbutton(fr_quadro1, text = "Basquete", variable = vbasquete, onvalue = "s", offvalue = "n", command = basqueteclicado)
cb_basquete.pack(side = LEFT)


app.mainloop()
from tkinter import *
from tkinter import messagebox


def mostrar_mensagens():
    messagebox.showinfo(title = "LPUS ENERGIA", message = "Python com Tkinter. Projeto de interface gráfica")

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("800x400")
app.configure(bg = "#dde")

vnum_caixa_texto = StringVar()

fr_quadro1 = Frame(app, borderwidth = 1, relief = "solid")
fr_quadro1.place(x = 10, y = 10, width = 300, height = 100)

fr_quadro2 = Frame(app, borderwidth = 1, relief = "solid", bg = "black")
fr_quadro2.place(x = 10, y = 120, width = 300, height = 100)

Label(fr_quadro1, text = "Tipo de caixa (1,2 ou 3)").pack()
tb_num = Entry(fr_quadro1, textvariable = vnum_caixa_texto)
vnum_caixa_texto.set("1")
tb_num.pack()

lb_porfolio = Label(fr_quadro2, text = "LPUS ENERGIA", bg = "black", fg = "#fff", font = ("Comic Sams", 10))
lb_porfolio.pack(side = LEFT, fill = X, expand = TRUE)

btn_mensagem = Button(fr_quadro1, text = "Mostrar mensagem", command = mostrar_mensagens)
btn_mensagem.pack()

app.mainloop()
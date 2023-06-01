from tkinter import *
from tkinter import messagebox


def mostrar_mensagens(tipo_mensagem, mensagem):
    if (tipo_mensagem == "1"):
        messagebox.showinfo(title = "LPUS ENERGIA", message = mensagem)
    elif (tipo_mensagem == "2"):
        messagebox.showwarning(title = "LPUS ENERGIA", message = mensagem)
    elif (tipo_mensagem == "3"):
        messagebox.showerror(title = "LPUS ENERGIA", message = mensagem)

def resetar_tb():
    resultado = messagebox.askyesno("Resetar", "Confirma reset do textbox?")
    if (resultado == True):
        tb_num.delete(0, END)
        tb_num.insert(0, "1")

vmsg = "Teste de mensagens"

app=Tk()
app.title ("Cadastro de Clientes")
app.geometry("800x400")
app.configure(bg = "#dde")

vnum_caixa_texto = StringVar()

Label (app, text = "Tipo de caixa (1,2 ou 3)").pack()
tb_num = Entry(app, textvariable = vnum_caixa_texto)
vnum_caixa_texto.set("1")
tb_num.pack()

btn_mensagem = Button(app, text = "Mostrar mensagem", command = lambda: mostrar_mensagens(vnum_caixa_texto.get(), vmsg))
btn_mensagem.pack()

btn_reset = Button(app, text = "Resetar textbox", command = resetar_tb)
btn_reset.pack()

app.mainloop()
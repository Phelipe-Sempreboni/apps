from tkinter import *
import pyodbc
import os

os.system("cls")

def sem_comando():
    print(" ")


def exec_tela_cadastro_clientes():
    exec(open(tela_cadastro_clientes()))


def conectar_ao_banco_de_dados():

    try:
        conexao = pyodbc.connect(
            Driver='{SQL Server Native Client 11.0}',
            Server='LAPTOP-PI0F6JSQ',
            Database='LPUS_ENERGIA',
            uid='sempreboni',
            pwd='LP23420v*',
            Trusted_Connection='no'
        )
        return conexao.cursor()
    except:
        print("Não foi possível conectar ao banco de dados")

def inserção_dados_clientes_sql():

    if  tb_nome.get() != "":
        vnome = tb_nome.get()
        vfone = tb_fone.get()
        vemail = tb_email.get()
        vobservacoes = tb_observacoes.get("1.0", END)

        cursor = conectar_ao_banco_de_dados()
        cursor.execute("INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('"+vnome+"', '"+vfone+"', '"+vemail+"', '"+vobservacoes+"')") 
        cursor.commit()

        tb_nome.delete(0, END)
        tb_fone.delete(0, END)
        tb_email.delete(0, END)
        tb_observacoes.delete("1.0", END)

        print("Dados do cliente gravados com sucesso")
    else:
        print("Não foi possível gravar os dados do cliente")

def tela_cadastro_clientes():

    global tb_nome
    global tb_fone
    global tb_email
    global tb_observacoes

    app=Tk()
    app.title ("Cadastro de Clientes")
    app.geometry("800x400")
    app.configure(bg = "#dde")

    Label(app, text = "Nome", bg = "#fff", fg = "#009", anchor = W).place(x = 10, y = 10, width = 45, height = 20)
    tb_nome = Entry(app)
    tb_nome.place(x = 10, y = 40, width = 240, height = 20)

    Label(app, text = "Telefone", bg = "#fff", fg = "#009", anchor = W).place(x = 10, y = 70, width = 52, height = 20)
    tb_fone = Entry(app)
    tb_fone.place(x = 10, y = 100, width = 100, height = 20)

    Label(app, text = "E-mail", bg = "#fff", fg = "#009", anchor = W).place(x = 10, y = 130, width = 50, height = 20)
    tb_email = Entry(app)
    tb_email.place(x = 10, y = 160, width = 210, height = 20)

    Label(app, text = "Observações", bg = "#fff", fg = "#009", anchor = W).place(x = 10, y = 190, width = 72, height = 20)
    tb_observacoes = Text(app)
    tb_observacoes.place(x = 10, y = 220, width = 300, height = 100)

    btn = Button(app, text = "Registrar cliente", command=inserção_dados_clientes_sql)
    btn.place(x = 10, y = 350, width = 100, height = 20)

def tela_menus():

    app=Tk()
    app.title ("Menu")
    app.geometry("800x400")
    app.configure(bg = "#dde")

    barra_de_menus = Menu(app)
    menu_contatos = Menu(barra_de_menus, tearoff = 0)

    menu_contatos.add_command(label = "Novo", command = tela_cadastro_clientes)
    menu_contatos.add_command(label = "Pesquisar", command = sem_comando)
    menu_contatos.add_command(label = "Deletar", command = sem_comando)
    menu_contatos.add_separator()
    menu_contatos.add_command(label = "Fechar", command = app.quit)
    barra_de_menus.add_cascade(label = "Contatos", menu = menu_contatos)

    menu_manutencao = Menu(barra_de_menus, tearoff = 0)
    menu_manutencao.add_command(label = "Banco de Dados", command = sem_comando)
    barra_de_menus.add_cascade(label = "Manutençao", menu = menu_manutencao)
    
    menu_sobre = Menu(barra_de_menus, tearoff = 0)
    menu_sobre.add_command(label = "LPUS ENERGIA", command = sem_comando)
    barra_de_menus.add_cascade(label = "Sobre", menu = menu_sobre)
    
    app.config(menu = barra_de_menus)

    app.mainloop()

tela_menus()
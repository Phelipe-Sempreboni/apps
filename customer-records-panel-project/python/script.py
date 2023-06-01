# Nota 1: O projeto abaixo simula um painel principal sobre registros de clientes, com comandos para (inserir, deletar, atualizar, consultar (geral) e consultar por nome) registros de clientes.
# Nota 2: Para este projeto utilizamos o Python 3.8 e como back-end o banco de dados SQL Server Management Studio 2017.
# Nota 3: Todo projeto foi desenvolvido para execução na própria (IDLE) ou (CMD).
# Nota 4: Foi criado no SQL Server um database (LPUS_ENERGIA).
# Nota 5: Foi criado no SQL Server um schema neste database (LPUS_ENERGIA). Schema chamado (clientes).
# Nota 6: Foi criado no SQL Server uma tabela, no schema (clientes). Tabela chamada (tbl_cadastro_clientes).
# Nota 7: Foram inseridos dados nessa tabela de cadastro de clientes.
# Nota 8: Todos esses passos estarão neste repositório deste projeto, tanto o código Python quanto o código SQL Server.
# Nota 9: Se for utilizar o código sem alteração em tabelas, database, etc, copie o código Python e cole na IDLE ou VSCODE e faça o mesmo para o código SQL Server.

# Obs 1: Para verificar o (DRIVER) do SQL Server, conforme temos em todos comandos, você pode seguir o caminho: Tecla do Windows ou no pesquisa, digitar (ODBC), irá abrir uma janela com algumas abas, procure por (DRIVERS) e procure os referente a (SQL Server). Lá estarão as informações de (DRIVERS).

# Obs 2: Caso não queira autenticação por SQL Server e sim autenticação por Windows, altere o comando da função (conectar()) chamado (Trusted_Connection) de 'no' para 'yes', e, retire o campo (pwd), pois, conexões com autenticação não necessitam de senhas, logo, o campo pode ser apagado.

# 1º Passo: Copie o código Python e cole na IDLE ou VSCODE e faça o mesmo para o código SQL Server
# 2º Passo: Leia os passos do código SQL Server e execute prestando atenção nos comentários.
# 3º Passo: Após execução dos comandos SQL Server, até o (INSERT INTO), que são a inserção de dados, vá para o arquivo Python.
# 4º Passo: Antes de executar o arquivo Python, altere os campos que estão comentados, que seriam os da função (conectar()).
# 5º Passo: Teste a execução dos programas e suas execuções.

import os
import pyodbc

def conectar():
    try:
        conexao = pyodbc.connect(
            Driver='{SQL Server Native Client 11.0}', #Altere de acordo com seu driver. A (#Nota4) fala desse assunto.
            Server='SERVIDOR', #Insira seu servidor.
            Database='DATABASENAME',#Insira o nome do banco de dados (database) que você quer conectar.
            uid='USUARIO', #Insira seu usuário.
            pwd='SENHA', #Insira sua senha.
            Trusted_Connection='no' #Este campo em (no) refere-se ao tipo de autentição, neste caso, autenticação SQL Server.
        )
        return conexao.cursor()
    except:
        print('Não foi possível conectar ao banco de dados.')
  
def menu_principal():
    os.system("cls")

    print('------- Painel Principal -------')
    print('\'')

    print("1 - Inserir novo registro")
    print("2 - Deletar registro")
    print("3 - Atualizar registro")
    print("4 - Consultar registros")
    print("5 - Consultar registro por nome")
    print("6 - Sair")

def menu_inserir():

    os.system("cls")

    nome_cliente = input('Digite o nome do cliente: ')
    telefone_cliente = input ('Digite o telefone do cliente: ')
    email_cliente = input ('Digite o e-mail do cliente: ')

    cursor = conectar()
    cursor.execute("INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('"+nome_cliente+"', '"+telefone_cliente+"', '"+email_cliente+"')")
    cursor.commit()

def menu_deletar_id():

    os.system("cls")

    deletar_id_cliente = input("Digite o ID do registro do cliente a ser deletado: ")

    cursor = conectar()
    cursor.execute("DELETE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] WHERE N_IDCLIENTE = '"+deletar_id_cliente+"'")
    cursor.commit()

def menu_atualizar():

    os.system("cls")

    atualizar_id_cliente = input("Digite o ID do registro do cliente a ser alterado: ")

    cursor = conectar()
    cursor.execute("SELECT * FROM [LPUS_Energia].[clientes].[tbl_cadastro_clientes] WHERE N_IDCLIENTE = '"+atualizar_id_cliente+"'")
    resultado_nome_cliente = cursor.fetchall()[0][1]

    cursor.execute("SELECT * FROM [LPUS_Energia].[clientes].[tbl_cadastro_clientes] WHERE N_IDCLIENTE = '"+atualizar_id_cliente+"'")
    resultado_telefone_cliente = cursor.fetchall()[0][2]

    cursor.execute("SELECT * FROM [LPUS_Energia].[clientes].[tbl_cadastro_clientes] WHERE N_IDCLIENTE = '"+atualizar_id_cliente+"'")
    resultado_email_cliente = cursor.fetchall()[0][3]

    nome_cliente = input('Digite o nome do cliente: ')
    telefone_cliente = input ('Digite o telefone do cliente: ')
    email_cliente = input ('Digite o e-mail do cliente: ')

    if(len(nome_cliente)==0):
        nome_cliente = resultado_nome_cliente
    if(len(telefone_cliente)==0):
        telefone_cliente = resultado_telefone_cliente
    if(len(email_cliente)==0):
        email_cliente = resultado_email_cliente

    cursor.execute("UPDATE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] SET T_NOMECLIENTE = '"+nome_cliente+"', T_TELEFONECLIENTE = '"+telefone_cliente+"', T_EMAILCLIENTE = '"+email_cliente+"' WHERE N_IDCLIENTE = '"+atualizar_id_cliente+"'")
    cursor.commit()

def menu_consultar_registros():

    os.system("cls")

    cursor = conectar()
    cursor.execute("SELECT * FROM [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]")
    resultado = cursor.fetchall()
    limite = 25
    contador = 0
    for r in resultado:
        print("ID: {0: <3} Nome: {1: <30} Telefone: {2: <15} E-mail {3: <30}".format(r[0], r[1], r[2], r[3]))
        contador+=1;
        if(contador>=limite):
            contador = 0
            os.system("pause")
            os.system("cls")
    print('Fim da lista de clientes cadastrados')
    os.system("pause")

def menu_consultar_registros_nome():

    os.system("cls")

    consultar_registros_cliente = input("Digite o nome: ")

    cursor = conectar()
    cursor.execute("SELECT * FROM [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] WHERE T_NOMECLIENTE LIKE '%"+consultar_registros_cliente+"%'")
    resultado = cursor.fetchall()
    limite = 25
    contador = 0
    for r in resultado:
        print("ID: {0: <3} Nome: {1: <30} Telefone: {2: <15} E-mail {3: <30}".format(r[0], r[1], r[2], r[3]))
        contador+=1;
        if(contador>=limite):
            contador = 0
            os.system("pause")
            os.system("cls")
    os.system("pause")

opcao = 0
while opcao !=6:
    menu_principal()
    opcao = int(input("Digite uma opção: "))
    if opcao == 1:
        menu_inserir()
    elif opcao == 2:
        menu_deletar_id()
    elif opcao == 3:
        menu_atualizar()
    elif opcao == 4:
        menu_consultar_registros()
    elif opcao == 5:
        menu_consultar_registros_nome()
    elif opcao == 6:
        os.system("cls")
        print('Programa finalizado.')
    else:
        os.system("cls")
        print('Opção inválida')
        os.system("pause")

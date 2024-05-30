-- 1º Passo: Criar um database para alocar as informações. Criarei um chamado (LPUS_Energia) com nome ficticio.

-- Criação com comando (CREATE TABLE) mais simples, sem parametros.
USE master;
CREATE DATABASE LPUS_ENERGIA;
GO

-- Comando (DROP DATABASE) caso queira execluir 0 banco de dados.
USE master;
DROP DATABASE LPUS_ENERGIA;
GO

---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- 2º Passo: Criar um schema (agrupamento) para tabela que iremos criar para cadastros de clientes.

-- Criação com comando (CREATE SCHEMA) mais simples, sem parametros.
USE LPUS_ENERGIA;
GO

CREATE SCHEMA clientes;
GO

---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- 3º Passo: Criar a tabela que receberá os dados dos cadastros dos clientes.
-- Essa tabela terá uma chave primária, que será a coluna N_IDCONTATO com autoincremento do número de ID.

-- Criação com comando (CREATE TABLE).
CREATE TABLE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]
(
    N_IDCLIENTE INT IDENTITY (1,1) NOT NULL,
    T_NOMECLIENTE VARCHAR (80),
    T_TELEFONECLIENTE VARCHAR (30),
    T_EMAILCLIENTE VARCHAR (50)
    CONSTRAINT PK_N_IDCLIENTE PRIMARY KEY CLUSTERED (N_IDCLIENTE)
);
GO

-- Teste com comando (SELECT) para verificar estrutura da tabela.
SELECT * FROM [LPUS_Energia].[clientes].[tbl_cadastro_clientes]

-- Comando auxiliar de (STORED PROCEDURE) do sistema para verificar estrutura/informações da tabela.
USE LPUS_ENERGIA;
GO

sp_help 'clientes.tbl_cadastro_clientes'

-- Comando de (DROP TABELA) caso seja necessário execluir a tabela criada.
DROP TABLE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]

-- Comando de (TRUNCATE TABLE) caso seja necessário excluir dados da tabela. Essa opção também zera os ids de autoincremento e não é possível recuperar esses dados, pois, não temos arquivos de logs de transações no comando (TRUNCATE TABLE).
-- Você se quiser também pode utilizar o (DELETE), que continua com os ids de autoincremento e tem arquivos de logs de transações para possíveis recuperações.
TRUNCATE TABLE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]
DELETE [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes]
---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- Comando abaixo de (INSERT INTO) para fazer testes de inserção, tanto no SQL quanto em Python.

INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Ronaldo Henrique', '1194458264', 'ronaldoe@outlook.com')
INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Adriano Barbosa', '1194454785', 'adriano@outlook.com')
INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Eduardo Leão', '1188596347', 'eduardo@outlook.com')
INSERT INTO [LPUS_ENERGIA].[clientes].[tbl_cadastro_clientes] VALUES ('Silvio de Lima', '11974126895', 'silvio@outlook.com')

---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x---------x

-- Vá para o script do Python, para executar e testar o painel principal de registro de clientes.
import sqlite3
import time

from tabulate import tabulate
from abc import abstractmethod, ABC


class BancoDeDados:
    @staticmethod
    def criar_tabelas():
        conn = sqlite3.connect('atacadinho.db')
        conn.execute('PRAGMA foreign_keys=on')
        conn_cursor = conn.cursor()
        ddl = """
            CREATE TABLE IF NOT EXISTS pessoas(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome VARCHAR(70) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                dt_nasc DATE NOT NULL,
                telefone VARCHAR(13) NOT NULL,
                email VARCHAR(60) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tiposFuncionarios(
                id_tipoFunc INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                descricao VARCHAR(70) NOT NULL                        
            );

            CREATE TABLE IF NOT EXISTS funcionarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                dt_cadastro DATE NOT NULL,
                pessoa_id INTEGER NOT NULL,
                tipoFunc_id INTERGER NOT NULL,
                id_register INTEGER NULL,
                CONSTRAINT fk_funcionario_tipoFuncionarios
                    FOREIGN KEY(tipoFunc_id)
                    REFERENCES tiposFuncionarios(id_tipoFunc)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_funcionario_pessoa
                    FOREIGN KEY(pessoa_id)
                    REFERENCES pessoas(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS logins(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome_usuario VARCHAR(60) NOT NULL,
                senha VARCHAR(60) NOT NULL,
                funcionario_id INTEGER NULL,
                CONSTRAINT fk_login_funcionario
                    FOREIGN KEY(funcionario_id)
                    REFERENCES funcionarios(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS categorias(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                descricao VARCHAR(255) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome VARCHAR(60) NOT NULL,
                valor_unitario DECIMAL(10,2),
                funcionarios_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                CONSTRAINT fk_produtos_funcionarios
                    FOREIGN KEY(funcionarios_id)
                    REFERENCES funcionarios(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_produtos_categorias
                    FOREIGN KEY(categoria_id)
                    REFERENCES categorias(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
        
            CREATE TABLE IF NOT EXISTS registro_movimentacao(
                id_registro_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS estoque(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                id_registro_movimentacao INTEGER NOT NULL,
                data_hora DATETIME default current_timestamp,
                id_funcionario INTERGER NOT NULL,
                CONSTRAINT fk_estoque_registro_movimentacao
                    FOREIGN KEY(id_registro_movimentacao)
                    REFERENCES registro_movimentacao(id_registro_movimentacao)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_estoque_funcionarios
                    FOREIGN KEY(id_funcionario)
                    REFERENCES funcionarios(id)
                CONSTRAINT fk_estoque_produtos
                    FOREIGN KEY(produto_id)
                    REFERENCES produtos(id)
            );
        """

        conn_cursor.executescript(ddl)

        conn.close()

    @staticmethod
    def validar_login(nome_usuario, senha):
        conn = sqlite3.connect('atacadinho.db')
        conn_cursor = conn.cursor()

        dql = """
            SELECT f.id, p.nome, f.tipoFunc_id
            FROM funcionarios f
            INNER JOIN pessoas p 
                ON p.id = f.pessoa_id
            INNER JOIN logins l
                ON l.funcionario_id = f.id 
                AND (l.nome_usuario = ? AND l.senha = ?);
        """

        conn_cursor.execute(dql, [nome_usuario, senha])
        dados_usuario = conn_cursor.fetchone()
        conn.close()

        return dados_usuario

    @staticmethod
    def consultar_usuarios():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT f.id , p.nome, tf.descricao 
	        FROM funcionarios f 
		        INNER JOIN pessoas p 
			        ON p.id = f.id 
		        INNER JOIN tiposFuncionarios tf
			        ON f.tipoFunc_id = tf.id_tipoFunc;
        """

        cursor.execute(dql)

        usuarios = cursor.fetchall()

        conn.close()

        print(tabulate(
            usuarios,
            headers=["ID", "NOME", "TIPO FUNCIONÁRIO"],
            tablefmt="fancy_grid"
        ))

    @staticmethod
    def cadastrar_usuarios(id_funcionario, nome, cpf, dt_nasc, telefone, email, tipo, nome_usuario, senha):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dml_table_pesssoas = """
            INSERT INTO pessoas(nome, cpf, dt_nasc, telefone, email)
            VALUES(?, ?, ?, ?, ?);
        """
        dql_max_pessoa = """
            SELECT MAX(id) FROM pessoas
        """
        dml_table_funcionarios = """
            INSERT INTO funcionarios(dt_cadastro, pessoa_id, tipoFunc_id, id_register)
            VALUES(?, ?, ?, ?);
        """
        dql_max_funcionario = """
            SELECT MAX(id) FROM funcionarios;
        """
        dml_table_logins = """
            INSERT INTO logins(nome_usuario, senha, funcionario_id)
            VALUES(?, ?, ?);
        """

        cursor.execute(dml_table_pesssoas, [
            nome, cpf, dt_nasc, telefone, email
        ])

        cursor.execute(dql_max_pessoa)
        last_pessoa = cursor.fetchone()

        cursor.execute(dml_table_funcionarios, [
            '2002-10-12', last_pessoa, tipo, id_funcionario
        ])

        cursor.execute(dql_max_funcionario)
        last_funcionario = cursor.fetchone()

        cursor.execute(dml_table_logins, [
            nome_usuario, senha, last_funcionario
        ])

        print(f'Usuário inserido com sucesso!!!')


    @staticmethod
    def tipos_usuarios():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT * FROM tiposFuncionarios
        """

        cursor.execute(dql)
        tipos_funcionarios = cursor.fetchall()
        conn.close()

        return tipos_funcionarios


class Pessoa:
    @staticmethod
    def fazer_login():
        nome_usuario = input('\nNome de Usuário: ')
        senha = input('\nSenha: ')

        user = BancoDeDados.validar_login(nome_usuario, senha)

        return user

    @staticmethod
    def sair_conta():
        pass


class Administrador(Pessoa):
    def __init__(self, id_admin, nome):
        self.__id_admin = id_admin
        self.__nome = nome
        self.banco = None

    @property
    def id_admin(self):
        return self.__id_admin

    @property
    def nome(self):
        return self.__nome

    def cadastrar_usuarios(self):
        nome = input('\nNome: ')

        cpf = input('\nCPF: ')

        data_nascimento = input('\nData de Nascimento: ')

        telefone = input('\nTelefone')

        email = input('\nEmail: ')

        print(tabulate(
            BancoDeDados.tipos_usuarios(),
            headers=["TIPO FUNCIONÁRIO"],
            tablefmt="fancy_grid"
        ))

        tipo_usuario = input('\nTipo de usuário: ')

        nome_usuario = input('\nNome_usuario: ')

        senha = input('\nSenha')

        BancoDeDados.cadastrar_usuarios(self.id_admin, nome, cpf, data_nascimento, telefone, email, tipo_usuario,
                                        nome_usuario, senha)

    def atualizar_administradores(self):
        pass

    def atualizar_funcionarios(self):
        pass

    def deletar_administradores(self):
        pass

    def deletar_funcionarios(self):
        pass


class Funcionario(Pessoa):
    def __init__(self, id, nome):
        self.__id = id
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    def sair_conta(self):
        pass


class Movimentacao(ABC):
    @abstractmethod
    def deletar_produto(self):
        pass

    @abstractmethod
    def inserir_produto(self):
        pass

    @abstractmethod
    def alterar_produto(self):
        pass

    @abstractmethod
    def consultar_produto(self):
        pass


class Venda(Movimentacao):
    def deletar_produto(self):
        pass

    def inserir_produto(self):
        pass

    def alterar_produto(self):
        pass

    def consultar_produto(self):
        pass

    def gerar_nota_fiscal(self):
        pass


class Estoque(Movimentacao):
    def deletar_produto(self):
        pass

    def inserir_produto(self):
        pass

    def alterar_produto(self):
        pass

    def consultar_produto(self):
        pass

import sqlite3
import database
from abc import abstractmethod, ABC


conn = sqlite3.connect('atacadinho.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = on")
cursor.executescript(database.tabelas)


class Pessoa:
    @staticmethod
    def fazer_login():
        username = input('\nNome de usuário: ')

        senha = input('\nSenha: ')

        dql = """
            SELECT f.id, p.nome, f.tipoFunc_id
            FROM funcionarios f
            INNER JOIN pessoas p
                ON p.id = f.pessoa_id
            INNER JOIN logins l
                ON l.funcionario_id = f.id
                AND (l.nome_usuario = ? AND l.senha = ?)
        """

        with conn:
            cursor.execute(dql, [username, senha])


        return cursor.fetchone()

    @staticmethod
    def sair_conta():
        pass


class Administrador(Pessoa):
    def __init__(self, id_admin, nome):
        self.__id = id_admin
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    def consultar_administradores(self):
        pass

    def consultar_funcionarios(self):
        pass

    def cadastrar_administradores(self):
        pass

    def cadastrar_funcionarios(self):
        pass

    def atualizar_administradores(self):
        pass

    def atualizar_funcionarios(self):
        pass

    def deletar_administradores(self):
        pass

    def deletar_funcionarios(self):
        pass

    def fazer_login(self, username, senha):
        pass

    def sair_conta(self):
        pass


class Funcionario(Pessoa):
    def __init__(self, id_funcionario, nome):
        self.__id = id_funcionario
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

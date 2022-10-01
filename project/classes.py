from abc import ABC, abstractmethod


class Pessoa(ABC):
    @abstractmethod
    def fazer_login(self, username, senha):
        pass

    @abstractmethod
    def sair_conta(self):
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
    def __init__(self, id_pessoa, nome):
        pass

    def fazer_login(self, username, senha):
        pass

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


class Estoque(Movimentacao):
    def deletar_produto(self):
        pass

    def inserir_produto(self):
        pass

    def alterar_produto(self):
        pass

    def consultar_produto(self):
        pass

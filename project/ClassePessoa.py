class Pessoa:
    def __init__(self, nome, cpf, matricula, tipo, senha):
        self.matriculaValidar = None
        self.nome = nome
        self.cpf = cpf
        self.matricula = matricula
        self.tipo = tipo
        self.senha = senha

    def login(self, matriculaValidar, senhaValidar):
        self.matriculaValidar = matriculaValidar
        self.senhaValidar = senhaValidar
        ###CRUD PARA VALIDAR O LOGIN


class Admin(Pessoa):
    def __init__(self, nome, cpf, matricula, tipo, senha):
        super().__init__(nome, cpf, matricula, tipo, senha)

    def cadastrarUser(self):
        print(self.nome)  ##INSERIR CRUD AQUI

    def deletarUser(self):
        print(self.nome)  ##INSERIR CRUD AQUI

    def atualizarUser(self):
        print(self.nome)  ##INSERIR CRUD AQUI

    def consultarUser(self):
        print(self.nome)  ##INSERIR CRUD AQUI


class User(Pessoa):
    def __init__(self, nome, cpf, matricula, tipo, senha):
        super().__init__(nome, cpf, matricula, tipo, senha)

    def adicionarProduto(self):
        self.produto = input(int("Insira o código (ID) do produto:\n"))
        listaVenda = []
        listaVenda.append(self.produto)
        return listaVenda

    def consultarVendas(self):
        print("Diego fará um CRUD")

    def consultarVendas(self):
        print("Diego fará um CRUD")

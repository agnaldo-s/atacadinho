from abc import ABC, abstractmethod


class Movimentacao(ABC):
    @abstractmethod
    def deletar(self):
        print("Diego irá inserir um CRUD")

    def inserir(self):
        print("Diego irá inserir um CRUD")

    def alterar(self):
        print("Diego irá inserir um CRUD")

    def consultar(self):
        print("Diego irá inserir um CRUD")


class Venda(Movimentacao):
    def deletar(Movimentacao):
        print("Diego irá fazer um CRUD para deletar do banco de dados quando a venda for cancelada pelo user")

    def inserir(Movimentacao):
        print("Classe talvez não seja utilizada aqui")

    def alterar(Movimentacao):
        print("Diego irá fazer um CRUD para atualizar o banco de dados quando a venda for autorizada pelo funcionário")

    def consultar(self):
        print("Diego irá inserir um CRUD para consultar o valor de determinado produto já cadastrado")

    def autorizarVenda(self):
        option = input(int("Selecione a opção abaixo:\n1 - Pagamento Confirmado;\n2 - Pagamento não autorizado;"))
        if option == 1:
            return True
        elif option == 2:
            return False
        else:
            print("Valor inválido")  ##estabelecer aqui forma de controle caso o usuário insira algo erroneamente;

    def imprimirVenda(self):
        print("Diego fará um CRUD aqui? não sei, pensar em como imprimir o resultado de uma ÚNICA venda!")


class Estoque(ABC):
    def deletar(Movimentacao):
        print("Diego irá fazer um CRUD para deletar do banco de dados produtos que o Admin queira deletar do banco")

    def inserir(Movimentacao):
        print("Diego irá fazer um CRUD para cadastrar novos produtos ao estoque")

    def alterar(Movimentacao):
        print("Diego irá fazer um CRUD para atualizar informações de algum produto específico já cadastrado no estoque")

    def consultar(self):
        print("Diego irá inserir um CRUD para consultar algum produto do estoque")

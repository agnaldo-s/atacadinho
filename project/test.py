class Produto:
    def __init__(self, id_p, nome):
        self.id_p = id_p
        self.nome = nome


class Client:
    def __init__(self, nome):
        self.nome = nome
        self.produtos = []

    def add_produto(self):
        id_prod = input('id: ')
        nome = input('nome prod: ')
        self.produtos.append(Produto(id_prod, nome))

    def ls_prod(self):
        for prod in self.produtos:
            print(prod.__dict__)

    def del_prod(self):
        id_remove = input('id_remove: ')
        for prod in self.produtos:
            if prod.id_p == id_remove:
                self.produtos.remove(prod)


c1 = Client('agnaldo')
c1.add_produto()
c1.add_produto()
c1.add_produto()
c1.add_produto()
c1.ls_prod()
c1.del_prod()
c1.ls_prod()


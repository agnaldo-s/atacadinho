from tabulate import tabulate


class A:
    def __init__(self, nome):
        self.nome = nome


class B:
    def __init__(self):
        self.persons = []

    def add_person(self, a):
        quantity = int(input('Quantity >> '))
        self.persons.append([a, quantity])

    def ls_persons(self):
        for i in self.persons:
            print(i[0].nome, i[1])


print(tabulate([
    [produto[0].nome, produto[0].valor_unitario, produto[1]]],
    headers=["PRODUTO", "VALOR UNITARIO", "QUANTIDADE"],
    tablefmt="fancy_grid"
))

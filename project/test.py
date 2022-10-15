#
# print(tabulate([
#     [produto[0].nome, produto[0].valor_unitario, produto[1]]],
#     headers=["PRODUTO", "VALOR UNITARIO", "QUANTIDADE"],
#     tablefmt="fancy_grid"
# ))
from tabulate import tabulate
from classes import Produto 

total = 0

produtos_para_vender = [
        [Produto('Pureza', 4.50, 1, 1), 4], 
        [Produto('Fanta Laranja', 5.55, 1, 1), 1]
        ]

for j in produtos_para_vender:
    total += j[0].valor_unitario * j[1]

cupom = []

for i in produtos_para_vender:
    cupom.append([i[0].nome, i[0].valor_unitario, i[1]])

print(tabulate([["CUPOM FISCAL"]], tablefmt="fancy_grid"))
print(tabulate(cupom, tablefmt="fancy_grid"))
print(tabulate([[f"TOTAL: R${total}"]], tablefmt="fancy_grid"))


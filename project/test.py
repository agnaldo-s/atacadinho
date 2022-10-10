#
# print(tabulate([
#     [produto[0].nome, produto[0].valor_unitario, produto[1]]],
#     headers=["PRODUTO", "VALOR UNITARIO", "QUANTIDADE"],
#     tablefmt="fancy_grid"
# ))

from datetime import datetime, date
import re

a = [(1,), (2,)]

b = int(input('number: '))

for i in a:
    for j in i:
        if b == j:
            print('tem id')
        else:
            print('nao tem id')



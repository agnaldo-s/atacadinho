#
# print(tabulate([
#     [produto[0].nome, produto[0].valor_unitario, produto[1]]],
#     headers=["PRODUTO", "VALOR UNITARIO", "QUANTIDADE"],
#     tablefmt="fancy_grid"
# ))


from classes import BancoDeDados

a = [(4, 'bebidas'), (9, 'salgados'), (11, 'doces')]

id_cat = int(input('id: '))

print(a)

for i in a:
    for j in i:
        if id_cat == j:
            print(i)




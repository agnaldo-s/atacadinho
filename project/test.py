#
# print(tabulate([
#     [produto[0].nome, produto[0].valor_unitario, produto[1]]],
#     headers=["PRODUTO", "VALOR UNITARIO", "QUANTIDADE"],
#     tablefmt="fancy_grid"
# ))

from datetime import datetime, date
import re

from tabulate import tabulate

print(tabulate(
    [
        ["Nome", "Diego"],
        ["CPF", "123.123.123-12"],
        ["Data de Nascimento", "17-10-2002"],
        ["Telefone", "91988505828"],
        ["Email", "diego@gmail.com"],
        ["Tipo Usuário", "Admin"],
        ["Nome de Usuário", "reis"],
        ["Senha", "123456"]
    ], headers=["Coluna", "Dados"], tablefmt="psql"
))

a = 'ana paula'

print(a.replace(' ', '').isalpha())

import os
from classes import *
from time import sleep


def header1(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    while True:
        header1('MENU PRINCIPAL')

        menu_principal = input(
            '\n[1] - Login'
            '\n\n[2] - Sair\n\n>> '
        )

        match menu_principal:
            case '1':
                login()
            case '2':
                print('\nVolte sempre!!!')
                sleep(1)
                quit()
            case _:
                print('\nINVÁLIDO!!!')
                sleep(1)
                clear()


def login():
    header1('LOGIN')

    while True:
        tipo_usuario = Pessoa.fazer_login()

        if tipo_usuario is None:
            print('\nNome de Usuário ou senha incorretos. Informe novamente!')
        elif tipo_usuario[2] == 1:
            area_admin(Administrador(tipo_usuario[0], tipo_usuario[1]))
        elif tipo_usuario[2] == 2:
            area_funcionario(Funcionario(tipo_usuario[0], tipo_usuario[1]))


def area_admin(admin):
    admin.banco = BancoDeDados()
    header1('ADMIN')

    while True:
        opcoes_admin = input(f"Olá, {admin.nome}!"
                             "\nO que deseja fazer?\n"
                             "\n[1] - Consultar Usuários"
                             "\n[2] - Cadastrar Usuários"
                             "\n[3] - Atualizar Usuários"
                             "\n[4] - Deletar Usuários"
                             "\n\n[5] - Usar Estoque"
                             "\n\n[6] - Sair\n\n>> ")
        match opcoes_admin:
            case '1':
                admin.banco.consultar_usuarios()
            case '2':
                admin.cadastrar_usuarios()
            case '3':
                admin.atualizar_usuarios()
            case '4':
                admin.deletar_usuarios()
            case '5':
                area_estoque(admin)
            case _:
                print('\nInválido! Informe novamente!')


def area_funcionario(funcionario):
    header1('FUNCIONÁRIO')

    while True:
        opcoes_funcionario = input(f"Olá, {funcionario.nome}!"
                                   "\nO que deseja fazer?\n"
                                   "\n[1] - Venda"
                                   "\n\n[2] - Sair\n\n>> ")

        match opcoes_funcionario:
            case '1':
                pass
            case _:
                print('\nInválido! Informe novamente!')


def area_estoque(admin):
    admin.estoque = Estoque()

    while True:
        opcoes_estoque = input('\nO que deseja fazer?\n'
                               '\n[1] - Consultar produtos'
                               '\n[2] - Inserir produtos'
                               '\n[3] - Adicionar categoria'
                               '\n[4] - Atualizar produtos\n\n>> ')

        match opcoes_estoque:
            case '1':
                admin.estoque.consultar_produtos()
            case '2':
                while True:
                    admin.adicionar_produtos()
                    print('\nSeus produtos: ')
                    admin.listar_produtos()

                    opcoes_produtos = input("O que deseja fazer?"
                                            "\n[1] - Adicionar mais um produto"
                                            "\n[2] - Cadastrar os produtos no sistema"
                                            "\n\n[3] - Sair e apagar\n\n>> ")

                    match opcoes_produtos:
                        case '1':
                            pass
                        case '2':
                            admin.estoque.inserir_produtos(admin.produtos)
                            break
                        case '3':
                            admin.produtos.clear()
                            break
                        case _:
                            print('Inválido! Informe novamente!')

            case '3':
                admin.adicionar_categoria()
            case '4':
                admin.estoque.alterar_produto()
            case _:
                print('\nInválido! Informe corretamente!')


BancoDeDados.criar_tabelas()
main()

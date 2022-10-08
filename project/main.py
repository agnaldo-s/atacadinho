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

    opcoes_admin = input(f"Olá, {admin.nome}!"
                         "\nO que deseja fazer?\n"
                         "\n[1] - Consultar Usuários"
                         "\n[2] - Cadastrar Usuários"
                         "\n[3] - Atualizar Usuários"
                         "\n[4] - Deletar Usuários"
                         "\n\n[5] - Sair\n\n>> ")

    match opcoes_admin:
        case '1':
            admin.banco.consultar_usuarios()
            sleep(999)


def area_funcionario(funcionario):
    header1('FUNCIONÁRIO')

    opcoes_funcionario = input(f"Olá, {funcionario.nome}!"
                               "\nO que deseja fazer?\n"
                               "\n[1] - Venda"
                               "\n\n[2] - Sair\n\n>> ")


BancoDeDados.criar_tabelas()
main()

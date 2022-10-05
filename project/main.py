import os
import sqlite3
from classes import *
from time import sleep

conexao_banco = sqlite3.connect('atacadinho.db')
conexao_banco.execute('PRAGMA foreign_keys=on')
cursor = conexao_banco.cursor()


def header1(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main(conn, conn_cursor):
    while True:
        header1('MENU PRINCIPAL')

        menu_principal = input(
            '\n[1] - Login'
            '\n\n[2] - Sair\n\n>> '
        )

        match menu_principal:
            case '1':
                login(conn, conn_cursor)
            case '2':
                print('\nVolte sempre!!!')
                sleep(1)
                quit()
            case _:
                print('\nINVÁLIDO!!!')
                sleep(1)
                clear()


def login(conn, conn_cursor):
    header1('LOGIN')

    while True:
        tipo_usuario = Pessoa.fazer_login(conn, conn_cursor)

        if tipo_usuario is None:
            print('\nNome de Usuário ou senha incorretos. Informe novamente!')
        elif tipo_usuario[2] == 1:
            area_admin(Administrador(tipo_usuario[0], tipo_usuario[1]))
        elif tipo_usuario[2] == 2:
            area_funcionario(Funcionario(tipo_usuario[0], tipo_usuario[1]))


def area_admin(admin):
    header1('ADMIN')

    opcoes_admin = input(f"Olá, {admin.nome}!"
                         "\nO que deseja fazer?\n"
                         "\n[1] - Consultar Usuários"
                         "\n[2] - Cadastrar Usuários"
                         "\n[3] - Atualizar Usuários"
                         "\n[4] - Deletar Usuários"
                         "\n\n[5] - Sair\n\n>> ")


def area_funcionario(funcionario):
    header1('FUNCIONÁRIO')

    opcoes_funcionario = input(f"Olá, {funcionario.nome}!"
                               "\nO que deseja fazer?\n"
                               "\n[1] - Venda"
                               "\n\n[2] - Sair\n\n>> ")


database.tabelas(conexao_banco, cursor)
main(conexao_banco, cursor)

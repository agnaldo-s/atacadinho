import os
import sqlite3
import database
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

    username = input('\nUsername: ')

    senha = input('\nSenha: ')

    database.validar_login(conn, conn_cursor, username, senha)
    sleep(999)


database.tabelas(conexao_banco, cursor)
main(conexao_banco, cursor)

import os
import sqlite3
import database
from classes import Pessoa
from time import sleep

conexao_banco = sqlite3.connect('atacadinho.db')
conexao_banco.execute('PRAGMA foreign_keys=on')
cursor = conexao_banco.cursor()

pessoa = Pessoa()


def header1(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main(conn, conn_cursor, person):
    while True:
        header1('MENU PRINCIPAL')

        menu_principal = input(
            '\n[1] - Login'
            '\n\n[2] - Sair\n\n>> '
        )

        match menu_principal:
            case '1':
                login(conn, conn_cursor, person)
            case '2':
                print('\nVolte sempre!!!')
                sleep(1)
                quit()
            case _:
                print('\nINVÁLIDO!!!')
                sleep(1)
                clear()


def login(conn, conn_cursor, person):
    header1('LOGIN')

    nome_usuario = input('\nNome de Usuário: ')

    senha = input('\nSenha: ')

    tipo_usuario = person.fazer_login(conn, conn_cursor, nome_usuario, senha)

    sleep(999)


database.tabelas(conexao_banco, cursor)
main(conexao_banco, cursor, pessoa)

import os
import stdiomask


def header1(msg):
    print('=' * 50)
    print(f'{msg:^50}')
    print('=' * 50)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def mask_password():
    senha = stdiomask.getpass(prompt='\nSenha: ', mask='*')
    return senha

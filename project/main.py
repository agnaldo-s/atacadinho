from useful import *
from classes import *
from time import sleep


def main():
    while True:
        clear()
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


def login():
    clear()

    while True:
        header1('LOGIN')
        tipo_usuario = Pessoa.fazer_login()

        if tipo_usuario is None:
            print('\nNome de Usuário ou senha incorretos. Informe novamente!')
            sleep(1)
            clear()
        else:
            print('\nLogin efetuado com sucesso!')
            sleep(1)
            if tipo_usuario[2] == 1:
                area_admin(Administrador(tipo_usuario[0], tipo_usuario[1]))
            elif tipo_usuario[2] == 2:
                area_funcionario(Funcionario(tipo_usuario[0], tipo_usuario[1]))


def area_admin(admin):
    admin.banco = BancoDeDados()

    while True:
        clear()
        header1('ADMIN')
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
                clear()
                header1('FUNCIONÁRIOS')
                admin.banco.consultar_usuarios()
                input('\nAperte ENTER para sair ')
            case '2':
                admin.cadastrar_usuarios()
            case '3':
                admin.atualizar_usuarios()
            case '4':
                admin.deletar_usuarios()
            case '5':
                area_estoque(admin)
            case '6':
                if admin.sair_conta():
                    return main()
            case _:
                print('\nInválido! Informe novamente!')
                sleep(1)


def area_funcionario(funcionario):

    while True:
        clear()
        header1('FUNCIONÁRIO')
        opcoes_funcionario = input(f"Olá, {funcionario.nome}!"
                                   "\nO que deseja fazer?\n"
                                   "\n[1] - Venda"
                                   "\n\n[2] - Sair\n\n>> ")

        match opcoes_funcionario:
            case '1':
                area_venda(funcionario)
            case '2':
                if funcionario.sair_conta():
                    return main()
            case _:
                print('\nInválido! Informe novamente!')


def area_venda(funcionario):

    funcionario.funcao = Venda()

    while True:
        clear()
        header1('ÁREA VENDA')
        opcoes_venda = input('\nO que deseja fazer?\n'
                             '\n[1] - Inserir produto'
                             '\n[2] - Remover produto'
                             '\n[3] - Listar produtos'
                             '\n[4] - Finalizar venda'
                             '\n\n[5] - Sair\n\n>> ')

        match opcoes_venda:
            case '1':
                funcionario.funcao.inserir_produto()
            case '2':
                pass
            case '3':
                funcionario.funcao.consultar_produto()
                input('\nAperte ENTER para sair')
            case '4':
                funcionario.funcao.gerar_nota_fiscal()
                input('\nAperte ENTER para sair')
            case '5':
                break
            case _:
                print('\nInválido! Informe novamente')


def area_estoque(admin):
    admin.estoque = Estoque()

    while True:
        clear()
        header1('ESTOQUE')
        opcoes_estoque = input('\nO que deseja fazer?\n'
                               '\n[1] - Consultar produtos'
                               '\n[2] - Inserir produtos'
                               '\n[3] - Adicionar categoria'
                               '\n[4] - Atualizar produtos'
                               '\n[5] - Entrada de produtos'
                               '\n\n[6] - Sair'
                               '\n\n>> ')

        match opcoes_estoque:
            case '1':
                admin.estoque.consultar_produtos()
                input('\nAperte ENTER para sair')
            case '2':
                if BancoDeDados.return_categorias() == []:
                    print('\nNão foi inserido nenhuma categoria.'
                            '\nAdicione uma para cadastrar um produto')
                    sleep(1)
                else:
                    while True:
                        admin.adicionar_produtos()
                        print('\nSeus produtos: ')
                        admin.listar_produtos()

                        opcoes_produtos = input("\nO que deseja fazer?\n"
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
            case '5':
                admin.estoque.entrada_produto(admin.id_admin)
            case '6':
                break
            case _:
                print('\nInválido! Informe corretamente!')
                sleep(1)


clear()
BancoDeDados.criar_tabelas()
main()

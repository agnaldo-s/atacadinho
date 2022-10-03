from ast import match_case
from tracemalloc import start
from ClassePessoa import Admin 
from ClassePessoa import Funcionario
from ClassePessoa import Pessoa
from ClasseAbstrata import Venda
from ClasseAbstrata import Estoque

class ChamarMenu:
  def __init__(self):
    print("MENU INICIAL")
    opcao = input(int(("Escolha a opção desejada:\n1 - LOGIN \n2 - SAIR")))
    return opcao
  
menuInicial = ChamarMenu()
pessoas = Pessoa()
admin = Admin()
funcionario = Funcionario()
vendas = Venda()
estoque = Estoque()

vendasDia = []

if menuInicial == 1:
  matriculaValidar = input(str("Inserir Usuário:\n"))
  senhaValidar = input(int("Inserir Usuário:\n"))
  tipoUser = pessoas.login(matriculaValidar, senhaValidar)
else:
  pass

while tipoUser == '001':
  ##MENU para ADMIN
  print("MENU ADMIN")
  opcao2 = input(int(("Escolha as opções a baixo:\n1 - Consultar Usuário\n2 - Cadastrar Usuário\n3 - Atualizar Usuário\n4 - Excluir Usuário\n5 - Fazer Logout")))
  match opcao2:
    case 1:
      admin.consultarUser()
      tipoUser == 'x'
    case 2:
      admin.cadastrarUser()
      tipoUser == 'x'
    case 3:
      admin.atualizarUser()
      tipoUser == 'x'
    case 3:
      admin.deletarUser()
      tipoUser == 'x'
    case 4:
      x = menuInicial()
      if x == 1:
        tipoUser = pessoas.login()
      else:
        tipoUser = 'x'

while tipoUser == '002':
  ##MENU FUNCIONÁRIO
  print("MENU FUNCIONÁRIO")
  opcao3 = input(int(("Escolha as opções a baixo:\n1 - Iniciar Venda\n2 -  Consultar Vendas do Dia\n3 - Fazer Logout")))
  match opcao3:
    case 1:
      start = input("Pressione Enter para iniciar!")
      x = 1
      while x != 0:
        produto = input(str("Digite o nome do produto:\n"))
        consultar = vendas.consultar() ##Consultar produto no BD e fazer um CRUD que retorne todos os produtos com o nome digitado pelao usuário, numa lista com o ID do produto ao lado, para o que o usuário escolha qual adicionar ao "carrinho";
        print(consultar)
        x = input("1 - Insira o ID do produto\n2 - Inserir outro produto\n3 - Finalizar Venda")
        if x == 2:
          continue
        elif x == 3:
          x = 0
          vendas.autorizarVenda()
          estoque.deletar(listaVenda)
          break
        else:
          listaVenda = []
          listaVenda.append(x)
          print(listaVenda)
          continue
    case 2:
      vendas.consultar()
    case 3:
      x = menuInicial()
      if x == 1:
        tipoUser = pessoas.login()
      else:
        tipoUser = 'x'




#Validar login
# if #coluna perfil = "001": ENTRAR NO MENU ADMIN
# elif #Coluna perfil = "002" ENTRAR NO MENU FUNCIONÁRIO
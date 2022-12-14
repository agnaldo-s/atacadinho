import re
import sqlite3
from useful import *
from time import sleep
from datetime import datetime, date
from tabulate import tabulate
from abc import abstractmethod, ABC


class BancoDeDados:
    @staticmethod
    def criar_tabelas():
        conn = sqlite3.connect('atacadinho.db')
        conn_cursor = conn.cursor()
        conn_cursor.execute('PRAGMA foreign_keys=on')
        ddl = """
            CREATE TABLE IF NOT EXISTS pessoas(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome VARCHAR(70) NOT NULL,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                dt_nasc DATE NOT NULL,
                telefone VARCHAR(13) NOT NULL,
                email VARCHAR(60) NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tiposFuncionarios(
                id_tipoFunc INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                descricao VARCHAR(70) NOT NULL                        
            );

            CREATE TABLE IF NOT EXISTS funcionarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                dt_cadastro DATE NOT NULL,
                pessoa_id INTEGER NOT NULL,
                tipoFunc_id INTEGER NOT NULL,
                id_register INTEGER NULL,
                CONSTRAINT fk_funcionario_pessoa
                    FOREIGN KEY(pessoa_id)
                    REFERENCES pessoas(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_funcionario_tipoFunc
                    FOREIGN KEY(tipoFunc_id)
                    REFERENCES tiposFuncionarios(id_tipoFunc)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS logins(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome_usuario VARCHAR(60) NOT NULL,
                senha VARCHAR(60) NOT NULL,
                funcionario_id INTEGER NULL,
                CONSTRAINT fk_login_funcionario
                    FOREIGN KEY(funcionario_id)
                    REFERENCES funcionarios(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS categorias(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                descricao VARCHAR(255) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                nome VARCHAR(60) NOT NULL,
                valor_unitario DECIMAL(10,2),
                funcionarios_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                CONSTRAINT fk_produtos_funcionarios
                    FOREIGN KEY(funcionarios_id)
                    REFERENCES funcionarios(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_produtos_categorias
                    FOREIGN KEY(categoria_id)
                    REFERENCES categorias(id)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
            );
        
            CREATE TABLE IF NOT EXISTS registro_movimentacao(
                id_registro_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS movimentacao(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                produto_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                id_registro_movimentacao INTEGER NOT NULL,
                data_hora DATETIME DEFAULT current_timestamp,
                id_funcionario INTERGER NOT NULL,
                vlr_unitario DECIMAL(10,2),
                CONSTRAINT fk_estoque_registro_movimentacao
                    FOREIGN KEY(id_registro_movimentacao)
                    REFERENCES registro_movimentacao(id_registro_movimentacao)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                CONSTRAINT fk_estoque_funcionarios
                    FOREIGN KEY(id_funcionario)
                    REFERENCES funcionarios(id)
                CONSTRAINT fk_estoque_produtos
                    FOREIGN KEY(produto_id)
                    REFERENCES produtos(id)
            );
        """

        conn_cursor.executescript(ddl)

        conn.close()

    @staticmethod
    def validar_login(nome_usuario, senha):
        conn = sqlite3.connect('atacadinho.db')
        conn_cursor = conn.cursor()

        dql = """
            SELECT f.id, p.nome, f.tipoFunc_id
            FROM funcionarios f
            INNER JOIN pessoas p 
                ON p.id = f.pessoa_id
            INNER JOIN logins l
                ON l.funcionario_id = f.id 
                AND (l.nome_usuario = ? AND l.senha = ?);
        """

        conn_cursor.execute(dql, [nome_usuario, senha])
        dados_usuario = conn_cursor.fetchone()
        conn.close()

        return dados_usuario

    @staticmethod
    def validar_cpf(cpf):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        validadores = [False, False]

        dql = """
            SELECT cpf 
            FROM pessoas
            WHERE cpf = ?
        """

        cursor.execute(dql, [cpf])
        cpf_encontrado = cursor.fetchone()
        conn.close()

        if cpf_encontrado is None:
            validadores[0] = True

        if re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            validadores[1] = True

        if False in validadores:
            return False
        else:
            return True

    @staticmethod
    def validar_telefone(telefone):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        validadores = [False, False]

        dql = """
            SELECT telefone 
            FROM pessoas
            WHERE telefone = ?
        """

        cursor.execute(dql, [telefone])
        dado_telefone = cursor.fetchone()
        conn.close()

        if dado_telefone is None:
            validadores[0] = True

        if re.match(r'^\d{2}9[0-9]{8}$', telefone):
            validadores[1] = True

        if False in validadores:
            return False
        else:
            return True

    @staticmethod
    def validar_email(email):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        validadores = [False, False]

        dql = """
            SELECT email
            FROM pessoas
            WHERE email = ?;
        """

        cursor.execute(dql, [email])
        dado_email = cursor.fetchone()
        conn.close()

        if dado_email is None:
            validadores[0] = True

        if re.fullmatch(r'^[a-zA-Z0-9]+[._]?[a-zA-Z0-9]*@[a-zA-Z]+\.[a-z]{3}$', email):
            validadores[1] = True

        return False if False in validadores else True

    @staticmethod
    def return_id_tipoFuncionarios():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT id_tipoFunc
            FROM tiposFuncionarios;
        """

        cursor.execute(dql)
        ids_tuple = cursor.fetchall()
        conn.close()

        ids = []

        for tup in ids_tuple:
            for id_tipo_func in tup:
                ids.append(id_tipo_func)

        return ids

    @staticmethod
    def return_id_funcionarios():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT id 
            FROM funcionarios
        """

        cursor.execute(dql)
        ids_funcionarios_tuple = cursor.fetchall()
        conn.close()

        func_ids = []

        for tuple in ids_funcionarios_tuple:
            for id in tuple:
                func_ids.append(id)

        return func_ids

    @staticmethod
    def consultar_valor_produto(id_produto):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT valor_unitario
            FROM produtos
            WHERE id = ?
        """

        cursor.execute(dql, [id_produto])
        valor_produto = cursor.fetchone()[0]
        conn.close()

        return valor_produto


    @staticmethod
    def validar_nome_usuario(nome_usuario):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT nome_usuario 
            FROM logins
            WHERE nome_usuario = ?;
        """

        cursor.execute(dql, [nome_usuario])
        dado_nome_usuario = cursor.fetchone()
        conn.close()

        return True if dado_nome_usuario is None else False

    @staticmethod
    def consultar_usuarios():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT f.id , p.nome, tf.descricao 
	        FROM funcionarios f 
		        INNER JOIN pessoas p 
			        ON p.id = f.pessoa_id 
		        INNER JOIN tiposFuncionarios tf
			        ON f.tipoFunc_id = tf.id_tipoFunc;
        """

        cursor.execute(dql)

        usuarios = cursor.fetchall()

        conn.close()

        print(tabulate(
            usuarios,
            headers=["ID", "NOME", "TIPO FUNCION??RIO"],
            tablefmt="fancy_grid"
        ))

    @staticmethod
    def cadastrar_usuarios(id_funcionario, nome, cpf, dt_nasc, telefone, email, tipo, nome_usuario, senha):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dml_table_pesssoas = """
            INSERT INTO pessoas(nome, cpf, dt_nasc, telefone, email)
            VALUES(?, ?, ?, ?, ?);
        """
        dql_max_pessoa = """
            SELECT MAX(id) FROM pessoas
        """
        dml_table_funcionarios = """
            INSERT INTO funcionarios(dt_cadastro, pessoa_id, tipoFunc_id, id_register)
            VALUES(date('now'), ?, ?, ?);
        """
        dql_max_funcionario = """
            SELECT MAX(id) FROM funcionarios;
        """
        dml_table_logins = """
            INSERT INTO logins(nome_usuario, senha, funcionario_id)
            VALUES(?, ?, ?);
        """

        cursor.execute(dml_table_pesssoas, [
            nome, cpf, dt_nasc, telefone, email
        ])

        cursor.execute(dql_max_pessoa)
        last_pessoa = cursor.fetchone()[0]

        cursor.execute(dml_table_funcionarios, [
            last_pessoa, tipo, id_funcionario
        ])

        cursor.execute(dql_max_funcionario)
        last_funcionario = cursor.fetchone()[0]

        cursor.execute(dml_table_logins, [
            nome_usuario, senha, last_funcionario
        ])

        conn.commit()

        print(f'Usu??rio inserido com sucesso!!!')

    @staticmethod
    def tipos_usuarios():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT * FROM tiposFuncionarios
        """

        cursor.execute(dql)
        tipos_funcionarios = cursor.fetchall()
        conn.close()

        return tipos_funcionarios

    @staticmethod
    def return_id_pessoa_funcionario(id_funcionario):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql_id_table_pessoa_funcionario = """
            SELECT p.id, f.id
            FROM pessoas p
                INNER JOIN funcionarios f
                    ON p.id = f.pessoa_id
                    WHERE f.id = ?
        """

        cursor.execute(dql_id_table_pessoa_funcionario, [id_funcionario])
        id_pessoa = cursor.fetchone()

        conn.close()

        return id_pessoa

    @staticmethod
    def atualizar_telefone(id_funcionario, novo_valor):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        id_pessoa = BancoDeDados.return_id_pessoa_funcionario(id_funcionario)

        dml = """
            UPDATE pessoas
            SET telefone = ?
            WHERE id = ?
        """

        cursor.execute(dml, [novo_valor, id_pessoa[0]])
        conn.commit()
        conn.close()

        print('\nTelefone do usu??rio atualizado!')

    @staticmethod
    def atualizar_email(id_funcionario, novo_valor):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        id_pessoa = BancoDeDados.return_id_pessoa_funcionario(id_funcionario)

        dml = """
            UPDATE pessoas
            SET email = ?
            WHERE id = ?
        """

        cursor.execute(dml, [novo_valor, id_pessoa[0]])
        conn.commit()

        conn.close()

        print('\nEmail do usu??rio atualizado')

    @staticmethod
    def atualizar_nome_de_usuario_e_senha(id_funcionario, novos_valores):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dml = """
            UPDATE logins
            SET nome_usuario = ?, senha = ?
            WHERE funcionario_id = ?
        """

        nome_usuario, senha = novos_valores

        cursor.execute(dml, [nome_usuario, senha, id_funcionario])
        conn.commit()
        conn.close()

        print('\nNome de usu??rio e senha atualizados!')

    @staticmethod
    def deletar_usuarios(id_pessoa):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys=on')

        dml = """
            DELETE FROM pessoas
            WHERE id = ?
        """

        cursor.execute(dml, [id_pessoa])
        conn.commit()

        conn.close()

        print('\nUsu??rio Deletado com sucesso!')

    @staticmethod
    def return_categorias():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT * 
            FROM categorias
        """

        cursor.execute(dql)
        categorias = cursor.fetchall()
        conn.close()

        return categorias

    @staticmethod
    def adicionar_categoria(nome_categoria):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dml = """
            INSERT INTO categorias(descricao)
            VALUES(?)
        """

        cursor.execute(dml, [nome_categoria])
        conn.commit()
        conn.close()

        print('\nCategoria Adicionada com sucesso!')

    @staticmethod
    def inserir_produtos(produtos):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()
        conn.execute('PRAGMA foreign_keys=on;')

        for produto in range(len(produtos)):
            dados_produto = [
                produtos[produto].nome,
                produtos[produto].valor_unitario,
                produtos[produto].id_funcionario,
                produtos[produto].categoria_id
            ]

            dml = """
                INSERT INTO produtos(nome, valor_unitario, funcionarios_id, categoria_id)
                VALUES(?, ?, ?, ?)
            """

            cursor.execute(dml, dados_produto)

        conn.commit()
        conn.close()

        print('\nProdutos adicionados com sucesso!!!')

    @staticmethod
    def consultar_produtos():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT p.id, p.nome, p.valor_unitario, c.descricao 
            FROM produtos p
                INNER JOIN categorias c 
                	ON p.categoria_id = c.id ;	
        """

        cursor.execute(dql)
        produtos = cursor.fetchall()
        conn.close()

        return produtos

    @staticmethod
    def consultar_id_produtos():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT id FROM produtos;
        """

        cursor.execute(dql)
        produtos = cursor.fetchall()
        conn.close()

        ids = []

        for produto in produtos:
            for id in produto:
                ids.append(id)
        
        return ids
    
    def retornar_id_movimentacao():
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()
        dql="""INSERT INTO registro_movimentacao(id_registro_movimentacao) VALUES (NULL);"""
        dql1 = """
            SELECT MAX(id_registro_movimentacao) FROM registro_movimentacao;
        """

        cursor.execute(dql)
        conn.commit()
        cursor.execute(dql1)
        id = cursor.fetchone()[0]
        conn.close()
        return id

    @staticmethod
    def adicionar_movimentacao(produto_id, quantidade, id_registro_movimentacao,id_funcionario,vlr_unitario):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()
        dml = """
                INSERT INTO movimentacao (produto_id, quantidade, id_registro_movimentacao,id_funcionario,vlr_unitario)
                VALUES(?, ?, ?, ?, ?)
            """

        cursor.execute(dml,[produto_id, quantidade, id_registro_movimentacao,id_funcionario,vlr_unitario])

        conn.commit()
        conn.close()

        print('\nMovimenta????o adicionada com sucesso!!!')

    @staticmethod
    def update_nome_produto(id_produto, novo_valor):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys=on')

        dml = """
            UPDATE produtos
            SET nome = ?
            WHERE id = ?
        """

        cursor.execute(dml, [novo_valor, id_produto])

        conn.commit()
        conn.close()

    @staticmethod
    def update_valor_unitario_produto(id_produto, novo_valor):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys=on')

        dml = """
            UPDATE produtos
            SET valor_unitario = ?
            WHERE id = ?
        """

        cursor.execute(dml, [id_produto, novo_valor])
        conn.commit()
        conn.close()

    @staticmethod
    def return_produto(id_produto):
        conn = sqlite3.connect('atacadinho.db')
        cursor = conn.cursor()

        dql = """
            SELECT p.nome, p.valor_unitario, p.funcionarios_id, p.categoria_id
            FROM produtos p
            WHERE id = ?
        """

        cursor.execute(dql, [id_produto])

        dados_produto = cursor.fetchone()

        conn.close()

        return dados_produto


class Pessoa:
    @staticmethod
    def fazer_login():
        nome_usuario = input('\nNome de Usu??rio: ')
        senha = mask_password()

        user = BancoDeDados.validar_login(nome_usuario, senha)

        return user

    @staticmethod
    def sair_conta():
        return True


class Administrador(Pessoa):
    def __init__(self, id_admin, nome):
        self.__id_admin = id_admin
        self.__nome = nome
        self.banco = None
        self.estoque = None
        self.produtos = []

    @property
    def id_admin(self):
        return self.__id_admin

    @property
    def nome(self):
        return self.__nome

    @staticmethod
    def validar_data(data):
        try:
            datetime.strptime(data, '%d-%m-%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_idade(data):
        return False if date.today().year - int(data[6:]) < 18 else True

    def cadastrar_usuarios(self):
        clear()
        header1('CADASTRO USU??RIO')
        while True:
            nome = input('\nNome: ').title()

            if len(nome) < 3:
                print('\nInforme um nome!!!')
                sleep(1)
            elif not nome.replace(' ', '').isalpha():
                print('\nInforme um nome v??lido!')
                sleep(1)
            else:
                break

        while True:
            cpf = input('\nCPF: ')

            if BancoDeDados.validar_cpf(cpf):
                break
            else:
                print('\nInforme um cpf v??lido!')

        while True:
            data_nascimento = input('\nData de Nascimento: ')

            if Administrador.validar_data(data_nascimento):
                if Administrador.validar_idade(data_nascimento):
                    break
                else:
                    print('N??o pode cadastrar uma pessoa com menos de 18 anos.')
            else:
                print('\nInforme uma data v??lida!')

        while True:
            telefone = input('\nTelefone: ')

            if BancoDeDados.validar_telefone(telefone):
                break
            else:
                print('\nTelefone Inv??lido!')

        while True:
            email = input('\nEmail: ')

            if BancoDeDados.validar_email(email):
                break
            else:
                print('\nEmail inv??lido! Informe novamente!')

        id_tipos_funcionarios = BancoDeDados.return_id_tipoFuncionarios()

        while True:
            clear()
            print(tabulate(
                BancoDeDados.tipos_usuarios(),
                headers=["ID", "TIPO FUNCION??RIO"],
                tablefmt="fancy_grid"
            ))

            tipo_usuario = input('\nTipo de usu??rio(id): ')

            if not tipo_usuario.isdecimal():
                print('\nInforme um n??mero v??lido!')
                sleep(1)
            elif int(tipo_usuario) in id_tipos_funcionarios:
                tipo_usuario = int(tipo_usuario)
                break
            else:
                print('\nInforme um id v??lido!')
                sleep(1)

        while True:
            nome_usuario = input('\nNome_usuario: ')

            if len(nome_usuario) < 4:
                print('\nInforme um nome de usu??rio maior!')
            elif not BancoDeDados.validar_nome_usuario(nome_usuario):
                print('\nEsse nome de usu??rio ja existe! Informe um novo!')
            else:
                break

        while True:
            senha = mask_password()

            if len(senha) < 6:
                print('\nInforme uma senha maior! 6 caracteres ou mais!')
            else:
                break

        tipo_usuario_extenso = ""

        if tipo_usuario == 1:
            tipo_usuario_extenso = 'Admin'
        elif tipo_usuario == 2:
            tipo_usuario_extenso = 'Funcionario'

        while True:
            clear()
            print(tabulate(
                [
                    ["Nome", f"{nome}"],
                    ["CPF", f"{cpf}"],
                    ["Data de Nascimento", f"{data_nascimento}"],
                    ["Telefone", f"{telefone}"],
                    ["Email", f"{email}"],
                    ["Tipo Usu??rio", f"{tipo_usuario_extenso}"],
                    ["Nome de Usu??rio", f"{nome_usuario}"],
                    ["Senha", f"{senha}"]
                ], headers=["Coluna", "Dados"], tablefmt="psql"
            ))

            opcao_confirmar_cadastro = input("\nO que deseja fazer?\n"
                                             "\n[1] - Confirmar cadastro"
                                             "\n[2] - Apagar e refazer cadastro"
                                             "\n[3] - Apagar e sair do cadastro"
                                             "\n\n>> ")

            match opcao_confirmar_cadastro:
                case '1':
                    BancoDeDados.cadastrar_usuarios(
                        self.id_admin, nome, cpf,
                        data_nascimento, telefone, email,
                        tipo_usuario, nome_usuario, senha
                    )
                    print('\nUsu??rio cadastrado com sucesso!')
                    sleep(1)
                    break
                case '2':
                    return self.cadastrar_usuarios()
                case '3':
                    print('\nSaindo do cadastro...')
                    sleep(1)
                    break
                case _:
                    print('\nInv??lido! Informe novamente!')
                    sleep(1)

    @staticmethod
    def atualizar_usuarios():
        clear()
        header1('ATUALIZAR USU??RIOS')
        BancoDeDados.consultar_usuarios()

        funcionario_id_update = 0

        while True:
            try:
                funcionario_id_update = int(input('\nQual funcion??rio deseja atualizar(id)? '))
                if funcionario_id_update in BancoDeDados.return_id_funcionarios():
                    break
                else:
                    print('\nO id informado n??o existe. Informe novamente!')
            except ValueError:
                print('\nInforme corretamente!!!')

        while True:
            informacoes_atualizar = input('\nQual informa????o deseja atualizar desse funcion??rio? '
                                          '\n[1] - Telefone'
                                          '\n[2] - Email'
                                          '\n[3] - Nome de Usu??rio e Senha\n\n>> ')

            match informacoes_atualizar:
                case '1':
                    while True:
                        novo_telefone = input('\nNovo valor do telefone: ')

                        if BancoDeDados.validar_telefone(novo_telefone):
                            BancoDeDados.atualizar_telefone(funcionario_id_update, novo_telefone)
                            break
                        else:
                            print('\nTelefone Inv??lido! Informe novamente')
                    break
                case '2':
                    while True:
                        novo_email = input('\nNovo valor do email: ')

                        if BancoDeDados.validar_email(novo_email):
                            BancoDeDados.atualizar_email(funcionario_id_update, novo_email)
                            break
                        else:
                            print('\nEmail inv??lido! Informe novamente!')
                    break
                case '3':
                    while True:
                        novo_username = input('\nNovo Nome de usu??rio: ')

                        if BancoDeDados.validar_nome_usuario(novo_username):
                            break
                        else:
                            print('\nEsse nome de usu??rio j?? existe! Informe novamente outro.')

                    while True:
                        nova_senha = input('\nNova senha: ')

                        if len(nova_senha) < 6:
                            print('\nInforme uma senha maior(6 caracteres)')
                        else:
                            break

                    BancoDeDados.atualizar_nome_de_usuario_e_senha(
                        funcionario_id_update, [novo_username, nova_senha]
                    )
                    break
                case _:
                    print('\nInv??lido! Informe novamente!')

    @staticmethod
    def deletar_usuarios():
        clear()
        header1('DELETAR USU??RIOS')
        BancoDeDados.consultar_usuarios()

        while True:
            id_funcionario = int(input('\nQual funcion??rio deseja deletar? '))

            if id_funcionario in BancoDeDados.return_id_funcionarios():
                break
            else:
                print('\nO id informado n??o existe! Informe novamente!')

        id_pessoa = BancoDeDados.return_id_pessoa_funcionario(id_funcionario)

        BancoDeDados.deletar_usuarios(id_pessoa[0])

    def adicionar_produtos(self):
        valor_unitario = 0.0

        while True:
            nome = input('\nNome produto: ')

            if len(nome) < 3:
                print('\nInforme um nome v??lido!')
            else:
                break

        while True:
            try:
                valor_unitario = float(input('Valor unit??rio: '))
                break
            except ValueError:
                print('\nInforme um valor v??lido!')


        func_id = self.id_admin

        categorias = BancoDeDados.return_categorias()

        id_categorias = []

        for categoria in categorias:
            for id in categoria:
                id_categorias.append(id)

        while True:
            clear()
            print(tabulate(
                categorias,
                headers=["ID", "CATEGORIA"], 
                tablefmt="fancy_grid")
                )

            id_categoria_escolher = input('\nInforme o id da categoria: ')

            try:
                int(id_categoria_escolher)
            except ValueError:
                print('\nInv??lido! Informe novamente!')
                sleep(1)
                continue

            if int(id_categoria_escolher) in id_categorias:
                break
            else:
                print('\nO id informado n??o existe. Informe novamente')
                sleep(1)

        self.produtos.append(Produto(nome, valor_unitario, func_id, id_categoria_escolher))


    def listar_produtos(self):
        produtos = []

        for produto in self.produtos:
            produtos.append([produto.nome, produto.valor_unitario])

        print(tabulate(
            produtos, 
            headers=["PRODUTO", "VALOR UNIT??RIO"],
            tablefmt="fancy_grid"
            ))

    @staticmethod
    def adicionar_categoria():
        nome_categoria = input('Informe uma categoria para adicionar: ')

        BancoDeDados.adicionar_categoria(nome_categoria)


class Funcionario(Pessoa):
    def __init__(self, id_funcionario, nome):
        self.__id = id_funcionario
        self.__nome = nome
        self.funcao = None

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    def sair_conta(self):
        return True


class Movimentacao(ABC):
    @abstractmethod
    def deletar_produto(self):
        pass

    @abstractmethod
    def inserir_produto(self):
        pass

    @abstractmethod
    def alterar_produto(self):
        pass

    @abstractmethod
    def consultar_produto(self):
        pass


class Venda(Movimentacao):
    def __init__(self):
        self.produtos_para_vender = []

    def deletar_produto(self):
        self.consultar_produto()

    def inserir_produto(self):
        print(tabulate(
            BancoDeDados.consultar_produtos(),
            headers=["ID", "NOME", "VALOR UNIT??RIO", "DESCRICAO"],
            tablefmt="fancy_grid"
        ))

        id_produto = int(input('\nInforme o id do produto para adicionar: '))

        nome, valor_unitario, funcionarios_id, categoria_id = BancoDeDados.return_produto(id_produto)

        quantidade = int(input(f'Informe a quantidade do produto {nome}: '))

        self.produtos_para_vender.append([Produto(nome, valor_unitario, funcionarios_id, categoria_id), quantidade])

        print(f'Produto {nome} adicionado!')

    def alterar_produto(self):
        pass

    def consultar_produto(self):
        produtos = []
        for produto in self.produtos_para_vender:
            produtos.append([produto[0].nome, produto[0].valor_unitario, produto[1]])

        print(tabulate(
            produtos, headers=["PRODUTO", "VALOR UNIT??RIO", "QUANTIADE"], tablefmt="fancy_grid"
        ))

    def gerar_nota_fiscal(self):
        total = 0

        for j in self.produtos_para_vender:
            total += j[0].valor_unitario * j[1]

        cupom = []

        for i in self.produtos_para_vender:
            cupom.append([i[0].nome, i[0].valor_unitario, i[1]])

        print(tabulate([["CUPOM FISCAL"]], tablefmt="fancy_grid"))
        print(tabulate(cupom, tablefmt="fancy_grid"))
        print(tabulate([[f"TOTAL: R${total}"]], tablefmt="fancy_grid"))


class Produto:
    def __init__(self, nome, valor_unitario, id_funcionario, categoria_id):
        self.nome = nome
        self.valor_unitario = valor_unitario
        self.id_funcionario = id_funcionario
        self.categoria_id = categoria_id


class Estoque:
    def deletar_produto(self):
        pass

    @staticmethod
    def inserir_produtos(produtos):
        BancoDeDados.inserir_produtos(produtos)

    @staticmethod
    def alterar_produto():
        while True:
            if BancoDeDados.consultar_produtos() == []:
                print('\nN??o existe produtos cadastrados ainda!')
                sleep(1)
                break
            else:
                header1('ATUALIZAR PRODUTO')
                while True:
                    print(tabulate(
                        BancoDeDados.consultar_produtos(),
                        headers=["ID", "PRODUTO", "VALOR UNIT??RIO", "CATEGORIA"],
                        tablefmt="fancy_grid"
                        ))
                    coluna_atualizar = input("\nQual coluna deseja atualizar?:"
                                             "\n[1] - Nome do produto"
                                             "\n[2] - Valor do produto"
                                             "\n\n[3] - Sair\n\n>> ")

                    id_produto = int(input("\nInforme o id do produto para escolher ele: "))

                    match coluna_atualizar:
                        case '1':
                            novo_nome = input('\nNovo nome do produto')
                            BancoDeDados.update_nome_produto(id_produto, novo_nome)
                        case '2':
                            pass
                        case '3':
                            pass

    @staticmethod
    def entrada_produto(admin):
        while True:
            try:
                id_produto = int(input("\nInforme o id do produto: "))
                if id_produto not in BancoDeDados.consultar_id_produtos():
                    print("\nO id informado n??o existe! Informe novamente!")
                else:
                    break
            except:
                print("\n\nInforme um n??mero inteiro!\n")

        while True:
            try:
                quantidade = int(input("\nInforme a quantidade do produto: "))
                if quantidade <= 0:
                    print("\nA quantidade deve ser maior que 0! Informe novamente!")
                else:
                    break
            except:
                print("\n\nInforme um n??mero inteiro!\n\n")
        while True: 
            att_valor = input("\nDeseja atualizar o valor do produto? [S/N]: ").upper()   
            if att_valor not in ['S', 'N']:
                print("\nOp????o inv??lida! Informe novamente!")
                sleep(2)
            else:
                break

        if att_valor == 'S':         
            while True:
                valor = float(input("\nInforme o valor do produto: "))
                if valor <= 0:
                    print("\nO valor deve ser maior que 0! Informe novamente!")
                    sleep(2)
                else:
                    break
        elif att_valor == 'N':
            valor = BancoDeDados.consultar_valor_produto(id_produto)

        id_movimentacao= BancoDeDados.retornar_id_movimentacao()
        BancoDeDados.adicionar_movimentacao(id_produto, quantidade,id_movimentacao, admin, valor) 
        BancoDeDados.update_valor_unitario_produto(id_produto, valor)

    @staticmethod
    def consultar_produtos():
        clear()
        header1('PRODUTOS')
        print(tabulate(
            BancoDeDados.consultar_produtos(),
            headers=["PRODUTO", "VALOR UNIT??RIO", "CATEGORIA"],
            tablefmt="fancy_grid"
        ))

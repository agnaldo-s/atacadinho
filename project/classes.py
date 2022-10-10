import sqlite3
import time

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
            headers=["ID", "NOME", "TIPO FUNCIONÁRIO"],
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

        print(f'Usuário inserido com sucesso!!!')

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

        print('\nTelefone do usuário atualizado!')

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

        print('\nEmail do usuário atualizado')

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

        print('\nNome de usuário e senha atualizados!')

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

        print('\nUsuário Deletado com sucesso!')

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
        nome_usuario = input('\nNome de Usuário: ')
        senha = input('\nSenha: ')

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

    def cadastrar_usuarios(self):
        nome = input('\nNome: ')

        cpf = input('\nCPF: ')

        data_nascimento = input('\nData de Nascimento: ')

        telefone = input('\nTelefone')

        email = input('\nEmail: ')

        print(tabulate(
            BancoDeDados.tipos_usuarios(),
            headers=["TIPO FUNCIONÁRIO"],
            tablefmt="fancy_grid"
        ))

        tipo_usuario = input('\nTipo de usuário: ')

        nome_usuario = input('\nNome_usuario: ')

        senha = input('\nSenha')

        BancoDeDados.cadastrar_usuarios(self.id_admin, nome, cpf, data_nascimento, telefone, email, tipo_usuario,
                                        nome_usuario, senha)

    @staticmethod
    def atualizar_usuarios():
        BancoDeDados.consultar_usuarios()

        while True:
            try:
                funcionario_id_update = int(input('\nQual funcionário deseja atualizar? '))
            except ValueError:
                print('\nInforme corretamente!!!')
            finally:
                break

        while True:
            informacoes_atualizar = input('\nQual informação deseja atualizar desse funcionário? '
                                          '\n[1] - Telefone'
                                          '\n[2] - Email'
                                          '\n[3] - Nome de Usuário e Senha')

            match informacoes_atualizar:
                case '1':
                    novo_telefone = input('\nNovo valor do telefone: ')
                    BancoDeDados.atualizar_telefone(funcionario_id_update, novo_telefone)
                    break
                case '2':
                    novo_email = input('\nNovo valor do email: ')
                    BancoDeDados.atualizar_email(funcionario_id_update, novo_email)
                    break
                case '3':
                    novo_username = input('\nNovo Nome de usuário: ')
                    nova_senha = input('\nNova senha: ')
                    BancoDeDados.atualizar_nome_de_usuario_e_senha(
                        funcionario_id_update, [novo_username, nova_senha]
                    )
                    break
                case _:
                    print('\nInválido! Informe novamente!')

    @staticmethod
    def deletar_usuarios():
        BancoDeDados.consultar_usuarios()

        id_funcionario = int(input('\nQual funcionário deseja deletar? '))

        id_pessoa = BancoDeDados.return_id_pessoa_funcionario(id_funcionario)

        BancoDeDados.deletar_usuarios(id_pessoa[0])

    def adicionar_produtos(self):
        nome = input('\nNome produto: ')
        valor_unitario = float(input('Valor unitário: '))
        func_id = self.id_admin
        print(tabulate(BancoDeDados.return_categorias(), headers=["ID", "CATEGORIA"], tablefmt="fancy_grid"))
        categoria_id = int(input('Informe o id da categoria: '))
        self.produtos.append(Produto(nome, valor_unitario, func_id, categoria_id))

    def listar_produtos(self):
        for produto in self.produtos:
            print(produto.__dict__)

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
        pass


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
        Venda.consultar_produto()

    def inserir_produto(self):
        print(tabulate(
            BancoDeDados.consultar_produtos(),
            headers=["ID", "NOME", "VALOR UNITÁRIO", "DESCRICAO"],
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
            produtos, headers=["PRODUTO", "VALOR UNITÁRIO", "QUANTIADE"], tablefmt="fancy_grid"
        ))

    def gerar_nota_fiscal(self):
        pass


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
        print(tabulate(BancoDeDados.consultar_produtos(),
                       headers=["ID", "PRODUTO", "VALOR_UNITARIO", "CATEGORIA"],
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
    def consultar_produtos():
        print(tabulate(
            BancoDeDados.consultar_produtos(),
            headers=["PRODUTO", "VALOR UNITÁRIO", "CATEGORIA"],
            tablefmt="fancy_grid"
        ))
